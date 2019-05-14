# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime
import math

class ResConfigSettings(models.TransientModel):
	_inherit = 'res.config.settings'

	pt_review_checkpoint = fields.Selection([
		("instant", "Instant approval upon creation"),
		("review", "Require manual approval")
	], default="review", required="True", string="Protocol", config_parameter='ecommerce_product_reviews.checkpoint')

	pt_review_team_ids = fields.Many2one('crm.team', string="Sale Team(s) to Notify", config_parameter='ecommerce_product_reviews.crm_team')

class ProductTemplateReview(models.Model):

	_name = "product.template.review"
	_inherit = ['mail.thread']
	_order = "review_date desc, id desc"
	_sql_constraints = [
		('rating_range', 'check(rating >= 0 and rating <= 5)', 'Rating should be between 0 to 5'),
	]

	@api.model
	def _get_default_state(self):
		checkpoint = self.env['ir.config_parameter'].sudo().get_param('ecommerce_product_reviews.checkpoint')
		if checkpoint == 'instant':
			return '3_approved'
		else:
			return '1_new'

	active = fields.Boolean('Active', default=True)
	state = fields.Selection([
		('1_new', 'New'),
		('2_in_review', 'In Review'),
		('3_approved', 'Approved'),
		('4_rejected', 'Rejected'),
	], string="Review Status", default=_get_default_state, copy=False, index=True, track_visibility='onchange', track_sequence=3)

	name = fields.Char('Review Title')
	body = fields.Text('Review Body')
	review_date = fields.Date('Review Date')
	image = fields.Binary('Review Image')
	rating = fields.Integer('Product Rating')
	partner_id = fields.Many2one('res.partner', string="Author")
	product_tmpl_id = fields.Many2one('product.template', string="Product")

	@api.model
	def create(self, vals):
		new_review = super(ProductTemplateReview, self).create(vals)
		crm_team_id = self.env['ir.config_parameter'].sudo().get_param('ecommerce_product_reviews.crm_team')
		crm_team = self.env['crm.team'].sudo().browse(int(crm_team_id))
		partner_ids = []
		for member in crm_team.member_ids:
			new_review.message_subscribe([member.partner_id.id])

		# new_review.message_post(
		# 	body="%s left you a new review of %s. Check it out!" % (new_review.partner_id.name, new_review.product_tmpl_id.name),
		# 	subject="%s left you a new review" % new_review.partner_id.name,
		# 	subtype='mail.mt_comment')

		if new_review.partner_id:
			new_review.message_subscribe([new_review.partner_id.id])

		return new_review

	def review_in_queue(self):
		self.state = '2_in_review'

	def approve_review(self):
		self.state = '3_approved'

	def reject_review(self):
		self.state = "4_rejected"

class ProductTemplate(models.Model):

	_inherit = "product.template"

	@api.model
	def get_avg_rating(self):
		reviews = self.env['product.template.review'].search([('product_tmpl_id','=',self.id), ('state','=','3_approved')])
		ratings = []

		for review in reviews:
			ratings.append(review.rating)

		if len(ratings):
			return sum(ratings) / len(ratings)
		else:
			return 0

	@api.model
	def get_ecommerce_rating_count(self):
		review_count = self.env['product.template.review'].search([('product_tmpl_id','=',self.id), ('state','=','3_approved')], count=True)
		return review_count

# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.exceptions import UserError
from datetime import datetime
import math
import json

class WebsiteSaleReviews(WebsiteSale):

	@http.route()
	def product(self, product, category='', search='', **kwargs):
		render = super(WebsiteSaleReviews, self).product(product, category, search, **kwargs)
		product = render.qcontext['product']
		review_count = request.env['product.template.review'].search([('product_tmpl_id','=',product.id),('state','=','3_approved')], count=True)
		reviews = request.env['product.template.review'].search([('product_tmpl_id','=',product.id),('state','=','3_approved')], order="review_date desc", limit=5)
		render.qcontext['reviews'] = reviews
		render.qcontext['review_count'] = review_count
		render.qcontext['math'] = math
		return render

class ReviewPages(http.Controller):
	@http.route('/shop/product/<int:product_id>/reviews', type='http', auth='public', website=True, csrf=False)
	def new_review(self, name, email, location, title, body, rating, image=None, product_id=None):
		Partners = request.env['res.partner']
		existing = Partners.sudo().search([('email','=',email)], order="write_date desc")
		if not request.env.user._is_public():
			partner_id = request.env.user.partner_id
		elif len(existing):
			partner_id = existing[0]
		else:
			partner_id = Partners.sudo().create({
				'name': name,
				'email': email,
				'street': location,
			})

		try:
			new_review = request.env['product.template.review'].sudo().create({
				'name': title,
				'body': body,
				'review_date': datetime.now(),
				'rating': rating,
				'product_tmpl_id': int(product_id),
				'partner_id': partner_id.id,
			})
			if image:
				new_review.image = image
			return json.dumps({'success': 1})
		except UserError as error:
			return json.dumps({'success': 0, 'error': error.name})

	# @http.route('/shop/product/<int:product_id>/reviews/<int:review_id>/image', type='http', auth='public', website=True, csrf=False)
	# def new_review(self, image, product_id=None):


	@http.route('/shop/product/<int:product_id>/reviews/page', type='http', auth='public', website=True, csrf=False)
	def new_page(self, page, direction, product_id=None):
		if direction == 'next':
			reviews = request.env['product.template.review'].sudo().search([('product_tmpl_id','=',int(product_id))], offset=int(page) * 5, limit=5, order="review_date desc")
			html = request.env['ir.ui.view'].sudo().render_template(
				'ecommerce_product_reviews.reviews_body',
				values=dict({
					'reviews': reviews,
				}),
			)
			return html
		elif direction == 'prev':
			reviews = request.env['product.template.review'].sudo().search([('product_tmpl_id','=',int(product_id))], offset=(int(page) - 2) * 5, limit=5, order="review_date desc")
			html = request.env['ir.ui.view'].sudo().render_template(
				'ecommerce_product_reviews.reviews_body',
				values=dict({
					'reviews': reviews,
				}),
			)
			return html
		else:
			reviews = request.env['product.template.review'].sudo().search([('product_tmpl_id','=',int(product_id))], offset=(int(page) - 1) * 5, limit=5, order="review_date desc")
			html = request.env['ir.ui.view'].sudo().render_template(
				'ecommerce_product_reviews.reviews_body',
				values=dict({
					'reviews': reviews,
				}),
			)
			return html
# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WebsiteProductCategories(models.Model):

	_inherit = "product.public.category"

	mega_image = fields.Binary('Mega Menu Image')
	mega_exclude = fields.Boolean('Exclude from Mega Menu')

class WebsiteMenu(models.Model):

	_inherit = "website.menu"

	has_mega = fields.Boolean('Use Mega Menu', default=False)
	mega_menu_id = fields.Many2one('vendere.mega.menu', string="Mega Menu")

	def create_mega_menu(self):
		self.ensure_one()
		mega_menu = self.env['vendere.mega.menu'].sudo().create({
			'name': 'mm_' + self.name,
			'menu_base_id': self.id,
		})
		self.write({
			'has_mega': True,
			'mega_menu_id': mega_menu.id,
		})
		action = self.env.ref('vendere_mega_menu.action_website_mega_menu_form').read()[0]
		action['res_id'] = mega_menu['id']
		return action

	def unlink_mega_menu(self):
		self.ensure_one()
		self.write({
			'has_mega': False,
		})
		self.mega_menu_id.unlink()

class VendereMegaMenu(models.Model):

	_name = "vendere.mega.menu"

	name = fields.Char("Mega menu Name")
	mega_type = fields.Selection([
		('shop', 'Product Category'),
		('meta', 'Meta Information')
	], string="Mega Menu Type")
	menu_base_id = fields.Many2one('website.menu', string="Base Menu")

	meta_tags = fields.Many2many('product.template.tag', string="Meta Tags to Display")

	@api.model
	def get_product_categories(self):
		Categs = self.env['product.public.category'].sudo().search([])
		Parents = Categs.filtered(lambda c: not c.parent_id and not c.mega_exclude)
		categs = []
		for parent in Parents:
			res = {'parent': {'name': parent.name, 'id': parent.id, 'record': parent}, 'children': [],}
			for child in parent.child_id:
				if not child.mega_exclude:
					res['children'].append({
						'name': child.name,
						'id': child.id,
					})
			categs.append(res)

		return categs
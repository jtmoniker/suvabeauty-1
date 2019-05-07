import math

from odoo import models, api, fields

class IrModuleModule(models.Model):
	_inherit = "ir.module.module"

	@api.model
	def check_installed(self, name):
		module = self.env['ir.module.module'].sudo().search([('name','=',name)])
		if module.state == 'installed':
			xml_id = False
			view = False
			if name == 'website_sale_wishlist':
				xml_id = self.env['ir.model.data'].sudo().search([('module','=','website_sale_wishlist'),('name','=','add_to_wishlist')])
			else:
				xml_id = self.env['ir.model.data'].sudo().search([('module','=','website_sale_comparison'),('name','=','add_to_compare')])

			if xml_id:
				res_id = xml_id.res_id
				view = self.env['ir.ui.view'].sudo().browse(res_id)
				print(view.name)
				print(view.active)
				active = view.active

			if view and active:
				return True
			else:
				return False
		else:
			return False

class ThemeDefault(models.AbstractModel):
	_inherit = 'theme.utils'

	def _theme_default_post_copy(self, mod):
		self.disable_view('website_theme_install.customize_modal')


class WebsiteProductCategories(models.Model):

	_inherit = "product.public.category"

	vendere_category_organize = fields.Boolean('Organize By Ecommerce Tag', default=False)
	vendere_finish_organize = fields.Boolean('Organize By Product Finish', default=False)

	@api.model
	def get_featured_categs(self):
		featured_categories = self.env['product.public.category'].search([('featured_category','=',True)])
		c_data = []
		for category in featured_categories:
			c_data.append({
				'id': category.id,
				'name': category.name,
			})
		return c_data

class ProductTemplate(models.Model):

	_inherit = "product.template"

	@api.model
	def _get_featured_products(self):
		featured_products = self.env['product.template'].search([('featured_product','=',True),('website_published','=',True)])
		return featured_products

	@api.model
	def update_featured_products(self, ids, website_id):
		res = {}
		Products = self.env['product.template'].browse(ids)
		for product in Products:
			combination = product.sudo()._get_first_possible_combination()
			price_info = product.with_context(website_id=int(website_id)).sudo()._get_combination_info(combination, add_qty=1)
			res[product.id] = {
				'price': price_info['list_price'],
			}
		return res
			
	@api.model
	def _get_style_classes(self):
		html_class = ""
		for style in self.website_style_ids:
			html_class += style.html_class + ' '

		return html_class

	@api.model
	def _get_forecasted_qty(self):
		return self.env['product.template'].sudo().browse(self.id).virtual_available

class IrUiView(models.Model):

	_inherit = "ir.ui.view"

	@api.model
	def _prepare_qcontext(self):
		qcontext = super(IrUiView, self)._prepare_qcontext()
		qcontext['math'] = math
		return qcontext



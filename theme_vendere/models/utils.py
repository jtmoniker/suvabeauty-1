import math

from odoo import models, api, fields

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
	def update_featured_products(self, ids):
		res = {}
		Products = self.env['product.template'].browse(ids)
		for product in Products:
			combination = product.sudo()._get_first_possible_combination()
			price_info = product.sudo()._get_combination_info(combination, add_qty=1)
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

class IrUiView(models.Model):

	_inherit = "ir.ui.view"

	@api.model
	def _prepare_qcontext(self):
		qcontext = super(IrUiView, self)._prepare_qcontext()
		qcontext['math'] = math
		return qcontext



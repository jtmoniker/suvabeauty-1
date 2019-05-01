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
	def get_featured_products(self):
		featured_products = self.env['product.template'].search([('featured_product','=',True),('website_published','=',True)])
		p_data = []
		for product in featured_products:
			combination = product.sudo()._get_first_possible_combination()
			price_info = product.sudo()._get_combination_info(combination, add_qty=1)
			product_variants = product.sudo().product_variant_ids
			p_data.append({
				'id': product.id,
				'name': product.name,
				'category': product.public_categ_ids[0].name,
				'price': price_info['list_price'],
				'rating': product.rating_get_stats()['avg'],
				'rating_count': product.rating_get_stats()['total'],
				'product_id': product_variants[0].id
			})
		return p_data

	@api.model
	def _get_style_classes(self):
		html_class = ""
		for style in self.website_style_ids:
			html_class += style.html_class + ' '

		return html_class



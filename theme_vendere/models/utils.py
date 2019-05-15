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

class Website(models.Model):

	_inherit = "website"

	def get_current_pricelist(self):
        """
        :returns: The current pricelist record
        """
        # The list of available pricelists for this user.
        # If the user is signed in, and has a pricelist set different than the public user pricelist
        # then this pricelist will always be considered as available
        available_pricelists = self.get_pricelist_available()
        pl = None
        partner = self.env.user.partner_id
        if request and request.session.get('website_sale_current_pl'):
            # `website_sale_current_pl` is set only if the user specifically chose it:
            #  - Either, he chose it from the pricelist selection
            #  - Either, he entered a coupon code
            pl = self.env['product.pricelist'].browse(request.session['website_sale_current_pl'])
            if pl not in available_pricelists:
                pl = None
                request.session.pop('website_sale_current_pl')
        if not pl:
            # If the user has a saved cart, it take the pricelist of this last unconfirmed cart
            pl = partner.last_website_so_id.pricelist_id
            if not pl:
                # The pricelist of the user set on its partner form.
                # If the user is not signed in, it's the public user pricelist
                pl = partner.property_product_pricelist
            if available_pricelists and pl not in available_pricelists:
                # If there is at least one pricelist in the available pricelists
                # and the chosen pricelist is not within them
                # it then choose the first available pricelist.
                # This can only happen when the pricelist is the public user pricelist and this pricelist is not in the available pricelist for this localization
                # If the user is signed in, and has a special pricelist (different than the public user pricelist),
                # then this special pricelist is amongs these available pricelists, and therefore it won't fall in this case.
                pl = available_pricelists.sudo().search([], order="sequence asc")[0]

        if not pl:
            _logger.error('Fail to find pricelist for partner "%s" (id %s)', partner.name, partner.id)
        return pl



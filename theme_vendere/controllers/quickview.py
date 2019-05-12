# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import math
import json

class QuickviewData(http.Controller):
	@http.route('/shop/product/quickview/<int:product_id>', type='http', auth='public', website=True)
	def handler(self, product_id=None):
		if product_id:
			product = request.env['product.template'].sudo().browse(int(product_id))
			images = []
			combination = product.sudo()._get_first_possible_combination()
			price_info = product.sudo()._get_combination_info(combination, add_qty=1)
			csrf = request.csrf_token()
			product_variants = product.sudo().product_variant_ids

			for image in product.product_image_ids:
				images.append(image.id)

			content = {
				'name': product.name,
				'category': product.public_categ_ids[0].name,
				'price': price_info['price'],
				'images': images,
				'description': product.quickview_description,
				'token': csrf,
				'variant': product_variants[0].id,
				'availability': product.inventory_availability,
				'virtual_available': product.virtual_available,
				'threshold': product.available_threshold
			}

			return json.dumps(content)

	@http.route('/shop/products/featured', type='http', auth='public', website=True, csrf=False)
	def update_featured_products(self):
		pricelist = request.website.get_current_pricelist()
		html = request.env['ir.ui.view'].sudo().render_template(
				'theme_vendere.snippet_featured_products',
				values=dict({
					'pricelist': pricelist,
					'math': math,
					'request': request,
				}),
			)

		return html
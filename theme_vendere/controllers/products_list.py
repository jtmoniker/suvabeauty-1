# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery
from odoo.addons.website_sale.controllers.main import TableCompute
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.http_routing.models.ir_http import slug
import json
import math

PPG = 20  # Products Per Page
PPR = 4

class WebsiteSaleVendere(WebsiteSale):

	@http.route()
	def shop(self, page=0, category=None, search='', ppg=False, show_list=False, tag=None, **post):
		render = super(WebsiteSaleVendere, self).shop(page, category, search, PPG, **post)

		# IDENTIFY WEBSITE THEME
		website_id = request.env.context['website_id']
		theme_id = request.env['website'].browse(website_id).theme_id.id
		theme_name = request.env['ir.module.module'].sudo().browse(theme_id).name

		if theme_name == 'theme_vendere':
			Products = request.env['product.template']

			render.qcontext['math'] = math

			if show_list:
				render.qcontext['show_list'] = True

			if tag:
				product_tag = request.env['product.template.tag'].browse(int(tag))
				tag_products = Products.search([('meta_tags','in',int(tag))])
				render.qcontext['products'] = tag_products

			if category:
				category = request.env['product.public.category'].browse(int(category)) if type(category) is str else category
				grid_finish = True if category.vendere_finish_organize else False
				grid_tag = True if category.vendere_category_organize else False

				if grid_finish or grid_tag:
					render.qcontext['grid'] = True

					organize = []
					if grid_finish:
						orgs = request.env['product.finish'].sudo().search([], order="sequence asc")
						subcategories = request.env['product.public.category'].search([('id','child_of',category.id),('id','!=',category.id)], order='sequence asc')
					else:
						orgs = request.env['product.template.tag'].sudo().search([], order="sequence asc")
						subcategories = request.env['product.public.category'].search([('id','child_of',category.id)], order='sequence asc')

					for org in orgs:
						res = {
							'org': org,
							'products': [],
						}
						if grid_finish:
							org_products = Products.search([('finish_id','=',org.id),('public_categ_ids','child_of',category.id)])
						else:
							org_products = Products.search([('ecommerce_tag','=',org.id),('public_categ_ids','child_of',category.id)])

						if len(org_products):
							for sc in subcategories:
								if grid_finish:
									products = Products.search([('finish_id','=',org.id),('public_categ_ids','child_of',sc.id)], order=self._get_search_order(post))
								else:
									products = Products.search([('ecommerce_tag','=',org.id),('public_categ_ids','child_of',sc.id)], order=self._get_search_order(post))
								
								res['products'].append(products)

								if not len(products):
									continue

							if not len(res['products']):
								continue
							else:
								organize.append(res)

					render.qcontext['org'] = organize

		return render

	@http.route()
	def product(self, product, category='', search='', **kwargs):
		render = super(WebsiteSaleVendere, self).product(product, category, search, **kwargs)
		render.qcontext['math'] = math
		active_categ = product.public_categ_ids[0]
		categories = []

		parent = True
		while parent:
			categories.append(active_categ)
			if active_categ.parent_id:
				active_categ = active_categ.parent_id
			else:
				parent = False

		render.qcontext['categories'] = list(reversed(categories))
		return render



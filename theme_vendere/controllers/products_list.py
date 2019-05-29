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

	@http.route([
		'''/shop''',
		'''/shop/page/<int:page>''',
		'''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>''',
		'''/shop/category/<model("product.public.category", "[('website_id', 'in', (False, current_website_id))]"):category>/page/<int:page>''',
		'''/shop/tag/<int:tag_id>''',
		'''/shop/tag/<int:tag_id>/page/<int:page>'''
	])
	def shop(self, page=0, category=None, search='', ppg=PPG, show_list=False, tag_id=False, **post):
		if show_list:
			post['show_list'] = True
		render = super(WebsiteSaleVendere, self).shop(page, category, search, PPG, **post)
		post['context'] = {'website_sale_stock_get_quantity': True}

		# IDENTIFY WEBSITE THEME
		website_id = request.env.context['website_id']
		theme_id = request.env['website'].browse(website_id).theme_id.id
		theme_name = request.env['ir.module.module'].sudo().browse(theme_id).name

		if theme_name == 'theme_vendere':
			Products = request.env['product.template']

			render.qcontext['math'] = math

			if show_list:
				render.qcontext['show_list'] = True

			if tag_id:
				product_tag = request.env['product.template.tag'].browse(int(tag_id))
				url = "/shop/tag/%s" % product_tag.id
				product_count = len(Products.search([('meta_tags','in',int(tag_id))]))
				pager = request.website.pager(url=url, total=product_count, page=page, step=ppg, scope=7, url_args=post)
				tag_products = Products.search([('meta_tags','in',int(tag_id))], limit=ppg, offset=pager['offset'], order=self._get_search_order(post))
				render.qcontext['products'] = tag_products
				render.qcontext['pager'] = pager
				render.qcontext['tag'] = product_tag

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
							org_products = Products.search([('finish_id','=',org.id),('public_categ_ids','child_of',category.id)], order=self._get_search_order(post))
						else:
							org_products = Products.search([('ecommerce_tag','=',org.id),('public_categ_ids','child_of',category.id)], order=self._get_search_order(post))

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

	def _get_search_order(self, post):
		# OrderBy will be parsed in orm and so no direct sql injection
		# id is added to be sure that order is a unique sort key
		return 'is_published desc,%s , id desc' % post.get('order', 'website_sequence asc')

	@http.route()
	def product(self, product, category='', search='', **kwargs):
		render = super(WebsiteSaleVendere, self).product(product, category, search, **kwargs)
		render.qcontext['math'] = math
		active_categ = product.public_categ_ids[0] if len(product.public_categ_ids) else False
		categories = []

		parent = True
		if active_categ:
			while parent:
				categories.append(active_categ)
				if active_categ.parent_id:
					active_categ = active_categ.parent_id
				else:
					parent = False

		render.qcontext['categories'] = list(reversed(categories))
		return render

	def _get_search_domain(self, search, category, attrib_values):
		domain = super(WebsiteSaleVendere, self)._get_search_domain(search, category, attrib_values)
		if search:
			for s_index, srch in enumerate(search.split(" ")):
				insert_locations = []
				locations = list(ind for ind, val in enumerate(domain) if val == '|')
				for index,location in enumerate(locations):
					try:
						if locations[index + 1] - location > 1:
							insert_locations.append(location)
					except:
						insert_locations.append(location)
						break

				domain.insert(insert_locations[s_index] + 1, ('website_description', 'ilike', srch))
				domain.insert(insert_locations[s_index] + 1, ('ecommerce_tag.name', 'ilike', srch))
				domain.insert(insert_locations[s_index] + 1, ('finish_id.name', 'ilike', srch))
				domain.insert(insert_locations[s_index] + 1, '|')
				domain.insert(insert_locations[s_index] + 1, '|')
				domain.insert(insert_locations[s_index] + 1, '|')

		return domain




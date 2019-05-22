# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

from odoo.addons.website_sale_delivery.controllers.main import WebsiteSaleDelivery

class WebsiteDeliveryWarehouse(WebsiteSaleDelivery):

	def _update_website_sale_delivery(self, **post):
		result = super(WebsiteDeliveryWarehouse, self)._update_website_sale_delivery(**post)
		order = request.website.sale_get_order()
		carrier_id = int(post['carrier_id'])
		if order:
			carrier = request.env['delivery.carrier'].sudo().browse(carrier_id)
			if carrier.warehouse_id:
				order.sudo().warehouse_id = carrier.warehouse_id.id
		return result
# 			
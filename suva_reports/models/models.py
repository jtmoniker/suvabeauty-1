# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):

	_inherit = "sale.order"

	@api.model
	def _get_item_count(self):
		count = 0
		for line in self.order_line:
			if line.product_id.type != 'service':
				count += line.product_uom_qty

		return int(count)
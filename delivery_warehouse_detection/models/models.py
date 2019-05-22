# -*- coding: utf-8 -*-

from odoo import models, fields, api

class DeliveryCarrier(models.Model):

	_inherit = "delivery.carrier"

	warehouse_id = fields.Many2one('stock.warehouse', 'Default Warehouse')

class SaleOrder(models.Model):

	_inherit = "sale.order"

	@api.onchange('carrier_id')
	def _change_warehouse(self):
		if self.carrier_id:
			if self.carrier_id.warehouse_id and self.warehouse_id != self.carrier_id.warehouse_id:
				self.warehouse_id = self.carrier_id.warehouse_id.id
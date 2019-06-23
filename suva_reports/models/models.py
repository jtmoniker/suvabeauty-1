# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class SaleOrder(models.Model):

	_inherit = "sale.order"

	@api.model
	def _get_item_count(self):
		count = 0
		for line in self.order_line:
			if line.product_id.type != 'service':
				count += line.product_uom_qty

		return int(count)

class AccountInvoice(models.Model):

	_inherit = "account.invoice"

	@api.model
	def _get_invoice_so(self):
		so = self.env['sale.order'].sudo().search([('name','=',self.origin)], limit=1)
		return so


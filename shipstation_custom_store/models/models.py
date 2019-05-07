# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class SaleOrder(models.Model):
	_inherit = "sale.order"

	associated_write_date = fields.Date('Last Modified Date of Associated Documents')

	@api.model
	def _compute_shipstation_status(self):

		# COMPUTE SHIPSTATION ORDER STATUS

		# unpaid = If order isn't invoiced or has unpaid invoices.
		# paid = If order is fully invoiced and invoices are paid and all deliveries are assigned.
		# shipped = If all order lines have qty_delivered equal to product_uom_qty
		# cancelled = If order is in state 'cancel'
		# on_hold = If at least one delivery is unassigned.

		deliveries = self.env['stock.picking'].search([('sale_id','=',self.id)])
		invoices = self.invoice_ids

		if self.state == 'cancel':
			return 'cancelled'
		elif self.invoice_status == 'invoiced':
			for invoice in invoices:
				if invoice.state not in ['in_payment', 'paid', 'cancel']:
					return 'unpaid'

			undelivered = False
			for line in self.order_line:
				if not line.is_delivery and line.qty_delivered != line.product_uom_qty:
					undelivered = True

			if undelivered:
				unassigned = False
				for delivery in deliveries:
					if delivery.state != 'assigned' and delivery.state != 'cancel':
						unassigned = True
				if unassigned:
					return 'on_hold'
				else:
					return 'paid'

			else:
				return 'shipped'
		else:
			return 'unpaid'

class StockPicking(models.Model):
	_inherit = 'stock.picking'

	ss_carrier = fields.Char('Shipstation Carrier')
	ss_service = fields.Char('Shipstation Service')

	@api.multi
	def write(self, vals):
		res = super(StockPicking, self).write(vals)
		so = self.env['sale.order'].browse(self.sale_id.id)
		if len(so):
			so.sudo().write({
				'associated_write_date': datetime.now()
			})
		return res

class AccountInvoice(models.Model):
	_inherit = 'account.invoice'

	@api.multi
	def write(self, vals):
		res = super(AccountInvoice, self).write(vals)
		so = self.env['sale.order'].search([('name','=',self.origin)])
		if len(so):
			so.sudo().write({
				'associated_write_date': datetime.now()
			})
		return res


class SSCustomStore(models.Model):
	_name = "shipstation.custom.store"

	name = fields.Char('Custom Store Name', required=True)
	endpoint = fields.Char('Custom Store URL', readonly=True, compute='_generate_endpoint', store=True)
	username = fields.Char('Custom Store Username')
	password = fields.Char('Custom Store Password')

	_sql_constraints = [
		('scs_name',
		 'unique (name)',
		 'You already have a custom store with that name.')
	]

	@api.depends('name')
	def _generate_endpoint(self):
		if self.name:
			base_url = self.env['ir.config_parameter'].sudo().search([('key','=','web.base.url')]).value
			self.name = self.name.lower()
			self.endpoint = base_url + '/shipstation/' + self.name
		else:
			return False

class DeliveryCarrier(models.Model):
	_inherit = 'delivery.carrier'

	shipstation = fields.Boolean('Integrate with Shipstation', default=False)
	ss_custom_store = fields.Many2one('shipstation.custom.store', string="Shipstation Store")



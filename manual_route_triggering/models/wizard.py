# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError

class ManuelProcurement(models.Model):
	_name = "manual.procurement"

	product_id = fields.Many2one('product.product', string="Product", domain=[('bom_ids','>',0)])
	product_qty = fields.Integer('Quantity')

class ManualReorderingWizard(models.TransientModel):
	_name = "manual.procurement.wizard"
	_description = "Wizard: Quickly trigger inventory routes for selected products."

	name = fields.Char('Reference', required=True)
	location_id = fields.Many2one('stock.warehouse', string="Warehouse", required=True)
	picking_policy = fields.Selection([
		('direct', 'Deliver each product when available'),
		('one', 'Deliver all products at once')
	], 'Shipping Policy', default='direct', required=True, help='If you deliver all products at once, the delivery order will be scheduled based on the greatest product lead time. Otherwise, it will be based on the shortest.')
	manual_procurements = fields.Many2many(comodel_name='manual.procurement', string="Manual Procurement")

	@api.multi
	def run(self):
		if len(self.manual_procurements):
			procurement_group = self.env['procurement.group'].create({'name': self.name, 'move_type': self.picking_policy})
			warehouse = self.location_id
			location = self.location_id.view_location_id.child_ids.search([('usage','=','internal')], limit=1, order='id asc')
			for procurement in self.manual_procurements:
				values = {
					'company_id': self.env.user.company_id,
					'group_id': procurement_group,
					'route_ids': procurement.product_id.route_ids | procurement.product_id.categ_id.route_ids,
					'warehouse_id': warehouse
				}
				try:
					self.env['procurement.group'].run(procurement.product_id, procurement.product_qty, procurement.product_id.uom_id, location, procurement.product_id.name, self.name, values)
				except UserError as error:
					raise UserError(error.name)
			return True
		else:
			return False


		return True

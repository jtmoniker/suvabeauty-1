# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):

	_inherit = "product.template"

	# Overwrite Weight and Volume

	@api.one
	@api.depends('cm_length', 'cm_width', 'cm_height')
	def _compute_volume(self):
		volume = (self.cm_length / 100) * (self.cm_width / 100) * (self.cm_height / 100)
		self.volume = volume

	@api.one
	@api.depends('g_weight', 'lbs_weight')
	def _compute_weight(self):
		if self.weight_uom_name == 'kg':
			self.weight = self.g_weight / 1000
		else:
			self.weight = self.lbs_weight

	volume = fields.Float('Volume', help="The volume in m3.", compute="_compute_volume", store=True, digits=dp.get_precision('Stock Volume'))
	weight = fields.Float(
		'Weight', digits=dp.get_precision('Stock Weight'),
		help="Weight of the product, packaging not included. The unit of measure can be changed in the general settings",
		compute="_compute_weight", store=True)

	limited_edition = fields.Boolean('Limited Edition', default=False)
	country_of_origin = fields.Many2one('res.country', string='Country Of Origin')

	# Freight Density

	gml_density = fields.Float('g/ml', digits=(16,2))
	oz_density = fields.Float('oz/fl.oz', digits=(16,2))

	# Freight Dimensions

	cm_length = fields.Float('Length', digits=(16,2))
	cm_width = fields.Float('Width', digits=(16,2))
	cm_height = fields.Float('Height', digits=(16,2))
	in_length = fields.Float('Length', digits=(16,2))
	in_width = fields.Float('Width', digits=(16,2))
	in_height = fields.Float('Height', digits=(16,2))

	# Freight Weight

	g_weight = fields.Float('grams', digits=(16,2))
	oz_weight = fields.Float('ounces', digits=(16,2))
	lbs_weight = fields.Float('pounds', digits=(16,2))

	global_category = fields.Char('Global Category')
	global_subcategory = fields.Char('Global Subcategory')

class StockWarehouse(models.Model):
	_inherit = "stock.warehouse"
	_order = "sequence asc"

	sequence = fields.Integer('Sequence')

class DeliveryCarrier(models.Model):
	_inherit = "delivery.carrier"

	currency_id = fields.Many2one('res.currency', 'Currency')

	def fixed_rate_shipment(self, order):
		carrier = self._match_address(order.partner_shipping_id)
		if not carrier:
			return {'success': False,
					'price': 0.0,
					'error_message': _('Error: this delivery method is not available for this address.'),
					'warning_message': False}

		price = self.fixed_price

		if self.currency_id:
			if self.currency_id.id != order.currency_id.id:
				price = self.env['res.currency']._compute(self.currency_id, order.currency_id, price)
		elif self.company_id and self.company_id.currency_id.id != order.currency_id.id:
			price = self.env['res.currency']._compute(self.company_id.currency_id, order.currency_id, price)

		return {'success': True,
				'price': price,
				'error_message': False,
				'warning_message': False}



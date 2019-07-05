# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime

class SaleCouponProgram(models.Model):

	_inherit = "sale.coupon.program"

	def _check_promo_code(self, order, coupon_code):
		message = super(SaleCouponProgram, self)._check_promo_code(order, coupon_code)
		if 'error' in message and message['error'] == 'Promo code is expired':
			if self.rule_date_from and self.rule_date_to:
				if self.rule_date_from <= datetime.now() and datetime.now() <= self.rule_date_to:
					message.pop('error')
			elif self.rule_date_from and self.rule_date_from <= datetime.now():
				message.pop('error')
			elif self.rule_date_to and datetime.now() <= self.rule_date_to:
				message.pop('error')

		return message

	@api.model
	def _filter_on_validity_dates(self, order):
		return self.filtered(lambda program:
			program.rule_date_from and program.rule_date_to and
			program.rule_date_from <= datetime.now() and program.rule_date_to >= datetime.now() or
			not program.rule_date_from or not program.rule_date_to)


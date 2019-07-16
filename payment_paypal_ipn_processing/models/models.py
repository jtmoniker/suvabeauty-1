# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PaymentTransaction(models.Model):

	_inherit = 'payment.transaction'

	@api.multi
	def _set_transaction_done(self):
		super(PaymentTransaction, self)._set_transaction_done()
		if not self.is_processed:
			try:
				self._post_process_after_done()
				request.env.cr.commit()
			except Exception as e:
				_logger.exception("Transaction post processing failed:" + " " + e.message)
				request.env.cr.rollback()



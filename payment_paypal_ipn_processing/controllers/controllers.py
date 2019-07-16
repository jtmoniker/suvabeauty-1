# # -*- coding: utf-8 -*-
# import logging
# import pprint

# from odoo import http
# from odoo.http import request
# from odoo.addons.payment_paypal.controllers.main import PaypalController

# _logger = logging.getLogger(__name__)

# class PaypalController(PaypalController):

# 	@http.route('/payment/paypal/ipn/')
# 	def paypal_ipn(self, **post):
# 		""" Paypal IPN. """
# 		_logger.info('Beginning Paypal IPN form_feedback with post data %s', pprint.pformat(post))  # debug
# 		try:
# 			self.paypal_validate_data(**post)
# 		except ValidationError:
# 			_logger.exception('Unable to validate the Paypal payment')
# 		else:
# 			tx = request.env['payment.transaction'].search([('reference', '=', post.get('item_number'))])
# 			try:
# 				tx.sudo()._post_process_after_done()
# 				request.env.cr.commit()
# 			except Exception as e:
# 				_logger.exception("Transaction post processing failed:" + " " + e.message)
# 				request.env.cr.rollback()
# 				return ''
# 		return ''
# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from lxml import etree as ET
from datetime import datetime
import json

## Information required to pass to shipstation for each order.

##	ORDERS/ORDER
##		OrderID: Unique Order Identifier. (SO name)
##		OrderNumber: User-visible order number (same as Order ID.)
##		OrderDate: Create Date of the order. (SO create_date)
##		OrderStatus: Status of the order in Odoo. Can map status to Shipstating Status. (SO state)
##		LastModified: Last time the order was modified in your system. (SO update_date)
##		OrderTotal: Total amount of the order (SO total)
##		ShippingAmount: Cost of shipping.

##	ORDER/CUSTOMER
##		CustomerCode: Unique customer identifier (username/email address)
##		BillTo: Container node for billing information.
##			Name: Billing Name (SO partner_invoice_id.name)
##		ShipTo: Container ndoe for shipping information
##			Name: Recipients Name (SO partner_shipping_id.name)
##			Address1: Recipients Address Line 1 (SO partner_shipping_id.street)
##			City: Recipients City (SO partner_shipping_id.city)
##			State: For US/Canadian addresses (2 character code) (SO partner_shipping_id.state.code)
##			PostalCode: zip/postal (SO partner_shipping_id.zip)
##			Country: 2-char ISO 3116-1 country code. (SO partner_shipping_id.country_id.code)

##	ORDER/ITEMS
##		SKU: Unique identifier for line item. (SO order_line.product_id.default_code)
##		Name: Product name (SO order_line.product_id.name)
##		Quantity: Quantity of ordered items. (SO order_line.product_qty)
##		UnitPrice: Price of a single item. (SO order_line.price_unit

class ShipstationCustomStore(http.Controller):

	# Helper function | Append new element to the dynamically built xml request body.

	def _append_element(self, root, tag, value, cdata):
		element = ET.SubElement(root, tag)
		if value and cdata:
			element.text = ET.CDATA(str(value))
		elif value:
			element.text = str(value)
		elif isinstance(value, float):
			element.text = str(value)
		return root

	# Helper function | Format Odoo date fields to coincide with shipstation requirements.

	def _format_date(self, date):
		formatted_date = date.strftime("%m/%d/%Y %H:%M")
		return formatted_date

	def _generate_orderline_xml(self, line):
		root = ET.Element('Item')
		self._append_element(root, 'SKU', line.product_id.default_code, True)
		self._append_element(root, 'Name', line.product_id.name, True)
		self._append_element(root, 'Quantity', int(line.product_uom_qty), False)
		self._append_element(root, 'UnitPrice', line.price_unit, False)

		return root

	def _generate_shipstation_order_xml(self, order):
		root = ET.Element('Order')
		self._append_element(root, 'OrderID', order.id, True)
		self._append_element(root, 'OrderNumber', order.name, True)
		self._append_element(root, 'OrderDate', self._format_date(order.confirmation_date), False)
		self._append_element(root, 'OrderStatus', order._compute_shipstation_status(), True)
		self._append_element(root, 'LastModified', self._format_date(order.write_date), False)
		self._append_element(root, 'ShippingMethod', order.carrier_id.name, True)
		self._append_element(root, 'OrderTotal', order.amount_untaxed, False)
		self._append_element(root, 'ShippingAmount', order.delivery_price, False)
		self._append_element(root, 'Customer', False, False)
		self._append_element(root.find('./Customer'), 'CustomerCode', order.partner_id.email, True)
		self._append_element(root.find('./Customer'), 'BillTo', False, False)
		self._append_element(root.find('./Customer/BillTo'), 'Name', order.partner_invoice_id.name, True)
		self._append_element(root.find('./Customer'), 'ShipTo', False, False)
		self._append_element(root.find('./Customer/ShipTo'), 'Name', order.partner_shipping_id.name, True)
		self._append_element(root.find('./Customer/ShipTo'), 'Address1', order.partner_shipping_id.street, True)
		self._append_element(root.find('./Customer/ShipTo'), 'City', order.partner_shipping_id.city, True)
		self._append_element(root.find('./Customer/ShipTo'), 'State', order.partner_shipping_id.state_id.code, True)
		self._append_element(root.find('./Customer/ShipTo'), 'PostalCode', order.partner_shipping_id.zip, True)
		self._append_element(root.find('./Customer/ShipTo'), 'Country', order.partner_shipping_id.country_id.code, True)

		self._append_element(root, 'Items', False, False)

		for line in order.order_line:
			if line.product_id.type in ['consu', 'product']:
				item = self._generate_orderline_xml(line)
				root.find('./Items').append(item)

		return root

	def _generate_shipstation_xml(self, root, orders):

		for order in orders:
			add_order = self._generate_shipstation_order_xml(order)
			root.append(add_order)

	@http.route('/shipstation/<store>', type='http', auth='none', methods=['GET', 'POST'], csrf=None)
	def handler(self, action, store=None, **kwargs):
		
		SaleOrders = request.env['sale.order']
		DeliveryCarriers = request.env['delivery.carrier']
		CustomStores = request.env['shipstation.custom.store']
		BackOrder = request.env['stock.picking']

		username = kwargs.get('SS-UserName')
		password = kwargs.get('SS-Password')
		custom_store = CustomStores.sudo().search([('name','=',store)])

		if username and password and username == custom_store.username and password == custom_store.password:
			if action == 'export':
				delivery_carriers = DeliveryCarriers.sudo().search([('shipstation','=',True), ('ss_custom_store','=',custom_store.id)]).ids
				orders = SaleOrders.sudo().search([
					('state','in',['sale', 'cancel']),
					('write_date','>=',kwargs.get('start_date')),
					('write_date','<=',kwargs.get('end_date')),
					('carrier_id','in',delivery_carriers),
					('invoice_status','=','invoiced'),
					('delivery_count','>',0)
				])

				response_body = ET.Element('Orders')

				self._generate_shipstation_xml(response_body, orders)
				tree = ET.ElementTree(response_body)

				response = request.make_response(ET.tostring(tree, encoding="utf-8", method="xml", xml_declaration=True), {'Content-Type': 'text/xml'})
				response.status = '200'

				return response

			elif action == 'shipnotify':
				order = request.env['sale.order'].sudo().search([('name','=',kwargs.get('order_number'))])
				deliveries = request.env['stock.picking'].sudo().search([('sale_id','=',order.id),('state','=','assigned')])

				for delivery in deliveries:
					backorder = False
					for line in delivery.move_lines:
						line.sudo().quantity_done = line.reserved_availability
						if line.reserved_availability < line.product_uom_qty:
							backorder = True

					delivery.sudo().action_done()

					if backorder:
						BackOrder = request.env['stock.picking'].sudo().search([('backorder_id','=',delivery.id)])

					delivery.sudo().write({
						'ss_carrier': kwargs.get('carrier'),
						'ss_service': kwargs.get('service'),
						'carrier_tracking_ref': kwargs.get('tracking_number')
					})

					message = 'This order has been shipped via shipstation and automatically validated as a result. Carrier and tracking information are available in the Additional Info tab of the delivery record.'
					bo_message = 'This order was shipped via shipstation. However, not all products were available within Odoo at the time of validation and a backorder was created. This backordered delivery must be validated when inventory levels allow and a manual delivery confirmation email must be sent.'

					if len(BackOrder):
						for bo in BackOrder:
							bo.message_post(
								body='This delivery is a back order of a shipment that has already been shipped via shipstation.',
								subject='Backorder of Shipstation Delivery',
								subtype='shipstation_custom_store.mt_shipstation')

					delivery.message_post(
						body=bo_message if backorder else message,
						subject='Shipped Via Shipstation',
						subtype='shipstation_custom_store.mt_shipstation')

					order.message_post(
						body=bo_message if backorder else message,
						subject='Shipped Via Shipstation',
						subtype='shipstation_custom_store.mt_shipstation')


					if not backorder:
						delivery._send_shipstation_delivery_confirmation(delivery.id)

				response = request.make_response('Received Shipment Notification')
				response.status = '200'
				return response
				
		else:
			response = request.make_response('Authentication Failed. Your username and password combination is incorrect.')
			response.status = '401'
			return response

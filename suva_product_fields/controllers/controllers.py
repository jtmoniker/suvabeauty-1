# -*- coding: utf-8 -*-
from odoo import http

# class SuvaProductFields(http.Controller):
#     @http.route('/suva_product_fields/suva_product_fields/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/suva_product_fields/suva_product_fields/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('suva_product_fields.listing', {
#             'root': '/suva_product_fields/suva_product_fields',
#             'objects': http.request.env['suva_product_fields.suva_product_fields'].search([]),
#         })

#     @http.route('/suva_product_fields/suva_product_fields/objects/<model("suva_product_fields.suva_product_fields"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('suva_product_fields.object', {
#             'object': obj
#         })
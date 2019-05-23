# -*- coding: utf-8 -*-
from odoo import http

# class AccountTaxcloudRemoteOrigin(http.Controller):
#     @http.route('/account_taxcloud_remote_origin/account_taxcloud_remote_origin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_taxcloud_remote_origin/account_taxcloud_remote_origin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_taxcloud_remote_origin.listing', {
#             'root': '/account_taxcloud_remote_origin/account_taxcloud_remote_origin',
#             'objects': http.request.env['account_taxcloud_remote_origin.account_taxcloud_remote_origin'].search([]),
#         })

#     @http.route('/account_taxcloud_remote_origin/account_taxcloud_remote_origin/objects/<model("account_taxcloud_remote_origin.account_taxcloud_remote_origin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_taxcloud_remote_origin.object', {
#             'object': obj
#         })
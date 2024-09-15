# -*- coding: utf-8 -*-
# from odoo import http


# class AccountSerialNumber(http.Controller):
#     @http.route('/account_serial_number/account_serial_number', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/account_serial_number/account_serial_number/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('account_serial_number.listing', {
#             'root': '/account_serial_number/account_serial_number',
#             'objects': http.request.env['account_serial_number.account_serial_number'].search([]),
#         })

#     @http.route('/account_serial_number/account_serial_number/objects/<model("account_serial_number.account_serial_number"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('account_serial_number.object', {
#             'object': obj
#         })


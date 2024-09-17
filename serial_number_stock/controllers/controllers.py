# -*- coding: utf-8 -*-
# from odoo import http


# class StockSerialNumber(http.Controller):
#     @http.route('/stock_serial_number/stock_serial_number', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_serial_number/stock_serial_number/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_serial_number.listing', {
#             'root': '/stock_serial_number/stock_serial_number',
#             'objects': http.request.env['stock_serial_number.stock_serial_number'].search([]),
#         })

#     @http.route('/stock_serial_number/stock_serial_number/objects/<model("stock_serial_number.stock_serial_number"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_serial_number.object', {
#             'object': obj
#         })


# -*- coding: utf-8 -*-
# from odoo import http


# class KeyboardSubtree(http.Controller):
#     @http.route('/keyboard_subtree/keyboard_subtree/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/keyboard_subtree/keyboard_subtree/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('keyboard_subtree.listing', {
#             'root': '/keyboard_subtree/keyboard_subtree',
#             'objects': http.request.env['keyboard_subtree.keyboard_subtree'].search([]),
#         })

#     @http.route('/keyboard_subtree/keyboard_subtree/objects/<model("keyboard_subtree.keyboard_subtree"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('keyboard_subtree.object', {
#             'object': obj
#         })

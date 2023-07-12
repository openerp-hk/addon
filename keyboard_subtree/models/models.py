# -*- coding: utf-8 -*-

# from odoo import models, fields, api
#
#
# class keyboard_subtree(models.Model):
#     _name = 'keyboard.subtree'
#     _description = 'keyboard_subtree'
#
#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#     lines = fields.One2many(comodel_name='keyboard.subtree.line',inverse_name='res_model_id')
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
#
#
# class keyboard_subtree_line(models.Model):
#     _name = 'keyboard.subtree.line'
#     _description = 'keyboard_subtree_line'
#
#     res_model_id = fields.Many2one(comodel_name='keyboard.subtree',string='主表')
#     name = fields.Char()
#     data = fields.Integer()
#     data2 = fields.Float(compute="_value_pc", store=True)
#     data3 = fields.Text()
#     data4 = fields.Text()
#     data5 = fields.Text()


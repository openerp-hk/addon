# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class account_serial_number(models.Model):
#     _name = 'account_serial_number.account_serial_number'
#     _description = 'account_serial_number.account_serial_number'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100


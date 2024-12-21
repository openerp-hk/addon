# -*- coding: utf-8 -*-

from odoo import models, fields


class StockPickingExtend(models.Model):
    _inherit = 'stock.picking'

    priority = fields.Selection([
        ('0', 'To be arrange'), ('1', 'Normal'),
        ('2', 'Urgent'), ('3', 'To be confirm'),
        ('4', 'No label/PL'), ('5', 'delay')
    ], default='0', string="Priority")


class StockMove(models.Model):
    _inherit = "stock.move"

    priority = fields.Selection([
        ('0', 'To be arrange'), ('1', 'Normal'),
        ('2', 'Urgent'), ('3', 'To be confirm'),
        ('4', 'No label/PL'), ('5', 'delay')
    ], default='0', string="Priority")

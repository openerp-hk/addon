# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MenuIconData(models.Model):
    _name = 'menu.icon.data'
    _description = 'icon'
    _sql_constraints = [
        ('menu_id_uniq', 'unique (menu_id)', '重复配置!'),
    ]

    menu_id = fields.Many2one('ir.ui.menu', string='menu')
    icon_data = fields.Binary(string='icon')

    def sync_icon_data(self):
        for record in self:
            if record.icon_data:
                record.menu_id.web_icon_data = record.icon_data

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

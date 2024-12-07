# -*- coding: utf-8 -*-

from odoo import models, fields, api


class IrUiMenu(models.Model):
    _inherit = 'ir.ui.menu'

    def load_web_menus(self, debug):
        menus = super().load_web_menus(debug)
        config_parameter = self.env['ir.config_parameter'].sudo()
        menus['root']['system_logo'] = config_parameter.get_param('system_logo')
        menus['root']['nav_logo'] = config_parameter.get_param('nav_logo')
        return menus
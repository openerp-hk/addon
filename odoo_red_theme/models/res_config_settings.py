# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    system_logo = fields.Binary(string='System Logo')
    nav_logo = fields.Binary(string='Nav Logo')

    def get_values(self):
        result = super(ResConfigSettings, self).get_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        result.update({
            'system_logo': config_parameter.get_param('system_logo'),
            'nav_logo': config_parameter.get_param('nav_logo')
        })
        return result

    def set_values(self):
        result = super(ResConfigSettings, self).set_values()
        config_parameter = self.env['ir.config_parameter'].sudo()
        config_parameter.set_param('system_logo', self.system_logo)
        config_parameter.set_param('nav_logo', self.nav_logo)
        return result


from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'
    _description = "钉钉参数设置"

    ding_app_key = fields.Char('AppKey')
    ding_app_secret = fields.Char('AppSecret')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        set_param = self.env['ir.config_parameter'].set_param
        set_param('ding_app_key', (self.ding_app_key or '').strip())
        set_param('ding_app_secret', (self.ding_app_secret or '').strip())

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        res.update(
            ding_app_key=get_param('ding_app_key', default=''),
            ding_app_secret=get_param('ding_app_secret', default=''),
        )
        return res

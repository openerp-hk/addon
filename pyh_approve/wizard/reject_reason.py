# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class WizardRejectReason(models.TransientModel):
    _name = "pyh.reject.reason"

    record_id = fields.Integer(string="Reference ID",
                readonly=True, store=True, invisible=True, default=False)
    model_name = fields.Char(string=u"模型名称",
                readonly=True, store=True, invisible=True, default=False)
    note = fields.Text(string=u"退件原因")


    @api.multi
    def action_reject(self):
        self.ensure_one()
        if self.note == '':
            raise UserError(u"必须设置退件原因！")

        self.env[self.model_name].browse(self.record_id).pyh_action_reject(u"退件原因: %s" % self.note)
        return {'type': 'ir.actions.act_window_close'}

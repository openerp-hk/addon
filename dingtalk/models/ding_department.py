# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from dingtalk import SecretClient
from odoo import models, api
from odoo.exceptions import ValidationError


class Department(models.Model):
    _inherit = "hr.department"
    _description = "获取钉钉部门信息、并保存"

    def get_ding_client(self):
        get_param = self.env['ir.config_parameter'].sudo().get_param
        if get_param('ding_app_key', default='') == '':
            raise ValidationError("未设置智能电表参数！")
        if get_param('ding_app_secret', default='') == '':
            raise ValidationError("未设置智能电表参数！")

        client = SecretClient(
            get_param('ding_app_key', default=''),
            get_param('ding_app_secret', default='')
        )
        return client

    @api.model
    def action_dingding_department(self):
        departments = self.env["hr.department"].search([
            ("ding_id", "!=", False)
        ], limit=1)
        if departments:
            raise ValidationError("不能重复同步！")

        return self.recursion_get_department(1, 0)

    def recursion_get_department(self, parent_id, id):
        departments = self.get_ding_client().department.list(parent_id, 'zh_CN', False)
        for line in departments:
            department_info = self.env["hr.department"].create({
                "name": line.name,
                "complete_name": self.get_ding_client().department.get(line.parentid).name + "/" + line.name,
                "parent_id": 0 if id == 0 else id,
                "ding_id": line.id,
                "ding_parent_id": line.parentid
            })
            self.recursion_get_department(line.id, department_info.id)
        if len(departments) == 0:
            return {"state": 0}

    @api.multi
    def action_sync_department_to_dingding(self):
        self.ensure_one()
        department_data = {
            "name": self.name,
            "parentid": self.parent_id.ding_id if self.parent_id else 1
        }
        self.ding_id = self.get_ding_client().department.update(department_data) \
            if self.ding_id else self.get_ding_client().department.create(
            department_data)

    @api.multi
    def unlink(self):
        self.get_ding_client().department.delete(self.ding_id)
        return super(Department, self).unlink()


# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .ding_client import DingClient
from odoo import models, api
from odoo.exceptions import ValidationError


class Users(models.Model, DingClient):
    _inherit = "hr.employee"
    _description = "修改员工信息"

    @api.model
    def action_dingding_user(self):
        departments = self.env["hr.department"].search([
            ("ding_id", "!=", False)
        ])
        if not departments:
            raise ValidationError("请先同步部门信息！")
        employee = self.env["hr.employee"].search([
            ("open_id", "!=", False)
        ])
        if employee:
            raise ValidationError("不能重复同步！")

        array_tels = []
        for line in departments:
            user_list = DingClient.client.user.listbypage(line.ding_id)
            if user_list.get("errcode") != 0:
                raise ValidationError(user_list.get("errmsg"))
            array = []
            for user_info in user_list.get("userlist"):
                if user_info.mobile not in array_tels:
                    res_user_info = self.env["res.users"].create({
                        "login": user_info.mobile,
                        "password": "$pbkdf2-sha512$25000$LWUsZSzFeM8ZAwDAOKc0Bg$eoabqNRXPLQvvHhNAR1u2o.W.IXBuDW98qOgb/GF.gZqU5hrE3u8DEn4neJryIX53fEkBTruEpM/.4iFPxOMeA",
                        "active": True,
                        "name": user_info.name,
                        "company_id": self.env.user.company_id.id
                    })
                    array_tels.append(user_info.mobile)
                    array.append({"id": res_user_info.id, "tel": res_user_info.login})

                res_user_id = 0
                for item in array:
                    if user_info.mobile == item["tel"]:
                        res_user_id = item["id"]
                self.env["hr.employee"].create({
                    "name": user_info.name,
                    "ding_user_id": user_info.userid,
                    "user_id": res_user_id,
                    "mobile_phone": user_info.mobile,
                    "work_email": user_info.email,
                    "job_title": user_info.position,
                    "unionid": user_info.unionid,
                    "open_id": user_info.openId,
                    "avatar": user_info.avatar,
                    "department_id": line.id,
                    "children": 0
                })
            array.clear()
        array_tels.clear()

    @api.multi
    def action_sync_employee_to_dingding(self):
        self.ensure_one()
        user_data = {
            "name": self.name,
            "department": [self.department_id.ding_id],
            "mobile": self.mobile_phone,
            "tel": self.work_phone,
            "workPlace": self.work_location,
            "email": self.work_email
        }
        self.ding_user_id = DingClient.client.user.update(
            user_data) if self.ding_user_id else DingClient.client.user.create(user_data)

    @api.multi
    def unlink(self):
        if self.ding_user_id:
            DingClient.client.user.delete(self.ding_user_id)
        return super(Users, self).unlink()

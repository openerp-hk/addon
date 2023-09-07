# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from .ding_client import DingClient
from .date_utils import DateUtil
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class Attendance(models.Model, DingClient):
    _inherit = "hr.attendance"
    _description = "修改考勤"

    def ding_auto_attendance(self):
        pass
        # user_list = self.env["hr.employee"].search([
        #     ("ding_user_id", "!=", False)
        # ])
        # date_unit = DateUtil()
        # for line in user_list:
        #     attendance_info = DingClient.client.attendance.list(
        #         str(fields.Date.today()) + " 00:00:00",
        #         str(fields.Date.today()) + " 00:00:00",
        #         [line.ding_user_id]
        #     )
        #     if attendance_info.get("errcode") != 0:
        #         raise ValidationError(attendance_info.get("errmsg"))
        #
        #     if len(attendance_info.get("recordresult")) != 0:
        #         info = attendance_info.get("recordresult")[0]
        #         self.env["hr.attendance"].create({
        #             "ding_group_id": info.groupId,
        #             "ding_plan_id": info.planId,
        #             "ding_record_id": info.recordId,
        #             "ding_check_type": info.checkType,
        #             "ding_time_result": info.timeResult,
        #             "ding_location_result": info.locationResult,
        #             "ding_approve_id": info.approveId if info.approveId else 0,
        #             "ding_procinst_id": info.procInstId if info.procInstId else 0,
        #             "ding_source_type": info.sourceType,
        #             "ding_work_date": str(info.workDate),
        #             "ding_base_check_time": str(info.baseCheckTime),
        #             "ding_user_check_time": str(info.userCheckTime),
        #             "employee_id": line.id,
        #             "check_in": date_unit.timestamp_to_datetime(info.userCheckTime),
        #             "check_out": date_unit.timestamp_to_datetime(info.userCheckTime),
        #             "check_date": date_unit.timestamp_to_datetime(info.userCheckTime),
        #             "worked_hours": 0
        #         })


# -*- coding: utf-8 -*-

import odoo
from odoo import _, api, fields, models
from odoo import SUPERUSER_ID
from lxml import etree
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

import logging
_logger = logging.getLogger(__name__)

G_CHECK_TYPE = [
        ('serial', u'串行审核'),
        ('parallel', u'部门会审')]

# 审核单据
class ConfigApproveCheck(models.Model):
    _name = 'config.approve.check'
    _description = u'审核人配置'
    _rec_name = 'model_id'

    model_id = fields.Many2one('ir.model', u'表单', required=True)
    model_model = fields.Char(related='model_id.model', string=u'模型', readonly=True, store=True)
    check_line_ids = fields.One2many('config.check.line', 'check_id', string=u'审核列表')
    user_ids = fields.Many2many('res.users', 'fit_users', string=u"适用用户", required=True)  # 哪些用户使用该审核列表，适用多部门
    check_type = fields.Selection(G_CHECK_TYPE, default='serial', string=u'审核类型', required=True)
    active = fields.Boolean(u'有效', default=True, copy=False)


class ConfigCheckLine(models.Model):
    _name = 'config.check.line'
    _description = u'审核人配置明细'
    _order = "sequence"

    check_id = fields.Many2one('config.approve.check', u'审核人配置')
    user_id = fields.Many2one('res.users', u'审核人')
    sequence = fields.Integer(u'序号', default=1)

"""

发邮件

反审核处理流程，需要填写理由

<p>Hello,</p>
<p>The following email sent to %s cannot be accepted because this is a private email address.
   Only allowed people can contact us at this address.</p>
</div><blockquote>%s</blockquote>"% (message.get('to'), message_dict.get('body'))

    on_post_message: function (message) {
        var self = this;
        var options = this.selected_message ? {} : {channel_id: this.channel.id};
        if (this.selected_message) {
            message.subtype = this.selected_message.is_note ? 'mail.mt_note': 'mail.mt_comment';
            message.subtype_id = false;
            message.message_type = 'comment';
            message.content_subtype = 'html';

            options.model = this.selected_message.model;
            options.res_id = this.selected_message.res_id;

"""

class OrderCheckLine(models.Model):
    _name = 'order.check.line'
    _description = u'单据审核信息'

    order_id = fields.Many2one('pyh.approver', u'待审核单据')
    user_id = fields.Many2one('res.users', u'审核人', readonly=True)
    remark = fields.Char(u'备注', default=False)
    is_checked = fields.Boolean(u'已审核', default=False, readonly=True)
    check_dt = fields.Datetime(u'审核时间')
    show_button = fields.Boolean(u'当前审核', default=False)
    next_check_line = fields.Many2one('order.check.line', u'下一审核信息')
    model_name = fields.Char(u'数据模型', required=True)

    @api.multi
    def pyh_action_approve(self):
        for line in self:
            if self._uid == SUPERUSER_ID or line._uid == line.user_id.id:
                vals = {
                    'is_checked': True,
                    'check_dt': datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'show_button': False,
                }
                line.write(vals)

                order = self.env[self._context.get('target_model_name', 'pyh.approver')].browse(line.order_id.id)
                line.pyh_post_note_message(order, u"用户 %s 已审核" % line.user_id.name)
                if order.check_type == 'serial' and line.next_check_line:
                    line.next_check_line.show_button = True
                    line.pyh_send_mail_to_approve()

                # 审核完成
                if order.check_is_done():
                    order.set_main_process_complete()
            else:
                raise UserError(u"审核必须由本人操作！")

    #@api.multi
    def reset_state(self, order):
        check_type = order.check_type
        vals = {'is_checked': False, 
                'check_dt': False,
                'show_button': False if check_type == 'serial' else True}
        self.write(vals)

    @api.multi
    def pyh_action_reject(self, reason):
        self.ensure_one()
        order = self.env[self._context.get('target_model_name', 'pyh.approver')].browse(self.order_id.id)
        self.reset_state(order)
        order.set_main_process_draft()
        self.remark = u"%s;%s" % (self.remark, reason) if self.remark else reason
        self.pyh_post_note_message(order, reason)

    @api.multi
    def pyh_button_reject(self):
        self.ensure_one()
        if self._uid != SUPERUSER_ID and self._uid != self.user_id.id:
            raise UserError(u"审核必须由本人操作！")

        context = dict(self._context or {})
        context.update(
            {'active_model': self._name,
             'default_record_id': self.id,
             'default_model_name': self._name,
             })
        view_id = self.env.ref('pyh_approve.view_reject_reason_form').id
        return {
            'name': u'退件原因',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'pyh.reject.reason',
            'views': [(view_id, 'form')],
            'view_id': view_id,
            'target': 'new',
            'res_id': False,
            'context': context}

    #@api.multi
    def pyh_post_note_message(self, order, msg):
        """
        message subtype: mail.mt_note
        """
        order.message_post(body=msg, subtype='mail.mt_note')

    @api.multi
    def pyh_send_mail_to_approve(self):
        return
        for rec in self:

            # Mail body, changed from mail template
            body_html = u"""
<div style="padding:0px;width:600px;margin:auto;background: #FFFFFF repeat top /100%%;color:#777777">
    <table cellspacing="0" cellpadding="0" style="width:600px;border-collapse:collapse;background:inherit;color:inherit">
        <tbody><tr>
            <td valign="center" width="200" style="padding:10px 10px 10px 5px;font-size: 12px">
            </td>
        </tr></tbody>
    </table>
</div>
<div style="padding:0px;width:600px;margin:auto;background: #FFFFFF repeat top /100%%;color:#777777">
    <p>尊敬的 %s:</p>
    <p>&#160;&#160;&#160;&#160;系统用户提交了下列单据，需要您审核。</p>
    <p>请点击下列链接进入系统，然后进行相关的操作。</p>
    <div style="text-align: center; margin-top: 16px;">
        <a href="%s/web#id=%d&amp;view_type=form&amp;model=%s&amp;action=%d&amp;db=%s" style="padding: 5px 10px; font-size: 12px; line-height: 18px; color: #FFFFFF; border-color:#875A7B; text-decoration: none; display: inline-block; margin-bottom: 0px; font-weight: 400; text-align: center; vertical-align: middle; cursor: pointer; white-space: nowrap; background-image: none; background-color: #875A7B; border: 1px solid #875A7B; border-radius:3px">打开文件</a>
    </div>
    <p>如果该邮件不是您希望看到的，请忽略并联系系统管理员。</p>
</div>
<div style="padding:0px;width:600px;margin:auto; margin-top: 10px; background: #fff repeat top /100%%;color:#777777">
    <p>Thanks &amp; Best regards！</p>
    <p style="font-size: 11px; margin-top: 10px;">
        <strong>Sent by %s using <a href="www.odoo.com" style="text-decoration:none; color: #875A7B;">Odoo</a></strong>
    </p>
</div>
""" % (rec.user_id.name, self.env['ir.config_parameter'].get_param('web.base.url', default='http://localhost:8069'), \
       rec.order_id.id, self._context.get('target_model_name', 'pyh.approver'), self._context.get('params')['action'], self._cr.dbname, self.env.user.company_id.name)

            mail_values = {
                'email_from': 'System<%s>' % self.env.user.company_id.email,
                'email_to': rec.user_id.email,
                'subject': u"审核通知",
                'body_html': body_html,
                'notification': True,
            }
            self.env['mail.mail'].create(mail_values).send()

class PyhApprover(models.AbstractModel):
    _name = 'pyh.approver'
    _description = 'Pengyunhui Approver'
    """
    注意：
        1. hr 模块的单据需要另外考虑
          例如请假单，领导自己需要请假，自己审核自己的单据
        2. 下列模块数据可以由子类来修改
            _state_in_process： 审核中状态( state )
            _state_draft：如果单据被拒签，回到什么状态( state )
            _state_complete：如果签核完成，进入什么状态( state )
            _ignore_view_modify：设置为True时，本模块不对Form视图做修改(fields_view_get)
    """

    _approve_level = 5
    _state_complete = 'sale'
    _state_draft = 'draft'
    _state_in_process = 'to approve'
    #_new_fields_list = ('state_detail', 'appr_user_id')
    #_ignore_view_modify = False

    check_line_ids = fields.One2many('order.check.line', 'order_id', string=u'审核信息')
    check_type = fields.Selection(G_CHECK_TYPE, default='serial', string=u'审核类型')
    is_approved = fields.Boolean(string=u'是否已审核', default=False, copy=False)

    """
    set_main_process_start：提交审核
    set_main_process_complete：审核完成
    set_main_process_draft：退件重置
    可以被继承、覆盖
    """
    @api.multi
    def set_main_process_complete(self):
        self.write({'state': self._state_complete, 'is_approved': True})

    @api.multi
    def set_main_process_draft(self):
        self.write({'state': self._state_draft, 'is_approved': False})

    @api.multi
    def set_main_process_start(self):
        self.write({'state': self._state_in_process})

    def check_is_done(self):
        if all(line.is_checked for line in self.check_line_ids):
            return True
        else:
            return False

    # 提交审核
    @api.multi
    def pyh_start_approve_process(self):
        InstCheckLine = self.env['order.check.line']
        for rec in self:
            # 创建审核列表
            if not rec.check_line_ids:
                config_check = self.env['config.approve.check'].search([('model_model', '=', self._name),
                                       ('active', '=', True), ('user_ids', '=', self._uid)], limit=1)
                rec.check_type = config_check.check_type
                for line in config_check.check_line_ids:
                    rec.check_line_ids += InstCheckLine.create({
                                          #'order_id': rec.id,
                                          'user_id':line.user_id.id,
                                          'show_button': False if rec.check_type == 'serial' else True,
                                          'model_name': self._context.get('target_model_name', 'pyh.approver')})
            else:
                rec.check_line_ids.reset_state(self)

            if not rec.check_line_ids:
                rec.set_main_process_complete()
                continue

            if rec.check_type == 'serial':
                rec.check_line_ids[0].show_button = True
                rec.check_line_ids[0].pyh_send_mail_to_approve()
                check_len = len(rec.check_line_ids)
                if check_len > 1:
                    for i in range(check_len-1):
                        rec.check_line_ids[i].write({'next_check_line': rec.check_line_ids[i+1].id})
            else:
                for check_line in rec.check_line_ids:
                    check_line.pyh_send_mail_to_approve()

            # 设置状态
            rec.set_main_process_start()

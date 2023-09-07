# -*- encoding: utf-8 -*-

以 sale.order 举例

1. 首先在系统根据用户配置审核列表

2. 继承关系
class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'pyh.approver']

3. 对应状态覆盖
    _state_complete = 'sale'
    _state_draft = 'draft'
    _state_in_process = 'to approve'
	check_line_ids = fields.One2many(string=u'审核信息', domain=[('model_name', '=', _name)])

4. 修改审核完成之后的动作（审核完成之后，调用原始的 action_confirm）
    @api.multi
    def set_main_process_complete(self):
        self.action_confirm()
        return super(SaleOrder, self).set_main_process_complete()

5. 修改视图，添加审核页签
  a) 添加提交审核按钮，且按钮指定 target_model_name
  b) 添加审核列表
  c) 审核列表添加审核与退件按钮，且按钮指定 target_model_name

  <record id="view_sale_order_check_inherited" model="ir.ui.view">
    <field name="name">sale.order.form</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="context">{}</field>
    <field eval="18" name="priority"/>
    <field name="arch" type="xml">
      <button name="action_confirm" position="replace">
        <button name="pyh_start_approve_process" string="提交审核" type="object" context="{'target_model_name': 'sale.order'}"
                attrs="{'invisible':['|', ('state', '!=', 'draft')]}" class="oe_highlight"/>
      </button>
      <xpath expr="//page[last()-1]" position="after">
        <page string="审核信息" attrs="{'invisible':[('state', '!=', 'to approve')]}">
          <field name="check_line_ids" widget="one2many_list" attrs="{'readonly': [('state', '!=', 'draft')]}">
            <tree editable="bottom" options="{'reload_on_button': true}" create="0" delete="0">
              <field name="user_id"/>
              <field name="remark"/>
              <field name="is_checked"/>
              <field name="check_dt"/>
              <field name="active" invisible="1"/>
              <button name="pyh_action_approve" string="审核" type="object" context="{'target_model_name': 'sale.order'}"
                      attrs="{'invisible':[('active', '=', False)]}" class="oe_highlight"/>
              <button name="pyh_button_reject" string="退件" type="object" context="{'target_model_name': 'sale.order'}"
                      attrs="{'invisible':[('active', '=', False)]}" class="oe_highlight"/>
            </tree>
          </field>
        </page>
      </xpath>
    </field>
  </record>


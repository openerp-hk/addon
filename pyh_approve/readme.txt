# -*- encoding: utf-8 -*-

For example: sale.order 

1. First, in system settings, audits the list according to the user configuration.

2. Inherit Models
class SaleOrder(models.Model):
    _name = 'sale.order'
    _inherit = ['sale.order', 'pyh.approver']

3. Overwrite existing field
    _state_complete = 'sale'
    _state_draft = 'draft'
    _state_in_process = 'to approve'
	check_line_ids = fields.One2many(string=u'Information', domain=[('model_name', '=', _name)])

4. Set action for after approval （action_confirm）
    @api.multi
    def set_main_process_complete(self):
        self.action_confirm()
        return super(SaleOrder, self).set_main_process_complete()

5. Modify existing view, add proval page
  a) Add submit button，calls  'target_model_name'
  b) Add list
  c) Add aproval and exist button

  <record id="view_sale_order_check_inherited" model="ir.ui.view">
    <field name="name">sale.order.form</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="context">{}</field>
    <field eval="18" name="priority"/>
    <field name="arch" type="xml">
      <button name="action_confirm" position="replace">
        <button name="pyh_start_approve_process" string="Submit" type="object" context="{'target_model_name': 'sale.order'}"
                attrs="{'invisible':['|', ('state', '!=', 'draft')]}" class="oe_highlight"/>
      </button>
      <xpath expr="//page[last()-1]" position="after">
        <page string="Information" attrs="{'invisible':[('state', '!=', 'to approve')]}">
          <field name="check_line_ids" widget="one2many_list" attrs="{'readonly': [('state', '!=', 'draft')]}">
            <tree editable="bottom" options="{'reload_on_button': true}" create="0" delete="0">
              <field name="user_id"/>
              <field name="remark"/>
              <field name="is_checked"/>
              <field name="check_dt"/>
              <field name="active" invisible="1"/>
              <button name="pyh_action_approve" string="Approval" type="object" context="{'target_model_name': 'sale.order'}"
                      attrs="{'invisible':[('active', '=', False)]}" class="oe_highlight"/>
              <button name="pyh_button_reject" string="Reject" type="object" context="{'target_model_name': 'sale.order'}"
                      attrs="{'invisible':[('active', '=', False)]}" class="oe_highlight"/>
            </tree>
          </field>
        </page>
      </xpath>
    </field>
  </record>


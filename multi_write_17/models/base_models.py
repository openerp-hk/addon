# -*- coding: utf-8 -*-
import json
from lxml import etree

from odoo import models, fields, api

class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get('multi_write') and self.env.context.get('multi_write_model') == self._name:
            (self.browse(self.env.context.get('multi_write_ids')) - self
             ).with_context({'multi_write': False, 'multi_write_ids': []}).write(vals)
        return res

    def get_views_multi_write(self, views, options=None):
        result = super().get_views(views, options)
        result = self.del_multi_write_xml(result)
        return result

    def multi_write(self):
        pass

    def del_multi_write_xml(self, result):
        for view_type in result['views']:
            if view_type not in ['form']:
                continue
            view = result['views'][view_type]
            form_node = etree.fromstring(view['arch'])
            footer = form_node.xpath('footer')
            if not footer:
                footer = etree.Element('footer')
                button_confirm = etree.Element('button')
                button_confirm.set('name', 'multi_write')
                button_confirm.set('string', u'确认')
                button_confirm.set('class', 'btn-primary')
                button_confirm.set('type', 'object')
                button_confirm.set('confirm', '当前修改将同时运用于您选择的所有记录，您确认继续么？')
                footer.append(button_confirm)
                button_cancel = etree.Element('button')
                button_cancel.set('string', u'取消')
                button_cancel.set('special', 'cancel')
                footer.append(button_cancel)
                form_node.insert(-1, footer)
            view['arch'] = etree.tostring(form_node, encoding='unicode')
        return result

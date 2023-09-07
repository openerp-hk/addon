# -*- coding: utf-8 -*-
{
    'name': "DingDing Talk",

    'summary': """
        钉钉同步""",

    'description': """
        钉钉同步模块主要解决客户已经在使用钉钉协同工具与odoo的使用结合;可以在钉钉内打开odoo并同步组织架构及审批和消息以及考勤和请假等信息""",

    'author': "Openerphk Team",
    'website': "https://cdn.openerp.hk/en",
    'license': 'LGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'tools',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr', 'project', 'crm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ding_data.xml',
        'views/ding_params.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'qweb': [
    ],
    'images': ['static/description/openerp1.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': '1',
}

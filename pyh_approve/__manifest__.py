# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Multi Stage Approval',

    'summary': """
       Multi stage approval supported by OpenERP.HK.""",

    'description': """
        Multi Stage Approval & Countersign & Cross Department.""",

    'version': '14.0.1.0.0',
    'author': "Openerphk Team",
    'website': "https://cdn.odoo.red",
    'license': 'LGPL-3',
    #'maintainer': 'Pengyunhui',
    'category': 'Tools',
    'sequence': '1',
    
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/approve_config_view.xml',
        'wizard/reject_reason_view.xml',
    ],
    'qweb' : [
    ],
    'auto_install': False,
    'installable': True,
    'application': True,
    'images': ['static/description/icon.png'],
}

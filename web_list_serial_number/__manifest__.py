# -*- coding: utf-8 -*-
{
    'name': "web_list_serial_number",

    'summary': "Control the visibility of row numbers in list views",

    'description': """
     This add-on is a functional plug-in that allows users to control the visibility of row numbers in list views, tree views, and other similar views.
    """,

    'author': "Odoo.RED Team",
    'website': "https://cdn.odoo.red/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        # 'views/views.xml',
        # 'views/templates.xml',
    ],
    # only loaded in demonstration mode

    'assets': {
        'web.assets_backend': [
            "web_list_serial_number/static/src/views/list/*.*",
        ],
    },    
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/images/web.jpg'],
    'sequence': 1
}


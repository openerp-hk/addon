# -*- coding: utf-8 -*-
{
    'name': "Row numbers in Stock",

    'summary': "Control the visibility of row numbers in stock",

    'description': """
    This add-on is a functional plug-in that allows users to control the visibility of row numbers in the stock modules.
    """,


    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'author': "Odoo.RED team",
    'website': "https://cdn.odoo.red",
    'category': 'Extra Tools',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product', 'web_list_serial_number'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/serialNumberListView.xml',
    ],
    # only loaded in demonstration mode
    'assets': {
        'web.assets_backend': [
            "serial_number_stock/static/src/views/*/*.*",
        ],
    },
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/images/stock.jpg'],
    'sequence': 100
}


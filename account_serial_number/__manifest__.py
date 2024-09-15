# -*- coding: utf-8 -*-
{
    'name': "Row numbers in Account",

    'summary': "Control the visibility of row numbers in account",

    'description': """
    This add-on is a functional plug-in that allows users to control the visibility of row numbers in the accounting modules.
    """,

    'author': "Odoo.RED team",
    'website': "https://cdn.odoo.red",
    'category': 'Extra Tools',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'web_list_serial_number'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/serialNumberListView.xml',
    ],
    # only loaded in demonstration mode
    'assets': {
        'web.assets_backend': [
            "account_serial_number/static/src/views/*/*.*",
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/images/account.jpg'],
    'sequence': 100
}


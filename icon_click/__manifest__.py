# -*- coding: utf-8 -*-
{
    'name': "icon click",

    'summary': """
       This module allows the user to toggle the row icon with a single click, enabling easy status changes and quick visual identification of the row's state.""",

    'description': """
       To boost efficiency, this module allows users to toggle row icons with a single click, highlighting the status of the specific row for easier identification and management.
    """,

    'author': "Odoo.Red team",
    'website': "https://cdn.odoo.red/",

    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'stock_priority/static/src/views/**/*',
            'stock_priority/static/src/views/scss/fields.scss',
        ]
    },
    'application': True,
    'installable': True,
    'images': ['static/description/icon.gif'],
    'license': 'LGPL-3',
}

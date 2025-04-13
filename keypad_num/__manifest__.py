# -*- coding: utf-8 -*-
{
    'name': "keypad_num",

    'summary': """
        This widget provides a numerical keypad for on-screen clicking, allowing users to input digits without using a physical keyboard.""",

    'description': """
        This widget triggers a keypad, enabling users to input digits directly without the need for a physical keyboard.
    """,

    'author': "cdn.odoo.red",
    'website': "https://cdn.odoo.red/",

    'category': 'Extra Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'keypad_num/static/src/views/**/*',
        ]
    },
    'application': True,
    'installable': True,
    'images': ['static/description/icon.gif'],
    'license': 'LGPL-3',
}

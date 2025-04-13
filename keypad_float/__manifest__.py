# -*- coding: utf-8 -*-
{
    'name': "keypad_float",

    'summary': """
        This addon enables a keypad to pop up when interacting with an input field, allowing users to input digits without a physical keyboard. """,

    'description': """
       Automatic Keypad Popup: When the user moves the mouse over an input field, the keypad appears automatically.
       Easy Integration: Developers only need to add an extra option to the widget configuration to enable this functionality.
       Auto-hide Functionality: The keypad will hide itself when the mouse moves away from the input field.
       This feature improves usability on touch-screen devices or for users who prefer on-screen input options.
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
            'keypad_float/static/src/views/**/*',
        ]
    },
    'images': ['static/description/icon.gif'],
    'application': True,
    'installable': True,
    'license': 'LGPL-3',
}

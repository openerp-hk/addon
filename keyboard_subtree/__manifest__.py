# -*- coding: utf-8 -*-
{
    'name': "keyboard_subtree",

    'summary': """Orderline Keyboard""",

    'description': """
        This module adds a Keyboard Control function to the OrderLine. 
        Frees your hands from the mouse, boosts operation efficiency.  
    """,

    'author': "Josh.Feng, Openerp.HK, Odoo.Red, Odoo SA",
    'website': "https://cdn.odoo.red/""https://cdn.openerp.hk/",

    # Free your hands from the mouse!
    'category': 'Accounting',
    'version': '14.0.1',

    'depends': ['base'],

    'data': [
        'views/assets.xml',
        'views/templates.xml',
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
    'application': True,
    'sequence': '1',
    'license': 'LGPL-3',
    'images': ['static/description/images/keyboard_extension.png'],
    'installable': True,
    'auto_install': False,
}

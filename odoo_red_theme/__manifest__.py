# -*- coding: utf-8 -*-
{
    'name': "Enhance theme",

    'summary': "Enhance your theme experience",

    'description': """
     Custom themes tailored to signify your business needs can further enhance your operational efficiency.
    """,

    'author': "cdn.odoo.red",
    'website': "https://cdn.odoo.red/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Theme/Theme',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_config_settings.xml',
        'views/menu_icon_data.xml',
        'views/webclient.xml'
    ],
    # only loaded in demonstration mode
    "installable": True,
    "application": True,
    "auto_install": False,
    "sequence": 1,
    'price': 19.99,
    'currency': 'USD',
    'images': ['static/description/icon.gif'],
    'license': 'LGPL-3',
    'assets': {
        'web.assets_backend': [
            'openerphk_theme/static/src/webclient/default.scss',
            'openerphk_theme/static/src/webclient/navbar/*.*',
            'openerphk_theme/static/src/webclient/menu/*.*',
            'openerphk_theme/static/src/webclient/burger_menu/*.*',
            'openerphk_theme/static/src/webclient/*.*',
            'openerphk_theme/static/src/views/form/form_status_indicator/*.*',
            'openerphk_theme/static/src/views/form/*.*',
            'openerphk_theme/static/src/views/list/*.*',
            'openerphk_theme/static/src/views/fields/*.*',
            'openerphk_theme/static/src/search/control_panel/control_panel.xml',
        ],
        'web.assets_frontend': [
            'openerphk_theme/static/src/webclient/default.scss',
            'openerphk_theme/static/src/scss/*.*',
        ]
    },
}


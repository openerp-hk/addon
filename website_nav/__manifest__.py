# -*- coding: utf-8 -*-
{
    'name': 'website_nav',
    'description': 'Navbar Extension',
    'summary': 'To place a Navbar at the top left corner. '
               'Extend nav selections.',
    'category': 'Theme/eCommerce',
    'version': '16.0.1.0.0',
    'author': 'cdn.odoo.red',
    'company': 'cdn.odoo.red',
    'maintainer': 'odoo.red',
    'website': "https://cdn.odoo.red",
    'depends': [ 'website_sale', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/footer.xml',
        'views/header.xml',
        'views/layouts.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            "/website_nav/static/src/css/style.css",
            "/website_nav/static/src/css/indexstatic.css",
            "/website_nav/static/src/css/mobile.css",
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/theme_screenshot.png',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
    'auto_install': False,
}

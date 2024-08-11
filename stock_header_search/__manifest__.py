# -*- coding: utf-8 -*-
{
    'name': "Stock Move Date Filters",

    'summary': "Stock Move Date Filters",

    'description': """
    This add-on is a funtional plug-in that places a fixed filter bar for stock move list views. It expedites the record filtering process with only one single click.
    
    """,

    'author': "Odoo.RED team",
    'website': "https://cdn.odoo.red",
    'category': 'Extra Tools',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'stock_header_search/static/src/js/date_search.js',
            'stock_header_search/static/src/js/header_select_model.js',
            'stock_header_search/static/src/js/stock_picking_list.js',
            'stock_header_search/static/src/xml/header_select_model.xml',
            'stock_header_search/static/src/css/header_select_model.css',
        ]
    },
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': ['static/description/images/stock.jpg'],
    'sequence': 100
}

# -*- coding: utf-8 -*-
{
    'name': "field_required_styles",

    'summary': "Highlighting Required Fields",

    'description': """
            Odoo 17 Highlight the required field if it is not filled. Once the field is filled, the widget will revert the field name color back to normal.
    """,

    'author': "cdn.odoo.red",
    'website': "https://cdn.odoo.red/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Extra Tools',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'assets': {
        'web.assets_backend': [
            'field_required_styles/static/src/scss/field_required_style.scss',
            'field_required_styles/static/src/js/field_required_label.js',
            'field_required_styles/static/src/xml/field_required_label.xml'
        ],
    },

    'license': 'AGPL-3',
}

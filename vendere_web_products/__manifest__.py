# -*- coding: utf-8 -*-
{
    'name': "Ecommerce Product Management",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "JT Moniker",
    'website': "https://www.jtmoniker.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Ecommerce',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['website_sale', 'website_sale_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
}
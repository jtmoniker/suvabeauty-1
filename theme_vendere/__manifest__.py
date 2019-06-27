# -*- coding: utf-8 -*-
{
    'name': "Vendere Ecommerce Theme",

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
    'category': 'Theme/Retail',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'website_sale', 
        'website_sale_wishlist', 
        'website_sale_comparison', 
        'website_crm',
        'vendere_web_products',
        'ecommerce_product_reviews',
        'vendere_mega_menu',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'views/navbar-templates.xml',
        'views/footer-templates.xml',
        'views/products-templates.xml',
        'views/quickview-templates.xml',
        'views/product-templates.xml',
        'views/checkout-templates.xml',
        'views/wishlist.xml',
        'views/comparison.xml',
        'views/contact-page.xml',
        'views/views.xml',
        'views/snippets.xml',
        'views/options.xml',
    ],
}
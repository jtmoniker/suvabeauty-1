# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

{
    'name': 'Product Attribute Image',
    'version': '1.0',
    'summary': 'Show Image on website for product attribute',
    'category': 'eCommerce',
    'sequence': 1,
    'author': 'Synconics Technologies Pvt. Ltd.',
    'website': 'www.synconics.com',
    'description': """
Show Image on website for product attribute
=============================

""",
    'depends': ['website_sale'],
    'data' : [
        'views/product_attribute.xml',
        'views/template.xml',
    ],
    'images': [
        'static/description/main_screen.jpg',
    ],
    'price': 25,
    'currency': 'EUR',
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'OPL-1',
}

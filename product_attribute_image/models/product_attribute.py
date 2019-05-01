# -*- coding: utf-8 -*-
# Part of Odoo. See COPYRIGHT & LICENSE files for full copyright and licensing details.

from odoo import fields, models, _


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    type = fields.Selection(selection_add=[('image', 'Image')])
    link_to_product = fields.Boolean('Is this attribute linked to another product?', default=False)


class ProductAttributeValue(models.Model):
    _inherit = "product.attribute.value"

    image = fields.Binary("Image", attachment=True,
        help="This field holds the image used for the Attribute's value")
    linked_product = fields.Many2one('product.template', string="Linked Product")

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

# class SaleOrder(models.Model):

# 	_inherit = "sale.order.line"

# 	def _get_sale_order_line_multiline_description_variants(self):
# 		"""When using no_variant attributes or is_custom values, the product
# 		itself is not sufficient to create the description: we need to add
# 		information about those special attributes and values.

# 		See note about `product_no_variant_attribute_value_ids` above the field
# 		definition: this method is not reliable to recompute the description at
# 		a later time, it should only be used initially.

# 		:return: the description related to special variant attributes/values
# 		:rtype: string
# 		"""
# 		if not self.product_custom_attribute_value_ids and not self.product_no_variant_attribute_value_ids:
# 			return ""

# 		name = "\n"

# 		product_attribute_with_is_custom = self.product_custom_attribute_value_ids.mapped('attribute_value_id.attribute_id')

# 		# display the no_variant attributes, except those that are also
# 		# displayed by a custom (avoid duplicate)
# 		for no_variant_attribute_value in self.product_no_variant_attribute_value_ids.filtered(
# 			lambda ptav: ptav.attribute_id not in product_attribute_with_is_custom
# 		):
# 			if not no_variant_attribute_value.attribute_id.link_to_product:
# 				name += "\n" + no_variant_attribute_value.attribute_id.name + ': ' + no_variant_attribute_value.name

# 		# display the is_custom values
# 		for pacv in self.product_custom_attribute_value_ids:
# 			name += "\n" + pacv.attribute_value_id.attribute_id.name + \
# 				': ' + pacv.attribute_value_id.name + \
# 				': ' + (pacv.custom_value or '').strip()

# 		return name
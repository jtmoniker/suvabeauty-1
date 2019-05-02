# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductFinish(models.Model):

	_name = "product.finish"
	_order = "sequence asc"

	name = fields.Char('Finish')
	description = fields.Text('Finish Description')
	sequence = fields.Integer('Sequence')

class ProductTag(models.Model):

	_name = "product.template.tag"
	_order = "sequence asc"

	name = fields.Char('Tag Name')
	sequence = fields.Integer('Sequence')
	image = fields.Binary('Tag Image')

class ProductCategories(models.Model):

	_inherit = "product.public.category"

	featured_category = fields.Boolean('Featured Category', default=False)

class ProductTemplate(models.Model):

	_inherit="product.template"
	_order = "sequence asc"

	ecommerce_tag = fields.Many2one('product.template.tag', string="Ecommerce Tag", help="Product tag that can be used to sort a product on the product category page.")
	meta_tags = fields.Many2many('product.template.tag', string="Meta Tags", help="Product Tags that can be used to sort products into 'meta' categories which can be accessed via a meta mega menu.")
	finish_id = fields.Many2one('product.finish', string="Finish Type")

	website_long_description = fields.Html('Long Description', sanitize=False)
	product_instructions = fields.Html('Instructions', sanitize=False)

	featured_product = fields.Boolean('Featured Product', default=False)

	@api.model
	def _get_secondary_img(self):
		for img in self.product_image_ids:
			if img.is_secondary:
				return img.id

	def set_attribute_group(self):
		view = self.env.ref('vendere_web_products.product_attribute_group_wizard')
		wiz = self.env['product.attribute.group.wizard'].create({
			'product_tmpl_id': self.id
		})
		res = {
			'success': True,
			'name': ('Set Attributes From Group'),
			'type': 'ir.actions.act_window',
			'view_type': 'form',
			'view_mode': 'form',
			'res_model': 'product.attribute.group.wizard',
			'views': [(view.id, 'form')],
			'view_id': view.id,
			'target': 'new',
			'res_id': wiz.id,
			'context': self.env.context,
		}
		return res

class ProductImage(models.Model):

	_inherit = 'product.image'

	is_secondary = fields.Boolean('Hover Image?')

class AttributeGroups(models.Model):

	_name = "product.attribute.group"
	_description = "Group attribute values within a particular attribute to easily apply like-combinations of attribute values to a product"

	name = fields.Char('Group Name')
	attribute_id = fields.Many2one('product.attribute', string="Attribute")
	attribute_value_ids = fields.Many2many('product.attribute.value', string="Attribute Values")

	@api.onchange('attribute_id')
	def update_values(self):
		return {'domain': {'attribute_value_ids': [('attribute_id','=',self.attribute_id.id)]}}

class SetAttributesGroup(models.TransientModel):

	_name = "product.attribute.group.wizard"

	product_tmpl_id = fields.Many2one('product.template', string="Product")
	attribute_group_id = fields.Many2one('product.attribute.group', string="Attribute Group")

	def set_attributes(self):
		if self.attribute_group_id:
			self.env['product.template.attribute.line'].create({
				'attribute_id': self.attribute_group_id.attribute_id.id,
				'product_tmpl_id': self.product_tmpl_id.id,
				'value_ids': [(6, 0, self.attribute_group_id.attribute_value_ids.ids)]
			})
			return True
		else: 
			return {
				'type': 'ir.actions.do_nothing'
			}




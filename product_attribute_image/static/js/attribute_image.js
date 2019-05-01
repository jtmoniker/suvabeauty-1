odoo.define('product_attribute_image.image_attribute', function(require) {

	require('web.dom_ready');

	$('ul.image_attrs > li').mouseenter(function(e) {
		var name = e.currentTarget.dataset.name;
		var tar = $(e.currentTarget.parentNode.parentNode.firstElementChild.nextElementSibling)
		tar.text(" " + name)
	});	

});
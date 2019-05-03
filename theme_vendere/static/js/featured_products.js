odoo.define('theme_vendere.featuredProducts', function(require) {

	require("web.dom_ready");
	var rpc = require('web.rpc');

	var products = []

	var $slides = $('.featured-products-container').find('li');
	$slides.each(function(idx, li) {
    	product_id = $(li).data()['product'];
    	products.push(product_id);
	});

	if (products.length) {
		rpc.query({
			model: 'product.template',
			method: 'update_featured_products',
			args: [products],
		}).then(function(data) {
			$slides.each(function(idx, li) {
				product_id = $(li).data()['product'];
		    	$(li).find('span.fp-price .oe_currency_value').text(data[product_id]['price'].toFixed(2))
			});
		});
	}
})
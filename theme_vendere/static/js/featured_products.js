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
		$.ajax({
			url: `/pricelist`,
			method: 'GET',
		}).then((webData) => {
			website = JSON.parse(webData);
			rpc.query({
				model: 'product.template',
				method: 'update_featured_products',
				args: [products, website['id']],
			}).then(function(data) {
				$slides.each(function(idx, li) {
					product_id = $(li).data()['product'];
			    	$(li).find('span.fp-price .oe_currency_value').text(data[product_id]['price'].toFixed(2))
				});
			});
		});
	}
})
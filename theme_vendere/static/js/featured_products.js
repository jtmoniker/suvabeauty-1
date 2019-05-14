odoo.define('theme_vendere.featuredProducts', function(require) {

	require("web.dom_ready");
	var rpc = require('web.rpc');

	var products = []

	var $featuredBlock = $('section.featured-products-section');

	if ($featuredBlock.length) {
		$featuredBlock.each(function(idx, block) {
			$.ajax({
				url: `/shop/products/featured`,
				method: "GET",
			}).then(function(html) {
				var el = $.parseHTML(html);
				$(block).html(el[1].innerHTML);
			}).then(function() {
				$('.featured-products-container').lightSlider({
					item: 5,
					autoWidth: true,
					pager: false,
				})
			});
		});
	}
})
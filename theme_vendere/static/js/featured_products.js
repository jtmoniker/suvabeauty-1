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
				var $models = $('.featured-products-section').find('[data-oe-model]');
				$models.each(function(idx, model) {
					$(model).removeAttr("data-oe-model data-oe-field data-oe-id data-oe-xpath");
				});
				$('.featured-products-container').lightSlider({
					item: 5,
					autoWidth: true,
					pager: false,
				})
			});
		});
	}
})
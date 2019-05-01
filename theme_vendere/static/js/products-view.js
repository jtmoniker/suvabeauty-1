odoo.define('vendere.Products', function(require) {

	require('web.dom_ready');
	var rpc = require('web.rpc');

	$('button.grid-view').on('click', (e) => {
		window.location.href = window.location.pathname;
	});

	$('button.list-view').on('click', (e) => {
		window.location.href = window.location.pathname + '?show_list=1';
	});

	$('div.prod-img > a').hover(function(e) {
		if (e.currentTarget.firstElementChild.dataset.secondary) {
			var $el = $(e.currentTarget.firstElementChild);
			var secondary = e.currentTarget.firstElementChild.dataset.secondary;
			$el.attr("src", `/website/image/product.image/${secondary}/image`);
		}
	}, function(e) {
		var $el = $(e.currentTarget.firstElementChild);
		var primary = e.currentTarget.firstElementChild.dataset.primary;
		$el.attr("src", `/website/image/product.template/${primary}/image`);
	});

});
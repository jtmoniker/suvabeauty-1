odoo.define('vendere.Products', function(require) {

	require('web.dom_ready');
	var rpc = require('web.rpc');

	$('button.grid-view').on('click', (e) => {
		var href = window.location.href
		var url_parts = href.split('?')
		if (url_parts.length >= 2) {
			var url_base = url_parts.shift();
			var queryString = url_parts.join('?');
			var prefix = 'show_list=';
			var parts = queryString.split(/[&;]/g);

			for (var i = 0; i < parts.length; i++) {
				if (parts[i].indexOf(prefix) >= 0) {
					parts.splice(i, 1);
				}
			}

			url = url_base + '?' + parts.join('&');
			window.location.href = url;

		}
	});

	$('button.list-view').on('click', (e) => {
		var arg_indicator = window.location.href.indexOf("?");
		var show_exists = window.location.href.indexOf("show_list");
		if (arg_indicator < 0 ) {
			window.location.href = window.location.href + '?show_list=1';
		} else {
			if (show_exists < 0) {
				window.location.href = window.location.href + '&show_list=1';
			}
		}
		
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
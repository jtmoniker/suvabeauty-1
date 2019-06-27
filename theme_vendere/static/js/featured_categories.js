odoo.define('theme_vendere.featuredCategories', function(require) {
	'use strict';

	var options = require('web_editor.snippets.options');
	var rpc = require('web.rpc')

	options.registry.featured_category_options = options.Class.extend({
		onBuilt: function() {

			var domain_fragments = window.location.href.split('/')
			var domain = domain_fragments[0] + '//' + domain_fragments[2];

			return this._rpc({
				model: 'product.public.category',
				method: 'get_featured_categs',
				args: [],
			}).then(function(categories) {
				categories.forEach(function(category) {
					var url = `${domain}/web/image?model=product.public.category&id=${String(category.id)}&field=image`;
					var html = `
						<div class="col-lg-6 col-md-6 col-sm-6 col-xs-12 categ-box"> 
							<a href="${domain}/shop/category/${String(category.id)}">
								<img src="${domain}/website/image/product.public.category/${category.id}/image" class="img img-fluid"/>
							</a>
							<h2>${category.name}</h2>
							<a class="btn" href="${domain}/shop/category/${String(category.id)}">
								Shop Now
							</a>
						</div>`;
					$('.featured-categ-container').append(html);
				});
			});
		}
	});
});
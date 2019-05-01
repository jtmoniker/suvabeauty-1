odoo.define('theme_vendere.featuredProducts', function(require) {

	var options = require('web_editor.snippets.options');
	var rpc = require('web.rpc');

	options.registry.featured_products_options = options.Class.extend({
		onBuilt: function() {
			var domain_fragments = window.location.href.split('/');
			var domain = domain_fragments[0] + '//' + domain_fragments[2];

			return this._rpc({
				model: 'product.template',
				method: 'get_featured_products',
				args: [],
			}).then(function(products) {
				products.forEach(function(product) {
					var val_integer = Math.floor(product.rating);
					var val_decimal = product.rating - val_integer;
					var empty_star = 5 - (val_integer + Math.ceil(val_decimal));
					var rating_html = "";
					if (val_integer) {
						for (i = 0; i < val_integer; i++) {
							rating_html += `<i style="font-size: 1.2em;" class="fa fa-star" role="img" aria-label="One star" title="One star"></i>`;
						}
					}
					if (val_decimal) {
						rating_html += `<i style="font-size: 1.2em;" class="fa fa-star-half-o" role="img" aria-label="Half a star" title="Half a star"></i>`;
					}
					for (i = 0; i < empty_star; i++) {
						rating_html += `<i style="font-size: 1.2em;" class="fa fa-star-o"></i>`;
					}
					var html = `
						<li>
							<div class='slider-prod'>
								<div class="slide-img">
									<a href="${domain}/shop/product/${product.id}">
										<img class="img img-fluid rounded" src="${domain}/website/image/product.template/${product.id}/image" data-secondary="${product.secondary_img}" data-primary="${product.id}"/>
									</a>
								</div>
								<div class="slide-content">
									<h6 class="prod-categ">${product.category}</h6>
									<h5 class="prod-name">${product.name}</h5>
									<div itemprop="offers" itemscope="itemscope" itemtype="http://schema.org/Offer" class="product_price">
										<b>
											<span class="fp-price">$${product.price}</span>
											<span itemprop="price" style="display:none;">${product.price}</span>
											<div class="o_website_rating_static">
												<span>${rating_html}</span><span style="color: black"> (${product.rating_count})</span>
											</div>
										</b>
										<div class="slide-action">
											<a href="${domain}/shop/product/${product.id}" role="button" class="btn btn-secondary btn-sm a-submit" aria-label="Shopping cart" title="Shopping cart">
												<i class="fa fa-shopping-bag"></i><span>Add To Cart</span>
											</a>
											<a type='button' class="quickview" data-product-id="${product.id}">
												<i class="fa fa-eye"></i>
											</a>
										</div>
									</div>
								</div>
							</div>
						</li>`;
					$('.featured-products-container').append(html);
				});
			});
		}
	});
});
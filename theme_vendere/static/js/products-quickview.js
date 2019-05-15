odoo.define('vendere.quickView', function(require) {

	require('web.dom_ready');

	var rpc = require('web.rpc')

	$(document).on('click', 'a.quickview', (e) => {
		var productId = e.currentTarget.dataset.productId;
		$.ajax({
			url: `/shop/product/quickview/${productId}`,
			method: 'GET',
		}).then((data) => {
			var product = JSON.parse(data)

			// SET PRODUCT IMAGE CAROUSEL
	    	$('#quickview_img').html(`
	    		<div id="o-carousel-product" class="carousel slide" data-ride="carousel" data-interval="0">
	    			<div class="carousel-outer">
	    				<div class="carousel-inner">
	    					<div id="template_${productId}" class="carousel-item active">
	    						<img src="/web/image/product.template/${productId}/image" class="img img-fluid roduct_detail_img" data-zoom-image>
	    					</div>
	    				</div>
	    			</div>
	    			<ol class="carousel-indicators">
	    				<li data-type="template" data-id="${productId}" class="active">
	    					<img class="img img-fluid" src="/website/image/product.template/${productId}/image/90x90">
	    				</li>
	    			</ol>
	    		</div>
	    	`)
	    	if (product['images'].length) {
	    		for (image_id of product['images']) {
		    		$('#quickview_img div.carousel-inner').append(`
		    			<div id="image_${image_id}" class="carousel-item">
		    				<img src="/web/image/product.image/${image_id}/image" class="img img-fluid product_detail_img" data-zoom-image>
		    			</div>
		    		`)
		    		$('#quickview_img ol.carousel-indicators').append(`
		    			<li data-type="image" data-id="${image_id}">
		    				<img class="img img-fluid" src="/website/image/product.image/${image_id}/image/90x90">
		    			</li>
		    		`)
		    	}
	    	}

	    	var addToCartHtml = `<input class="btn btn-primary" value="SOLD OUT">`;
	    	if (product['availability'] == 'never' || product['availability'] == 'custom' || product['availability'] == 'always' && product['virtual_available'] > 0 || product['availability'] == 'threshold' && product['virtual_available'] >= product['threshold']) { 
	    		addToCartHtml = `<input class="btn btn-primary" type="submit" value="ADD TO CART">`;
	    	}

	    	// SET PRODUCT CONTENT
	    	$('#quickview_content').html(`
	    		<h2>${product['name']}</h2>
	    		<h3>$${product['price']}</h2>
	    		<h4>${product['category']}</h3>
	    		<br/>
	    		<div class="description">
	    			${product['description'] ? product['description'] : ''}
	    		</div>
	    		<br/>
	    		<div class="content-footer">
	    			<a href="/shop/product/${productId}">
	    				<span>View full product details</span><span>&rarr;</span>
	    			</a>
		    		<hr/>
		    		<form action="/shop/cart/update" method="POST">
		    			<div class="quickview_update_cart_content">
		    				<input type="hidden" name="csrf_token" value="${product['token']}" />
                            <input type="hidden" class="product_id" name="product_id" value="${product['variant']}" />
                            <input type="hidden" class="product_template_id" name="product_template_id" value="${productId}" />
		    				<label>Quantity</label>
		    				<input id="quickview_cart_qty" min="1" type="number" name="add_qty" value="1">
		    				${addToCartHtml}
			  			</div>
			  		</form>
		  		</div>
	    	`)

	    }).then(() => {
	    	$('#quickview_modal').modal('show');
	    });
	});

	$(document).on('click', '#quickview_modal ol.carousel-indicators li', function(e){
	    var type = e.target.parentElement.dataset.type;
	    var id = e.target.parentElement.dataset.id;
	    $('#quickview_img div.carousel-inner div.active').removeClass('active');
	    $(`#quickview_img div.carousel-inner div#${type}_${id}`).addClass('active');
	    $('ol.carousel-indicators li.active').removeClass('active');
	    $(e.target.parentElement).toggleClass('active');
	});
});
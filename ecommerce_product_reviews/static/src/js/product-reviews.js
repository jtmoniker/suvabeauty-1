odoo.define('ecommerce_product_reviews.reviews', function(require) {

	require('web.dom_ready');
	rpc = require('web.rpc');

	var totalPages = 1
	if ($('#reviews-pager').length) {
		totalPages = $('#reviews-pager').data()['total'];
	}
	var $productID = $('input.product_template_id').val();

	$('#reviews-next').on('click', (e) => {
		e.preventDefault();
		var $activePage = $('#reviews-pager > a.active');
		var currentPage = $activePage.data()['page'];
		var $pagerElements = $('#reviews-pager').children();

		$.ajax({
			url: `/shop/product/${$productID}/reviews/page`,
			method: "GET",
			data: {
				'page': currentPage,
				'direction': 'next',
			},
		}).then(function(html) {
			$('#reviews-body').replaceWith(html);
			$activePage.toggleClass('active');
			$activePage.next().toggleClass('active');
			$('#reviews-prev').removeClass('inactive');
			if (currentPage == totalPages - 1) {
				$('#reviews-next').addClass('inactive');
			}

			// Handle Dynamic Reviews Pager on 'Next' Click.

			if (totalPages > 10) {
				if (currentPage == 1 && !$('span.first-separator').length || !$('span.first-separator').length) {
					$($pagerElements[0]).after("<span class='first-separator'>...</span>");
				}
				if ($activePage.next().hasClass('last-separator') || $activePage.next().hasClass('first-separator')) {
					var pagerElements = [];
					for (var i = currentPage; i < currentPage + 9; i++) {
						if (i == currentPage + 1) {
							pagerElements.push(`
								<a href="#" class="review-pager active" data-page="${i}">
	                                ${i}
	                            </a>
							`)
						} else if (i < totalPages && i != 1) {
							pagerElements.push(`
								<a href="#" class="review-pager" data-page="${i}">
	                                ${i}
	                            </a>
							`)
						} else if (i == totalPages) {
							$('span.last-separator').remove();
							pagerElements.push(`
								<a href="#" class="review-pager" data-page="${i}">
	                                ${i}
	                            </a>
							`)
						}
					}
					$("span.first-separator").nextUntil("span.last-separator").remove();
					$("span.first-separator").after(pagerElements.join("\n"));
				}
			}
		}).then(function() {
			$("HTML, BODY").animate({
				scrollTop: $('div#product_reviews').offset().top - 100
			}, 500);
		});
	});

	$('#reviews-prev').on('click', (e) => {
		e.preventDefault();
		var $activePage = $('#reviews-pager > a.active');
		var currentPage = $activePage.data()['page'];
		var $pagerElements = $('#reviews-pager').children();
		$.ajax({
			url: `/shop/product/${$productID}/reviews/page`,
			method: "GET",
			data: {
				'page': currentPage,
				'direction': 'prev',
			},
		}).then(function(html) {
			$('#reviews-body').replaceWith(html);
			$activePage.toggleClass('active');
			$activePage.prev().toggleClass('active');
			$('#reviews-next').removeClass('inactive');
			if (currentPage == 2) {
				$('#reviews-prev').addClass('inactive');
			}
		}).then(function() {
			$("HTML, BODY").animate({
				scrollTop: $('div#product_reviews').offset().top - 100
			}, 500);
		});

		// Handle Dynamic Reviews Pager on 'Prev' Click.

		if (totalPages > 10) {
			if (currentPage == 2) {
				$(".first-separator").remove();
			}
			if ($activePage.prev().hasClass('first-separator') || $activePage.prev().hasClass('last-separator')) {
				if (!$('span.last-separator').length) {
					$($pagerElements[$pagerElements.length - 1]).before("<span class='last-separator'>...</span>");
				}

				var pagerElements = []
				for (var i = currentPage - 8; i <= currentPage; i++) {
					if (i == currentPage - 1) {
						pagerElements.push(`
							<a href="#" class="review-pager active" data-page="${i}">
	                            ${i}
	                        </a>
						`)
					} else if (i > 1 && i != totalPages) {
						pagerElements.push(`
							<a href="#" class="review-pager" data-page="${i}">
	                            ${i}
	                        </a>
						`)
					}
				}
				$("span.first-separator").nextUntil("span.last-separator").remove();
				$("span.last-separator").before(pagerElements.join("\n"));
			}
		}
	});

	$(document).on('click', 'a.review-pager', (e) => {
		e.preventDefault();
		if ($(e.currentTarget).hasClass('active')) {
			return false;
		} else {
			var $activePage = $('#reviews-pager > a.active');
			var $pagerElements = $('#reviews-pager').children();
			var $newPage = $(e.currentTarget);
			var newPage = $newPage.data()['page'];
			$.ajax({
				url: `/shop/product/${$productID}/reviews/page`,
				method: "GET",
				data: {
					'page': newPage,
					'direction': 'direct',
				},
			}).then(function(html) {
				$('#reviews-body').replaceWith(html);
				$activePage.removeClass('active');
				$newPage.addClass('active');
				if (newPage == 1) {
					$('#reviews-prev').addClass('inactive');
					$('#reviews-next').removeClass('inactive');
				} else if (newPage == totalPages) {
					$('#reviews-next').addClass('inactive');
					$('#reviews-prev').removeClass('inactive');
				} else {
					$('#reviews-prev').removeClass('inactive');
					$('#reviews-next').removeClass('inactive');
				}
			}).then(function() {
				$("HTML, BODY").animate({
					scrollTop: $('div#product_reviews').offset().top - 100
				}, 500);
			});

			if (totalPages > 10) {
				if (newPage == totalPages && !$('span.first-separator').length) {
					$($pagerElements[0]).after("<span class='first-separator'>...</span>");
				} else if (newPage == 1 && !$('span.last-separator').length) {
					$($pagerElements[$pagerElements.length - 1]).before("<span class='last-separator'>...</span>");
				}
			}
		}
	});

	$('a#review-write-btn').on('click', (e) => {
		e.preventDefault();
		$('div#review-form').toggleClass('d-none');
	});

	$(document).on('mouseenter', 'div#review-form-rating i', (e) => {
		var $target = $(e.currentTarget);
		$target.addClass('fa-star hovered').removeClass('fa-star-o');
		$target.prevAll().addClass('fa-star included').removeClass('fa-star-o');
	});

	$(document).on('mouseleave', 'div#review-form-rating i', (e) => {
		var $target = $(e.currentTarget);
		$target.removeClass('hovered');
		if (!$target.hasClass('selected')) {
			$target.prevAll().removeClass('fa-star included').addClass('fa-star-o');
			$target.removeClass('fa-star').addClass('fa-star-o');
		} 
	});

	$(document).on('click', 'div#review-form-rating i', (e) => {
		var $target = $(e.currentTarget);
		$target.siblings('.selected').removeClass('selected');
		$target.siblings('.included').removeClass('included');
		$target.siblings('.fa-star').removeClass('fa-star').addClass('fa-star-o');
		$target.addClass('fa-star selected').removeClass('fa-star-o');
		$target.prevAll().addClass('fa-star').removeClass('fa-star-o');
	});

	function newReview(values, emailRegEx, productID) {
		if ($('#review-form > form > div#review-form-rating > i.selected').length) {
			values['rating'] = $('#review-form > form > div#review-form-rating > i.selected').data()['rating'];
		} else {
			values['rating'] = 0;
		}

		if (values['email'] && !emailRegEx.test(values['email'])) {
			$('#review-form > form > span.email-error').text('Please use a valid email address');
		} else {
			$('#review-form > form > span.email-error').text('');
			if (!values['name'] || !values['title'] || !values['rating']) {
				if (!values['name']) {
					$('#review-form > form > span.name-error').text("Who's writing this review?");
				} else {
					$('#review-form > form > span.name-error').text('');
				}
				if (!values['title']) {
					$('#review-form > form > span.title-error').text('What do you want to call your review?');
				} else {
					$('#review-form > form > span.title-error').text('');
				}
				if (!values['rating']) {
					$('#review-form > form > span.rating-error').text('What would you rate this product?');
				} else {
					$('#review-form > form > span.rating-error').text('');
				}
			} else {
				$.ajax({
					url: `/shop/product/${productID}/reviews`,
					method: "POST",
					data: values,
				}).then(function(response) {
					var data = JSON.parse(response);
					if (data['success']) {
						$('div#review-form > form').replaceWith("<h4 margin-bottom: 30px;>Thank you for the review! We appreciate your feedback.</h4>");
						$('a#review-write-btn').remove();
					}
				});
			}
		}
	}

	$(document).on('click', 'div#review-form-footer > input.btn-submit', (e) => {
		e.preventDefault();
		var values = {};
		var emailRegEx = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
		var productID = $('#review-form > form > input.review-product').val();

		const reader = new FileReader();

		values['name'] = $('#review-form > form > input.review-name').val();
		values['email'] = $('#review-form > form > input.review-email').val();
		values['location'] = $('#review-form > form >input.review-location').val();
		values['title'] = $('#review-form > form > input.review-title').val();
		values['body'] = $('#review-form > form > textarea.review-body').val();
		// var image = document.getElementById('review-image').files[0];

		// reader.onload = function(e) {
		// 	var fileData = reader.result;
		//     var bytes = new Uint8Array(fileData);
		//     var binaryText = '';

		//     for (var index = 0; index < bytes.byteLength; index++) {
		//         binaryText += String.fromCharCode(bytes[index]);
		//     }
		// 	values['image'] = binaryText;
		// 	newReview(values, emailRegEx, productID);
		//   };

		newReview(values, emailRegEx, productID);

		// if ($('#review-form > form > input#review-image').val()) {
		// 	reader.readAsArrayBuffer(image);
		// } else {
		// 	newReview(values, emailRegEx, productID);
		// }
	})

	$(document).on('keyup', '#review-form > form > textarea.review-body', (e) => {
		var contentLength = $(e.currentTarget).val().length;
		$('#review-form-body-count').html(1500 - contentLength);
	});

	$(document).on('change', '#review-form > form > textarea.review-body', (e) => {
		var contentLength = $(e.currentTarget).val().length;
		$('#review-form-body-count').html(1500 - contentLength);
	});

});
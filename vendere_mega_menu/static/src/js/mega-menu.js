odoo.define('vendere.megaMenu', function(require) {

	require('web.dom_ready');

	$(document).on('click', 'li.mega-menu a.nav-link', function(e){
		let $menuArch = $(e.currentTarget.nextElementSibling);
		let closeMenu = $menuArch.hasClass('open') ? true : false;
		window.setTimeout(function() {
			$menuArch.toggleClass('open');
			window.setTimeout(function() {
				if (closeMenu) {
					$menuArch.hide();
				}
			}, 300);
		}, 10);
		$menuArch.show();
	});

	$(document).on('mouseleave', 'li.mega-menu', function(e) {
		let $menuArch = $(e.currentTarget).children('section.menu-arch');
		let closeMenu = $menuArch.hasClass('open') ? true : false;
		if (closeMenu) {
			$menuArch.toggleClass('open');
			window.setTimeout(function() {
				$menuArch.hide();
			}, 300);
		}
	});

	// $('li.mega-menu').mouseleave((e) => {
	// 	let $menuArch = $(e.currentTarget).children('section.menu-arch');
	// 	let closeMenu = $menuArch.hasClass('open') ? true : false;
	// 	if (closeMenu) {
	// 		$menuArch.toggleClass('open');
	// 		window.setTimeout(function() {
	// 			$menuArch.hide();
	// 		}, 300);
	// 	}
	// });

	$(document).on('click', 'div.v-mega-container div.v-mega-parent button', function(e) {
		$(e.currentTarget).addClass('active');
		$(e.currentTarget).siblings('.active').removeClass('active');

		let selector = e.currentTarget.dataset['selector'];

		$(`div.v-mega-children a.active`).removeClass('active');
		$(`div.v-mega-img img.active`).removeClass('active');
		$(`div.v-mega-children a.${selector}`).addClass('active');
		$(`div.v-mega-img img.${selector}`).addClass('active');
	});

	// $('div.v-mega-shop div.v-mega-parent button').click((e) => {

	// 	$(e.currentTarget).addClass('active');
	// 	$(e.currentTarget).siblings('.active').removeClass('active');

	// 	let selector = e.currentTarget.dataset['selector'];

	// 	$(`div.v-mega-children a.active`).removeClass('active');
	// 	$(`div.v-mega-img img.active`).removeClass('active');
	// 	$(`div.v-mega-children a.${selector}`).addClass('active');
	// 	$(`div.v-mega-img img.${selector}`).addClass('active');
	// });

});
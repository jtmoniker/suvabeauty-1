odoo.define('theme_vendere.Navbar', function(require) {
	
	require('web.dom_ready');

	$(document).on('click', 'header a.search-link', function(e){
		e.preventDefault();
		var $el = $(e.target).closest('header');
		var $search = $el.find('div.search-dropdown');
		if ($search.hasClass('active')) {
			window.setTimeout(function() {
				$search.toggleClass('show-search');
			}, 500);
			$search.toggleClass('active');
		} else {
			window.setTimeout(function() {
				$search.toggleClass('active');
				$el.find('div.search-dropdown input').focus()
			}, 10);
			$search.toggleClass('show-search');
		}
	});	

	$(document).on('mouseleave', 'div.search-dropdown', function(e){
		var $el = $(e.currentTarget);
		if ($el.hasClass('active')) {
			window.setTimeout(function() {
				$el.toggleClass('show-search');
			}, 500);
			$el.toggleClass('active');
		}
	});
});
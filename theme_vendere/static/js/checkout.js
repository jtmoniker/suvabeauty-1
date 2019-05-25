odoo.define('theme_vendere.checkout', function(require) {

	require('web.dom_ready')

	$('div.div_zip label').removeClass('label-optional');
	$('div.div_zip label').text('Zip/Postal Code')

})
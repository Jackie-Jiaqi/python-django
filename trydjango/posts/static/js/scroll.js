$(function() {

	var modern = window.requestAnimationFrame,
	target = $('.fading'), zenith, nadir, spot, pilot;

	storeDimensions();

	$(window).resize(storeDimensions).scroll(function() {

		spot = $(this).scrollTop();

		if (!pilot) {
		if (modern) requestAnimationFrame(checkFade);
		else checkFade();
		}
	});

	$('.button').click(function(e) {

		e.preventDefault();

		pilot = true;

		var destination = $(this.hash).offset().top,
		goal = $(this.hash).find('.fading');

		if (destination != spot && goal.length) goal.stop().fadeTo(0,0);

		$('html, body').animate({scrollTop: destination}, 600, function() {

			if (goal.length) goal.fadeTo(1500,1);
			pilot = false;
		});
	});

function storeDimensions() {

	zenith = []; nadir = [];

	target.each(function() {

		var placement = $(this).offset().top;

		zenith.push(placement-$(window).height()*0.8);
		nadir.push(placement+$(this).outerHeight());
	});
}

function checkFade() {

	target.each(function(i) {

		if (!$(this).is(':animated')) {
		if (spot > zenith[i] && spot < nadir[i]) $(this).fadeTo(1500,1);
		else if ($(this).css('opacity') != 0) $(this).fadeTo(0,0);
		}
	});
}
});
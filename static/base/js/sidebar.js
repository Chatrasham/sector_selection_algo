(function($) {

	"use strict";

	var fullHeight = function() {

		$('.js-fullheight').css('height', $(window).height());
		$(window).resize(function(){
			$('.js-fullheight').css('height', $(window).height());
		});

	};
	fullHeight();

	$('#sidebarCollapse').on('click', function () {
		$('#sidebar').toggleClass('active');

		if($('.invisible_behind_sidebar').css('display') == "none"){
      		$('.invisible_behind_sidebar').css('display','block');
      		$('.navbar').css('width',"");
			$('.navbar').css('right',"20px");
			$('.navbar').css('left',"320px");
			}
      	else {

		$('.invisible_behind_sidebar').css('display','none');

      		$('.navbar').css('width',"97%");
			$('.navbar').css('right',"20px");
			$('.navbar').css('left',"20px");


			}

		if($('.searchbar_base').css('margin-inline-start') == "250px"){ // or this.value == 'volvo'
      		$('.searchbar_base').css('margin-inline-start',"110px");
			}
      	else {
		$('.searchbar_base').css('margin-inline-start', "250px");
			}

  });

})(jQuery);



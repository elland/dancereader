var popupStatus = 0;

function loadPopup(whichpopup) {
	if(popupStatus == 0) {
		$("#popupbg").css({
			"opacity": "0.7"
		});
		$("#popupbg").fadeIn("slow");
		$(whichpopup).fadeIn("slow");
		popupStatus = 1;
	}
}

function disablePopup(whichpopup) {
	if(popupStatus == 1) {
		$("#popupbg").fadeOut("noraml");
		$(whichpopup).fadeOut("normal");
		popupStatus = 0;
	}
}

function centerPopup(whichpopup) {
	var windowWidth = document.documentElement.clientWidth;
	var windowHeight = document.documentElement.clientHeight;
	var popupHeight = $(whichpopup).height();
	var popupWidth = $(whichpopup).width();
	
	$(whichpopup).css({
		"position": "absolute",
		"top": windowHeight/2-popupHeight/2,
		"left": windowWidth/2-popupWidth/2
	});
}

$(document).ready(function(){
	var windowHeight = document.documentElement.clientHeight;
	$("#main").css({"min-height": (windowHeight*78)/100});
	
	// Popups
	$(".addfeed").click(function(event){
		event.preventDefault();
		centerPopup("#addfeedpopup");
		loadPopup("#addfeedpopup");
	});
	$("#popupclose").click(function(event){
		event.preventDefault();
		disablePopup("#addfeedpopup");
	});

	$(".deletefeed").click(function(event){
		event.preventDefault();
		centerPopup("#deletefeedpopup");
		loadPopup("#deletefeedpopup");
	});
	$(".cancel").click(function(event){
		event.preventDefault();
		disablePopup("#deletefeedpopup");
	});
	
	$(".posttitle").click(function() {
		if ($(this).next("p.postcontent").is(":hidden")) {
			$(this).next("p.postcontent").slideDown("fast");
		}
		else {
			$(this).next("p.postcontent").slideUp("fast");
		}
	});
	$(".expandall").click(function(event) {
		event.preventDefault();
		$("p.postcontent").slideDown("fast");
	});
	$(".collapseall").click(function(event) {
		event.preventDefault();
		$("p.postcontent").slideUp("fast");
	});
});
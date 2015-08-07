$(document).ready(function() {
	$("a[rel=formatting]").click(function(){
		$("#formatting").slideToggle("slow");
		return false;
	});
	
	$("#top_links a").click(function(){
		$(".top-list").hide();
		$("#top_links li").removeClass("active");
		$("#"+$(this).attr("rel")).show();
		$(this).parent().addClass("active");
		return false;
	});
	
});
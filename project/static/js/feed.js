function view_story(id){
	var id = parseInt(id.substring(8));

}


// binders
window.onload = function(){
$(".relate_button").on("click", function relate(e){
	let button = document.getElementById(e.target.id);
	console.log($(button).css("color"));
	if($(button).css("color") == "rgb(79, 79, 79)"){
		$(button).css("color", "rgb(255, 0, 0)");
	}

	else if($(button).css("color") == "rgb(255, 0, 0)"){
		$(button).css("color", "rgb(79, 79, 79)");
	}

	let id = parseInt(button.id.substring(10));
	console.log(id);
	$.ajax({
	  type: "POST",
	  url: '/relate/' + id.toString(),
	  success: function(){
	  	console.log("success")
	  },
	  error: function(){
		console.log("error");
	  }
	});
});
}
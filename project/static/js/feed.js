
$(document).ready(function(){
	let likes = document.getElementsByClassName("relate_button");
	for (let i = 0; i < likes.length; i++) {
		let postid = parseInt(likes[i].id.substring(10));
		let like = document.getElementById(likes[i].id);
		var is_liked = "no";
		$.ajax({
		  type: "GET",
		  url: '/isliked/' + postid.toString(),
		  success: function(res){
		  	is_liked = res;
			set_relate_color(like, is_liked);
		  },
		  error: function(){
			console.log("error");
		  }
		});

	};
});

function set_relate_color(like, is_liked){
		if(is_liked === "yes"){
			console.log("IS LIKED");
			$(like).css("color", "rgb(255, 0, 0)");
		}
		else{
			$(like).css("color", "rgb(79, 79, 79)");
		}
};


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
		  success: function(res){
		  	console.log(res);
		  },
		  error: function(){
			console.log("error");
		  }
		});
	});

	$(".post_template").on("click", function show_story(e){
		console.log(e.target.parentElement.id);
		let post = document.getElementById(e.target.parentElement.id);
		let id = parseInt(post.id.toString().substring(8));

		$.ajax({
		  type: "GET",
		  url: '/stories/' + id.toString(),
		  success: function(res){
		  	window.location.href = res.redirecturl;

		  },
		  error: function(){
			console.log("error");
		  }
		});
	});
}
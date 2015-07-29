$(document).ready(function(){
	$('h1').click(function(){
		$.ajax({
			type: 'GET',
			url: 'http://api.test.com:8000/episode/15/.json',
			datatype: 'json',
			xhrFields: {
				withCredentials: true
			},
			success: function(data) { console.log(data); },
			error: function() { console.log("Failure!"); },
		});
	});
	
	$("#play").click(function(){
		$(this).toggleClass('glyphicon-pause').toggleClass('glyphicon-play'); 
	});
});

//$(document).on('click',"#play",function(){
//    $(this).toggleClass('glyphicon-pause').toggleClass('glyphicon-play');
//});

$(document).ajaxComplete(function(){            
//var response2 = $.parseJSON(response); //Takes AJAX Reponse Text and parses it to JSON
	//console.log(response2);
});

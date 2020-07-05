$('#create-meeting').click(function(){
	$('#chatt-room').html('');
	$("#chatt-room").append( "<div id ='meet'></div>" );
	createRoom(logedin_user , logedin_user);
});

function createRoom(room_name , display_name){
	const domain = 'meet.jit.si';
	const options = {
    	roomName: room_name,
    	width: 1000,
    	height: 600,
    	parentNode: document.querySelector('#meet'),
    	userInfo: {
        	displayName: display_name
    	}
	};
	const api = new JitsiMeetExternalAPI(domain, options);

}


$('#join-meeting-btn').click(function(){
	var room_name = $('#join-meeting-input').val();
	$('#vedio-chatt-room').html('');
	$("#vedio-chatt-room").append( "<div id ='meet'></div>" );
	createRoom(room_name , logedin_user);
});


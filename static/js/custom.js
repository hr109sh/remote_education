
$('#create-meeting').click(function(){
	var subject = $('#SubjectDropdown').val();
	var topic = $('#topicDropdown').val();
	if (subject && topic){
		$.ajax({
        	url: '/schedule_meeting/',
        	data: {
          		'subject': subject,
          		'topic' : topic
        	},
        	dataType: 'json',
        	success: function (data) {
        		$('#chatt-room').html('');
        		$("#chatt-room").append( "<p>Meeting Id :- "+data.meeting_id+"</p>" );
        		$("#chatt-room").append( "<div id ='meet'></div>" );
				createRoom(data.meeting_id,logedin_user);
        	}
      	});
	}
	else{
		$('#create-meeting-alet').html('Please select value');
		$('#create-meeting-alet').css('display','block');
	}
});

function createRoom(room_name , display_name){
	const domain = 'meet.jit.si';
	const options = {
    	roomName: room_name,
    	width: 1000,
    	height: 580,
    	parentNode: document.querySelector('#meet'),
    	userInfo: {
        	displayName: display_name
    	}
	};
	const api = new JitsiMeetExternalAPI(domain, options);

}


function QustionInteral(meeting_id) {
    $.ajax({
        url: '/get_question/',
        data: {
            'meetingId': meeting_id,
        },
        dataType: 'json',
        success: function (data) {
            $('.modal-body').html('')
            $("#exampleModalCenter").modal("hide");
            $('.modal-body').append("<p>"+data.question+"</p>");
            $(".modal-body").append( "<p id ='report_id'>"+data.student_report_id+"</p>" );
            $("#exampleModalCenter").modal("show");
        }
    });
}


$('#join-meeting-btn').click(function(){
	var meeting_name = $('#meeting-name').val();
	var meeting_id = $('#meetingid').val();
	if (meeting_name && meeting_id){
		$.ajax({
        	url: '/check_for_meetingid/',
        	data: {
          		'meetingId': meeting_id,
        	},
        	dataType: 'json',
        	success: function (data) {
        		if(data.metting_value){
        			$.ajax({
        				url: '/student_join_meeting/',
        				data: {
          					'meeting_name': meeting_name,
          					'meetingId' : meeting_id
        				},
        				dataType: 'json',
        				success: function (data) {
							$('#vedio-chatt-room').html('');
							$("#vedio-chatt-room").append( "<div id ='meet'></div>" );
							createRoom(meeting_id ,meeting_name);
        				}
      				});
                    setInterval( function() { QustionInteral(meeting_id); }, 100000);
        		}
        		else{
        			alert('fail')
        		}
        	}
      	});
	}
	else{
		$('#join-meeting-alert').html('Please Enter value');
		$('#join-meeting-alert').css('display','block');
	}
});


$('#yes-answer').click(function(){
    var studentReport_id = document.querySelector('#report_id').innerText;
   $.ajax({
        url: '/question_response/',
        data: {
            'studentReportId': studentReport_id,
            'responseAnswer':'Yes'
        },
        dataType: 'json',
        success: function (data) {
            $("#exampleModalCenter").modal("hide");
        }
    });
});

$('#no-answer').click(function(){
    var studentReport_id = document.querySelector('#report_id').innerText;
    $.ajax({
        url: '/question_response/',
        data: {
            'studentReportId': studentReport_id,
            'responseAnswer':'No'
        },
        dataType: 'json',
        success: function (data) {
            $("#exampleModalCenter").modal("hide");
        }
    });
});

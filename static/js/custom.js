
$('#create-meeting').click(function(){
	var subject = $('#SubjectDropdown').val();
	var topic = $('#topicDropdown').val();
    var grade = $('#GradeDropdown').val();
	if (subject && topic && grade){
		$.ajax({
        	url: '/schedule_meeting/',
        	data: {
          		'subject': subject,
          		'topic' : topic,
                'grade' : grade
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
            $('#response-option1').remove();
            $('#response-option2').remove();
            $('#option1').append("<p id ='response-option1'>"+data.option1+"</p>");
            $('#option2').append("<p id = 'response-option2'>"+data.option2+"</p>")
            $('#input-option1').val(data.option1);
            $('#input-option2').val(data.option2);
            $('input[name="optradio"]').prop('checked', false);
            $('#question').html('')
            $('#question').append("<p>"+data.question+"</p>");
            $("#question").append( "<p id ='report_id' style='display:none;'>"+data.student_report_id+"</p>" );
            $("#myToast").toast("show");
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
                    setInterval( function() { 
                                        QustionInteral(meeting_id);
                                        $("#myToast").toast("hide");
                                         }, 10000);
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


$('.myanswer').change(function(){
    var studentReport_id = document.querySelector('#report_id').innerText;
    var selValue = $("input[type='radio']:checked").val();
   $.ajax({
        url: '/question_response/',
        data: {
            'studentReportId': studentReport_id,
            'responseAnswer':selValue
        },
        dataType: 'json',
        success: function (data) {
            $("#myToast").toast("hide");
        }
    });
});


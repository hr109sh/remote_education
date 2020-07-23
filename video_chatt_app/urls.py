from django.urls import path
from video_chatt_app import views 

app_name = 'video_chatt_app'
urlpatterns = [
	path('',views.index,name = 'index'),
	path('create_meeting/',views.create_meeting,name="create_meeting"),
	path('join_meeting/',views.join_meeting,name = "join_meeting"),
	path('schedule_meeting/',views.schedule_meeting,name = "schedule_meeting"),
	path('check_for_meetingid/',views.check_for_meetingid,name = 'check_for_meetingid'),
	path('student_join_meeting/',views.student_join_meeting,name = 'student_join_meeting'),
	path('upload_question/',views.upload_question,name = "upload_question"),
	path('get_question/',views.get_question,name = "get_question"),
	path('question_response/',views.question_response,name="question_response"),
	path('student_info/',views.student_info,name="student_info"),
	path('intrac_tutor/',views.intract_tutor,name="intrac_tutor"),
	path('insert_question/',views.insert_question,name= "insert_question"),
	path('get_dashboard_data/',views.get_dashboard_data,name="get_dashboard_data"),
	path('teacher_dashboard/',views.teacher_dashboard,name="teacher_dashboard")
]
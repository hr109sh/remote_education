from django.urls import path
from video_chatt_app import views 

app_name = 'video_chatt_app'
urlpatterns = [
	path('',views.index,name = 'index'),
	path('create_meeting/',views.create_meeting,name="create_meeting"),
	path('join_meeting/',views.join_meeting,name = "join_meeting"),
	path('student_dashboard/',views.student_dashboard,name = "student_dashboard"),
	path('schedule_meeting/',views.schedule_meeting,name = "schedule_meeting"),
	path('check_for_meetingid/',views.check_for_meetingid,name = 'check_for_meetingid'),
	path('student_join_meeting/',views.student_join_meeting,name = 'student_join_meeting'),
	path('upload_question/',views.upload_question,name = "upload_question")
]
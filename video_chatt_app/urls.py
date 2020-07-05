from django.urls import path
from video_chatt_app import views 

app_name = 'video_chatt_app'
urlpatterns = [
	path('',views.index,name = 'index'),
	path('create_meeting/',views.create_meeting,name="create_meeting"),
	path('join_meeting/',views.join_meeting,name = "join_meeting"),
	path('student_dashboard/',views.student_dashboard,name = "student_dashboard")
]
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index(request):
	return render(request,'video_chatt_app/home.html')


# def client(request,room_name):
# 	return render(request,'video_chatt_app/client.html',{'room_name':room_name})


@login_required
def create_meeting(request):
	return render(request,'video_chatt_app/create_meeting.html')

@login_required
def join_meeting(request):
	return render(request,'video_chatt_app/join_meeting.html')


@login_required
def student_dashboard(request):
	return render(request,'video_chatt_app/student_dashboard.html')


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . models import *

# Create your views here.


@login_required
def index(request):
	user_obj = User.objects.get(username = request.user.username)
	user_role = UserRole.objects.get(user_id = user_obj)
	user_role_info = user_role.role_id.name
	return render(request,'video_chatt_app/home.html',{'user_role_info':user_role_info})


# def client(request,room_name):
# 	return render(request,'video_chatt_app/client.html',{'room_name':room_name})


@login_required
def create_meeting(request):
	user_obj = User.objects.get(username = request.user.username)
	subject_list = subject_teacher.objects.filter(user_id = user_obj)
	subject_obj = []
	for subject in subject_list:
		subject_obj.append(subject.subject_id)
	data = {
		'subject_obj':subject_obj
	}
	return render(request,'video_chatt_app/create_meeting.html',context=data)

@login_required
def join_meeting(request):
	return render(request,'video_chatt_app/join_meeting.html')


@login_required
def student_dashboard(request):
	return render(request,'video_chatt_app/student_dashboard.html')


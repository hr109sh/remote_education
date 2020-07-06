from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . models import *
from django.http import JsonResponse
import random

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
	topic_list = []
	for subject in subject_list:
		topic_obj = Topic.objects.filter(subject_id = subject.subject_id)
		topic_list.append(topic_obj)
	print(topic_list)
	data = {
		'subject_list':subject_list,
		'topic_list':topic_list
	}
	return render(request,'video_chatt_app/create_meeting.html',context=data)


def schedule_meeting(request):
	requested_sub = request.GET.get('subject', None)
	requested_topic = request.GET.get('topic', None)
	user_meeting_obj = 1
	while user_meeting_obj:
		meeting_id = random.randint(4444,77778886655)
		try:
			user_meeting_obj = UserMeeting.objects.get(meeting_id = meeting_id)
		except:
			user_meeting_obj = 0
	user_meeting = UserMeeting(
							user_id =  User.objects.get(username = request.user.username),
							meeting_id = meeting_id,
							meeting_subject = Subject.objects.get(subject_name = requested_sub),
							meeting_topic = Topic.objects.get(topic_name = requested_topic)
							)
	user_meeting.save()
	data = {
		'meeting_id':meeting_id
	}
	return JsonResponse(data)


@login_required
def join_meeting(request):
	return render(request,'video_chatt_app/join_meeting.html')


@login_required
def student_dashboard(request):
	return render(request,'video_chatt_app/student_dashboard.html')


def check_for_meetingid(request):
	meeting_id = request.GET.get('meetingId', None)
	try:
		user_meeting = UserMeeting.objects.get(meeting_id = meeting_id)
		data = {
			'metting_value' :True
		}
	except:
		data = {
			'metting_value' :False
		}
	return JsonResponse(data)

def student_join_meeting(request):
	meeting_id = request.GET.get('meetingId', None)
	meeting_name = request.GET.get('meetingName', None)
	user_attandance_obj = User_attendence(
							user_id = User.objects.get(username = request.user.username),
							meeting_id = UserMeeting.objects.get(meeting_id = meeting_id)
						)
	user_attandance_obj.save()
	data = {
		'mesaage':'Marked Attandance'
	}
	return JsonResponse(data)
	


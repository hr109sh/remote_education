from django.shortcuts import render,redirect
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
	subject_obj = Subject.objects.all()
	topic_obj = Topic.objects.all()
	grade_obj = UserGrade.objects.all()
	role_obj = Role.objects.get(name = 'student')
	requested_user = UserRole.objects.filter(role_id = role_obj)
	data = {
		'subject_obj':subject_obj,
		'topic_obj':topic_obj,
		'grade_obj':grade_obj,
		'requested_user':requested_user,
		'user_role_info':user_role_info

	}
	if user_role_info == 'teacher':
		return render(request,'video_chatt_app/home.html',context=data)
	else:
		return redirect('/join_meeting/')


# def client(request,room_name):
# 	return render(request,'video_chatt_app/client.html',{'room_name':room_name})


@login_required
def create_meeting(request):
	user_obj = User.objects.get(username = request.user.username)
	subject_list = subject_teacher.objects.filter(user_id = user_obj)
	user_role = UserRole.objects.get(user_id = user_obj)
	user_role_info = user_role.role_id.name
	topic_list = []
	for subject in subject_list:
		topic_obj = Topic.objects.filter(subject_id = subject.subject_id)
		topic_list.append(topic_obj)
	print(topic_list)
	data = {
		'subject_list':subject_list,
		'topic_list':topic_list,
		'user_role_info':user_role_info
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
	user_obj = User.objects.get(username = request.user.username)
	user_role = UserRole.objects.get(user_id = user_obj)
	user_role_info = user_role.role_id.name
	return render(request,'video_chatt_app/join_meeting.html',{'user_role_info':user_role_info})


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


def upload_question(request):
	user_obj = User.objects.get(username = request.user.username)
	user_role = UserRole.objects.get(user_id = user_obj)
	user_role_info = user_role.role_id.name
	return render(request,'video_chatt_app/upload_question.html',{'user_role_info':user_role_info})


def get_question(request):
	meeting_id = request.GET.get('meetingId', None)
	user_obj = User.objects.get(username = request.user.username)
	user_meeting_obj = UserMeeting.objects.get(meeting_id= meeting_id)
	user_question = Questions.objects.filter(topic_id = user_meeting_obj.meeting_topic)
	questions_list = []
	for item in user_question:
		questions_list.append(item)
	random_question = random.choice(questions_list)
	question_instance = Questions.objects.get(id = random_question.id)
	student_report_obj = StudentReport(
							user_id = user_obj,
							meeting_id = user_meeting_obj,
							question_id = question_instance,
						)
	student_report_obj.save()
	data = {
		'student_report_id':student_report_obj.id,
		'id':random_question.id,
		'topic_id':random_question.topic_id.topic_name,
		'question':random_question.question
	}
	return JsonResponse(data)


def question_response(request):
	student_report_id = request.GET.get('studentReportId', None)
	response_answer = request.GET.get('responseAnswer', None)
	student_response_obj = StudentReport.objects.get(id = student_report_id)
	correct_answer = Answer.objects.get(question_id = student_response_obj.question_id)
	if correct_answer.question_answer == response_answer:
		student_response_obj.answer_corrent = 'yes'
		data = {
			'message':'Correct Answer'
		}
	else:
		student_response_obj.answer_corrent = 'No'
		data = {
			'message':'Wrong Answer'
		}
	return JsonResponse(data)




	


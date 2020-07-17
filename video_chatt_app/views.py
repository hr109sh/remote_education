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
	user_role = UserRole.objects.filter(user_id = user_obj)[0]
	user_grade = UserRole.objects.filter(user_id = user_obj)
	subject_list = subject_teacher.objects.filter(user_id = user_obj)
	user_role_info = user_role.role_id.name
	student_role_id = Role.objects.get(name = 'student')
	student_list = UserRole.objects.filter(role_id = student_role_id)
	topic_list = []
	for subject in subject_list:
		topic_obj = Topic.objects.filter(subject_id = subject.subject_id)
		topic_list.append(topic_obj)
	data = {
		'user_role_info':user_role_info,
		'user_grade':user_grade,
		'subject_list':subject_list,
		'topic_list':topic_list,
		'student_list':student_list

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
	user_role = UserRole.objects.filter(user_id = user_obj)[0]
	user_role_info = user_role.role_id.name
	topic_list = []
	for subject in subject_list:
		topic_obj = Topic.objects.filter(subject_id = subject.subject_id)
		topic_list.append(topic_obj)
	data = {
		'subject_list':subject_list,
		'topic_list':topic_list,
		'user_role_info':user_role_info
	}
	return render(request,'video_chatt_app/create_meeting.html',context=data)


@login_required
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
	try:
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
	except Exception as err:
		print('error fetching details:', err)


@login_required
def join_meeting(request):
	user_obj = User.objects.get(username = request.user.username)
	user_role = UserRole.objects.filter(user_id = user_obj)[0]
	user_role_info = user_role.role_id.name
	return render(request,'video_chatt_app/join_meeting.html',{'user_role_info':user_role_info})




@login_required
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

@login_required
def student_join_meeting(request):
	meeting_id = request.GET.get('meetingId', None)
	meeting_name = request.GET.get('meetingName', None)
	try:
		user_attandance_obj = User_attendence(
								user_id = User.objects.get(username = request.user.username),
								meeting_id = UserMeeting.objects.get(meeting_id = meeting_id)
							)
		user_attandance_obj.save()
		data = {
			'mesaage':'Marked Attandance'
		}
		return JsonResponse(data)
	except Exception as err:
		print('error fetching details: ', err)


@login_required
def upload_question(request):
	user_obj = User.objects.get(username = request.user.username)
	subject_list = subject_teacher.objects.filter(user_id = user_obj)
	grade_list = TeacherGrade.objects.filter(user_id = user_obj)
	user_role = UserRole.objects.filter(user_id = user_obj)[0]
	user_role_info = user_role.role_id.name
	topic_list = []
	for subject in subject_list:
		topic_obj = Topic.objects.filter(subject_id = subject.subject_id)
		topic_list.append(topic_obj)
	data = {
		'subject_list':subject_list,
		'topic_list':topic_list,
		'user_role_info':user_role_info,
		'grade_list':grade_list
	}
	return render(request,'video_chatt_app/upload_question.html',context=data)


@login_required
def get_question(request):
	meeting_id = request.GET.get('meetingId', None)
	user_obj = User.objects.get(username = request.user.username)
	user_meeting_obj = UserMeeting.objects.get(meeting_id= meeting_id)
	user_question = Questions.objects.filter(topic_id = user_meeting_obj.meeting_topic)
	questions_list = []
	for item in user_question:
		questions_list.append(item)
	try:
		random_question = random.choice(questions_list)
		question_instance = Questions.objects.get(id = random_question.id)
		answer_obj = Answer.objects.get(question_id = question_instance)
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
			'question':random_question.question,
			'option1':answer_obj.option1,
			'option2':answer_obj.option2
		}
		return JsonResponse(data)
	except Exception as err:
		print('error fetching details:', err)

@login_required
def question_response(request):
	try:
		student_report_id = request.GET.get('studentReportId', None)
		response_answer = request.GET.get('responseAnswer', None)
		student_response_obj = StudentReport.objects.get(id = student_report_id)
		answer_obj = Answer.objects.get(question_id = student_response_obj.question_id)
		print(response_answer)
		print(answer_obj.correct_answer )
		if answer_obj.correct_answer == response_answer:
			student_response_obj.answer_corrent = 'yes'
			student_response_obj.save()
			data = {
				'message':'Correct Answer'
			}
		else:
			student_response_obj.answer_corrent = 'no'
			student_response_obj.save()
			data = {
				'message':'Wrong Answer'
			}
		return JsonResponse(data)
	except Exception as err:
		print('error fetching details: ', err)

@login_required
def student_info(request):
	try:
		user_obj = User.objects.get(username = request.user.username)
		user_role = UserRole.objects.filter(user_id = user_obj)[0]
		user_role_info = user_role.role_id.name
		return render(request, 'video_chatt_app/student_info.html',{'user_role_info':user_role_info})
	except Exception as err:
		print('Error fetching details:', err)

@login_required
def insert_question(request):
	selected_grade = request.GET.get('selectedGrade', None)
	selected_sub = request.GET.get('selectedSub', None)
	selected_topic = request.GET.get('selectedTopic', None)
	input_question = request.GET.get('inputQuestion', None)
	option1 = request.GET.get('option_1', None)
	option2 = request.GET.get('option_2', None)
	selected_answer = request.GET.get('selectedAnswer', None)
	if selected_answer == 'option1':
		response_answer = option1
	else:
		response_answer = option2
	try:
		topic_obj = Topic.objects.get(topic_name = selected_topic)
		question_obj = Questions(topic_id = topic_obj,question = input_question)
		question_obj.save()
		answer_obj = Answer(
						question_id = question_obj,
						option1 = option1,
						option2 = option2,
						correct_answer = response_answer
					)
		answer_obj.save()

		
		data = {
			'message':'Saved Sucessfully'
		}
		return JsonResponse(data)
	except Exception as err:
		print('Error fetching details: ' , err)


	


from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from . models import *
from django.http import JsonResponse
import random
import datetime
from django.db.models import Q

# Create your views here.


@login_required
def index(request):
	user_obj = User.objects.get(username = request.user.username)
	user_role = UserRole.objects.filter(user_id = user_obj)[0]
	user_grade = TeacherGrade.objects.filter(user_id = user_obj)
	subject_list = subject_teacher.objects.filter(user_id = user_obj)
	user_role_info = user_role.role_id.name
	student_role_id = Role.objects.get(name = 'student')
	student_list = UserRole.objects.filter(role_id = student_role_id)
	topic_list = []
	total_student_count = total_session_attended(request.user.username)
	student_attentiveness = total_student_attentivness(request.user.username)
	accurate_response = total_accurate_response(request.user.username)
	for subject in subject_list:
		topic_obj = Topic.objects.filter(subject_id = subject.subject_id)
		topic_list.append(topic_obj)
	data = {
		'user_role_info':user_role_info,
		'user_grade':user_grade,
		'subject_list':subject_list,
		'topic_list':topic_list,
		'student_list':student_list,
		'total_student_count':total_student_count,
		'student_attentiveness':student_attentiveness,
		'accurate_response':accurate_response

	}
	if user_role_info == 'teacher':
		return render(request,'video_chatt_app/home.html',context=data)
	else:
		return redirect('/join_meeting/')


def total_session_attended(username):
	user_obj = User.objects.get(username = username)
	user_metting_obj = UserMeeting.objects.filter(user_id = user_obj)
	count = 0
	for user_meeting in user_metting_obj:
		user_attendence_obj = User_attendence.objects.filter(meeting_id = user_meeting)
		count = count+len(user_attendence_obj)
	return count


def total_student_attentivness(username):
	user_obj = User.objects.get(username = username)
	teacher_meeting_obj = UserMeeting.objects.filter(user_id = user_obj)
	total_question = 0 
	user_response = 0 
	student_attentiveness = 0
	for meeting_obj in teacher_meeting_obj:
		student_report_obj = StudentReport.objects.filter(meeting_id = meeting_obj)
		total_question = total_question+len(student_report_obj)
		for student_data in student_report_obj:
			if student_data.answer_time:
				user_response = user_response+1
	if user_response and total_question:
		student_attentiveness = "{:.2f}".format((user_response/total_question)*100)
	return student_attentiveness


def total_accurate_response(username):
	user_obj = User.objects.get(username = username)
	teacher_meeting_obj = UserMeeting.objects.filter(user_id = user_obj)
	total_question = 0 
	user_correct_response = 0 
	accurate_response = 0
	for meeting_obj in teacher_meeting_obj:
		student_report_obj = StudentReport.objects.filter(meeting_id = meeting_obj)
		total_question = total_question+len(student_report_obj)
		for student_data in student_report_obj:
			if student_data.answer_corrent == 'yes':
				user_correct_response = user_correct_response+1
	if user_correct_response and total_question:
		accurate_response = "{:.2f}".format((user_correct_response/total_question)*100)
	return accurate_response



@login_required
def create_meeting(request):
	user_obj = User.objects.get(username = request.user.username)
	subject_list = subject_teacher.objects.filter(user_id = user_obj)
	user_grade = TeacherGrade.objects.filter(user_id = user_obj)
	user_role = UserRole.objects.filter(user_id = user_obj)[0]
	user_role_info = user_role.role_id.name
	topic_list = []
	for subject in subject_list:
		topic_obj = Topic.objects.filter(subject_id = subject.subject_id)
		topic_list.append(topic_obj)
	data = {
		'subject_list':subject_list,
		'topic_list':topic_list,
		'user_grade':user_grade,
		'user_role_info':user_role_info
	}
	return render(request,'video_chatt_app/create_meeting.html',context=data)


@login_required
def schedule_meeting(request):
	requested_sub = request.GET.get('subject', None)
	requested_topic = request.GET.get('topic', None)
	requested_grade = request.GET.get('grade', None)
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
							grade_id = UserGrade.objects.get(student_grade = int(requested_grade)),
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
		student_grade_obj = StudentGrade.objects.get(user_id = User.objects.get(username = request.user.username))
		attention_span_obj = AttentionSpain.objects.get(user_grade = student_grade_obj.grade_id)
		user_attandance_obj = User_attendence(
								user_id = User.objects.get(username = request.user.username),
								meeting_id = UserMeeting.objects.get(meeting_id = meeting_id)
							)
		user_attandance_obj.save()
		data = {
			'mesaage':'Marked Attandance',
			'attention_span':attention_span_obj.attention_span
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
		if answer_obj.correct_answer == response_answer:
			student_response_obj.answer_corrent = 'yes'
			student_response_obj.answer_time = datetime.datetime.now()
			student_response_obj.save()
			data = {
				'message':'Correct Answer'
			}
		else:
			student_response_obj.answer_corrent = 'no'
			student_response_obj.answer_time = datetime.datetime.now()
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
		student_grade = StudentGrade.objects.filter(user_id = user_obj)[0]
		# accurate_response = get_student_attentivness(user_obj)
		data = {
			# 'student_grade':student_grade,
			'user_role_info':user_role_info
		}
		return render(request, 'video_chatt_app/student_info.html',context=data)
	except Exception as err:
		print('Error fetching details:', err)


# def get_student_attentivness(user_obj):
# 	total_question = 0 
# 	user_response = 0 
# 	student_attentiveness = 0
# 	studengt_response = StudentReport.objects.filter(user_id = user_obj)
# 	total_question = total_question+len(studengt_response)
# 	for response in studengt_response:
# 		if response.answer_time:
# 			user_response = user_response+1
# 	if user_response and total_question:
# 		student_attentiveness = "{:.2f}".format((user_response/total_question)*100)
# 	return student_attentiveness

# def get_student_accurate_response():
# 	return 

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

def get_dashboard_data(request):
	selected_grade = request.GET.get('selectedGrade', None)
	selected_sub = request.GET.get('selectedSub', None)
	selected_topic = request.GET.get('selectedTopic', None)
	search_parameter = {
							'grade_id':selected_grade,
							'meeting_subject':selected_sub,
							'meeting_topic':selected_topic,
							'user_id':request.user.username
						}

	req = None
	for key,value in search_parameter.items():
		if value!='':
			if key == 'grade_id':
				grade_obj = UserGrade.objects.get(student_grade = int(value))
				new_req = Q(**{key: grade_obj})
			elif key == 'meeting_subject':
				subject_obj = Subject.objects.get(subject_name = value)
				new_req = Q(**{key: subject_obj})
			elif key == 'meeting_topic':
				topic_obj = Topic.objects.get(topic_name = selected_topic)
				new_req = Q(**{key: topic_obj})
			elif key == 'user_id':
				user_obj = User.objects.get(username = request.user.username)
				new_req = Q(**{key: user_obj})
			if req:
				req &= new_req
			else:
				req = new_req
		else:
			continue
	user_meeting_obj = UserMeeting.objects.filter(req)
	if user_meeting_obj:
		session_attended = get_total_session_attended(user_meeting_obj)
		student_attentivness = get_total_student_attentivness(user_meeting_obj)
		accurate_response = get_total_accurate_response(user_meeting_obj)
	else:
		session_attended = 0
		student_attentivness = 0
		accurate_response = 0

	data = {
		'session_attended':session_attended,
		'student_attentivness':student_attentivness,
		'accurate_response':accurate_response
	}
	return JsonResponse(data)


def get_total_session_attended(user_meeting_obj):
	count = 0
	for user_meeting in user_meeting_obj:
		user_attendence_obj = User_attendence.objects.filter(meeting_id = user_meeting)
		count = count+len(user_attendence_obj)
	return count


def get_total_student_attentivness(user_meeting_obj):
	total_question = 0 
	user_response = 0 
	student_attentiveness = 0
	for meeting_obj in user_meeting_obj:
		student_report_obj = StudentReport.objects.filter(meeting_id = meeting_obj)
		total_question = total_question+len(student_report_obj)
		for student_data in student_report_obj:
			if student_data.answer_time:
				user_response = user_response+1
	if user_response and total_question:
		student_attentiveness = "{:.2f}".format((user_response/total_question)*100)
	return student_attentiveness


def get_total_accurate_response(user_meeting_obj):
	total_question = 0 
	user_correct_response = 0 
	accurate_response = 0
	for meeting_obj in user_meeting_obj:
		student_report_obj = StudentReport.objects.filter(meeting_id = meeting_obj)
		total_question = total_question+len(student_report_obj)
		for student_data in student_report_obj:
			if student_data.answer_corrent == 'yes':
				user_correct_response = user_correct_response+1
	if user_correct_response and total_question:
		accurate_response = "{:.2f}".format((user_correct_response/total_question)*100)
	return accurate_response




def intract_tutor(request):
	user_obj = User.objects.get(username = request.user.username)
	user_role = UserRole.objects.filter(user_id = user_obj)[0]
	user_role_info = user_role.role_id.name
	return render(request,'video_chatt_app/intract_tutor.html',{'user_role_info':user_role_info})

def add_topic(request):
	user_obj = User.objects.get(username = request.user.username)
	subject_list = subject_teacher.objects.filter(user_id = user_obj)
	grade_list = TeacherGrade.objects.filter(user_id = user_obj)
	user_role = UserRole.objects.filter(user_id = user_obj)[0]
	user_role_info = user_role.role_id.name
	data = {
		'subject_list':subject_list,
		'user_role_info':user_role_info,
		'grade_list':grade_list
	}
	return render(request,'video_chatt_app/add_topic.html',{'user_role_info':user_role_info})


def teacher_dashboard(request):
	meeting_id = request.GET.get('meetingId', None)
	meeting_obj = UserMeeting.objects.filter(meeting_id = int(meeting_id))
	student_attendance = get_total_session_attended(meeting_obj)
	student_activness = get_total_student_attentivness(meeting_obj)
	student_effectness = get_total_accurate_response(meeting_obj)
	data = {
		'student_attendance':student_attendance,
		'student_activness':student_activness,
		'student_effectness':student_effectness
	}
	return JsonResponse(data)



	


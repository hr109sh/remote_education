from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Role(models.Model):
	name = models.CharField(max_length = 100)

	def __str__(self):
		return self.name


class UserRole(models.Model):
	user_id= models.ForeignKey(User, on_delete=models.CASCADE)
	role_id = models.ForeignKey(Role, on_delete=models.CASCADE)



class Subject(models.Model):
	subject_name = models.CharField(max_length = 100)

	def __str__(self):
		return self.subject_name


class Topic(models.Model):
	topic_name = models.CharField(max_length = 100)
	subject_id = models.ForeignKey(Subject,on_delete=models.CASCADE)

class Questions(models.Model):
	topic_id = models.ForeignKey(Topic,on_delete = models.CASCADE)
	question = models.TextField()

class Answer(models.Model):
	question_id = models.ForeignKey(Questions,on_delete = models.CASCADE)
	question_answer = models.CharField(max_length = 100)

class subject_teacher(models.Model):
	subject_id = models.ForeignKey(Subject,on_delete= models.CASCADE)
	user_id = models.ForeignKey(User,on_delete = models.CASCADE)

class user_parent(models.Model):
	parent_name = models.CharField(max_length = 100)
	user_id = models.ForeignKey(User,on_delete = models.CASCADE)



class UserMeeting(models.Model):
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
	meeting_id = models.IntegerField()
	meeting_subject = models.ForeignKey(Subject,on_delete = models.CASCADE)
	meeting_topic = models.ForeignKey(Topic,on_delete = models.CASCADE)
	meet_start = models.DateTimeField(auto_now_add=True)
	meet_end = models.DateTimeField(null=True,blank=True)

class User_attendence(models.Model):
	user_id= models.ForeignKey(User, on_delete=models.CASCADE)
	meeting_id = models.ForeignKey(UserMeeting,on_delete=models.CASCADE)

class StudentReport(models.Model):
	user_id = models.ForeignKey(User,on_delete = models.CASCADE)
	meeting_id = models.ForeignKey(UserMeeting,on_delete = models.CASCADE)
	question_id = models.ForeignKey(Questions,on_delete = models.CASCADE)
	question_time = models.DateTimeField(auto_now_add = True)
	answer_time = models.DateTimeField(null=True)
	answer_corrent = models.CharField(max_length = 100)


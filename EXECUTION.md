# Execution

In TeacherAssist, the teacher and student users are created by the superadmin. The superadmin is the school administrator. The management of the roles and the responsibility lies with the superadmin. 

## Steps to Create Super Admin User

Super Admin User is school administrator responsible for the creation and management of teacher and student users.

1. 	Navigate to the repository and change to the directory where the app is located.

```bash
cd remote_education
```

2. 	Run the below command. Provide details of username, email address and password

```bash
python manage.py createsuperuser
```	

![TeacherAssist/Create_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/create_superadmin.png)

3.	Run the app.

```bash
python manage.py runserver
```

View your app at: http://localhost:8000

4. Hit the url http://localhost:8000/admin/ and login using the super user credentials 

![TeacherAssist/Login_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/django_admin_login.png)

## Steps to Create Subject

The different subjects taught in the school are entered into the system.

1. 	Hit the url http://localhost:8000/admin/video_chatt_app/subject/ to add new subject introduced. Click on 'ADD SUBJECT'

![TeacherAssist/Subject_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_subject.png)

2. 	Add the subject of your choice and save

![TeacherAssist/NewSubject_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/new_subject.png)

## Steps to Set-up Teacher User

A new teacher can be added in the system by the school administrator. 
Note: All the steps are required and have to be added in the appropriate sequence. 

### Add New Teacher

1. 	Hit the url http://localhost:8000/admin/auth/user/ to add new teacher. Click on Add User.

![TeacherAssist/NewUser_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_newuser.png)

2. 	Enter the username as per the organizational guidelines. Set a default password. Click on SAVE. 

![TeacherAssist/NewUser1_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/new_user.png)

3.	User will be successfully created. You will now be prompted to add additional user details like First Name, Last Name, Email Address. 
Additional details can be added. Click on SAVE.

![TeacherAssist/NewUser1_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_userdetails.png)

### Associate Teacher with Teacher Role

1. 	Hit the url http://localhost:8000/admin/video_chatt_app/userrole/ and Click on 'ADD USER ROLE'

![TeacherAssist/UserRole_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_userrole.png)

2.	Select the teacher to be mapped to the 'teacher' role id. Click on SAVE.
![TeacherAssist/MapRoleTeacher_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/map_teacherrole.png)

### Associate Teacher with Subjects

1. 	Hit the url http://localhost:8000/admin/video_chatt_app/subject_teacher/ and Click on 'ADD SUBJECT TEACHER'

![TeacherAssist/SubjectTeacher_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_subjectteacher.png)

2.	Select the appropriate subject id and user id. Click on SAVE.

![TeacherAssist/MapSubjectTeacher_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/map_subjectteacher.png)

### Associate Teacher with Grade

1. 	Hit the url http://localhost:8000/admin/video_chatt_app/teachergrade/ and Click on 'ADD TEACHER GRADE'

![TeacherAssist/GradeTeacher_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_teachergrade.png)

2.	Select the appropriate user id and grade id. Click on SAVE. 
	Note: The grade id is indicated in the brackets and refer to the grade the teacher is teaching. e.g. UserGrade object(3) means 3rd grade.

![TeacherAssist/MapGradeTeacher_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/teacher_grade.png)

## Steps to Set-up Student User

A new student can be added in the system by the school administrator. 
Note: All the steps are required and have to be added in the appropriate sequence. 

### Add New Student

1. 	Hit the url http://localhost:8000/admin/auth/user/ to add new student. Click on Add User.

![TeacherAssist/NewUser_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_newuser.png)

2. 	Enter the username as per the organizational guidelines. Set a default password. Click on SAVE. 

![TeacherAssist/Student_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_student.png)

3.	User will be successfully created. You will now be prompted to add additional user details like First Name, Last Name, Email Address. 
Additional details can be added. Click on SAVE.

![TeacherAssist/Student_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_studentdetails.png)

### Associate Teacher with Student Role

1. 	Hit the url http://localhost:8000/admin/video_chatt_app/userrole/ and Click on 'ADD USER ROLE'

![TeacherAssist/UserRole_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_userrole.png)

2.	Select the student to be mapped to the 'student' role id. Click on SAVE.
![TeacherAssist/MapRoleStudent_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/map_studentrole.png)

### Associate Student with Grade

1. 	Hit the url http://localhost:8000/admin/video_chatt_app/studentgrade/ and Click on 'ADD STUDENT GRADE'

![TeacherAssist/GradeStudent_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/add_studentgrade.png)

2.	Select the appropriate user id and grade id. Click on SAVE. 
	Note: The grade id is indicated in the brackets and refer to the grade the student is studying in. e.g. UserGrade object(3) means 3rd grade.

![TeacherAssist/MapGradeStudent_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/map_studentgrade.png)

## View Role 

There are currently two roles in the TeacherAssist application i.e. Teacher and Student.

Hit the url http://localhost:8000/admin/video_chatt_app/role/ and view the available roles in the system.

![TeacherAssist/Role_SuperAdmin](https://github.com/hr109sh/remote_education/blob/master/static/images/django_roles.png)

from django.db import models
from django.contrib import admin
from django.contrib.auth.models import *

# Create your models here.
class TeacherManager(models.Manager):
    def create_teacher(self, name, highschool, university, age, sex, career, money, tutorTime, tutorType, user):
        teacher = self.model(name=name, highschool=highschool, university=university, age=age, sex=sex, career=career, money=money, tutorTime=tutorTime, tutorType=tutorType)
        teacher.user = user
        teacher.save()
        return teacher 

    def change_teacher(self, id, name, highschool, university, age, sex, career, money, tutorTime, tutorType):
        teacher =  self.get(id=id)
        teacher.name = name
        teacher.highschool = highschool
        teacher.university = university
        teacher.age = age
        teacher.sex = sex
        teacher.career = career
        teacher.money = money
        teacher.tutorTime = tutorTime
        teacher.tutorType = tutorType
        teacher.save()
        return teacher

class Teacher(models.Model):
    name = models.CharField(max_length = 30)
    highschool = models.CharField(max_length = 30)
    university = models.CharField(max_length = 30)
    age = models.IntegerField()
    sex = models.IntegerField()
    career = models.TextField()
    money = models.IntegerField()
    tutorTime = models.IntegerField()
    tutorType = models.IntegerField()
    user = models.OneToOneField(User, null=True)
    objects = TeacherManager()

class TeacherAdmin(admin.ModelAdmin):
    list_display = ('name', 'highschool', 'university', 'age', 'sex', 'career', 'money', 'tutorTime', 'tutorType', 'get_user')
    def get_user(self, obj):
        return obj.user.username
admin.site.register(Teacher, TeacherAdmin)


class StudentManager(models.Manager):
    def create_student(self, name, grade, sex, user):
        student = self.model(name=name, grade=grade, sex=sex)
        student.user = user
        student.save()
        return student

class Student(models.Model):
    name = models.CharField(max_length = 30)
    grade = models.IntegerField()
    sex = models.IntegerField()
    user = models.OneToOneField(User, null=True)
    objects = StudentManager()

class StudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'grade', 'sex', 'get_user')
    def get_user(self, obj):
        return obj.user.username
admin.site.register(Student, StudentAdmin)


class StudentLectureOfferManager(models.Manager):
    def create(self, money, tutorTime, comment, user):
        studentLectureOffer = self.model(money=money, tutorTime=tutorTime, comment=comment)
        studentLectureOffer.user = user 
        studentLectureOffer.save()
        return studentLectureOffer;

class StudentLectureOffer(models.Model):
    money = models.IntegerField()
    tutorTime = models.IntegerField()
    comment = models.TextField()
    user = models.ForeignKey(User)
    objects = StudentLectureOfferManager()

class StudentLectureOfferAdmin(admin.ModelAdmin):    
    list_display = ('id', 'get_user', 'money', 'tutorTime', 'comment')
    def get_user(self, obj):
        return obj.user.username
admin.site.register(StudentLectureOffer, StudentLectureOfferAdmin)

class LectureManager(models.Manager):
    def create_lecture(self, teacher, student, startDate, endDate, totalTime, spentTime):
        lecture = self.model(startDate=startDate, endDate=endDate, totalTime=totalTime, spentTime=spentTime)
        lecture.teacher = teacher
        lecture.save()
        lecture.student.add(student)
        return lecture

class Lecture(models.Model):
    teacher = models.ForeignKey(Teacher)
    student = models.ManyToManyField(Student)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    totalTime = models.FloatField()
    spentTime = models.FloatField()
    objects = LectureManager()

class LectureAdmin(admin.ModelAdmin):
    list_display = ('startDate', 'endDate', 'totalTime', 'spentTime', 'get_teacher', 'get_students')
    def get_teacher(self, obj):
        return obj.teacher.name
    def get_students(self, obj):
        name = '';
        for student in obj.student.all():
            name = name + student.name + ' '
        return name
admin.site.register(Lecture, LectureAdmin)

class TeacherRequestManager(models.Manager):
    def create_teacher_request(self, teacher, student, comment, permission) :
        teacherRequest = self.model(comment=comment, permission=permission)
        teacherRequest.teacher = teacher 
        teacherRequest.student = student
        teacherRequest.save() 
        return teacherRequest

class TeacherRequest(models.Model):
    teacher = models.ForeignKey(Teacher)
    student = models.ForeignKey(User)
    comment = models.TextField()
    permission = models.IntegerField()
    objects = TeacherRequestManager()

class TeacherRequestAdmin(admin.ModelAdmin):
    list_display = ('get_teacher', 'get_student', 'comment', 'permission')
    def get_teacher(self, obj):
        return obj.teacher.name
    def get_student(self, obj):
        return obj.student.username
admin.site.register(TeacherRequest, TeacherRequestAdmin)

class StudentRequestManager(models.Manager):
    def create_student_request(self, student, teacher, comment, permission) : 
        studentRequest = self.model(comment=comment, permission=permission) 
        studentRequest.teacher = teacher
        studentRequest.student = student
        studentRequest.save()
        return studentRequest
    
class StudentRequest(models.Model):
    student = models.ForeignKey(Student)
    teacher = models.ForeignKey(Teacher)
    comment = models.TextField()
    permission = models.IntegerField()
    objects = StudentRequestManager()
    
class StudentRequestAdmin(admin.ModelAdmin):
    list_display = ('get_student', 'get_teacher', 'comment', 'permission')
    def get_student(self, obj):
        return obj.student.name
    def get_teacher(self, obj):
        return obj.teacher.name
admin.site.register(StudentRequest, StudentRequestAdmin)

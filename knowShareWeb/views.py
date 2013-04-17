# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext 
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth import *
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist 
from knowShareWeb.forms import * 
from knowShareWeb.models import *

#HTML ACCESS
def main_page(request):
    return render_to_response('index.html', RequestContext(request))

def howto_page(request):
    return render_to_response('howto.html', RequestContext(request))

def teacher_page(request):
    isInGroup = False
    for group in request.user.groups.all():
        if group.name == 'Teacher' or group.name == 'Student':
            isInGroup = True 
    teachers =  Teacher.objects.all()
    for teacher in teachers:
        teacher.career =  teacher.career.replace('\r', '</br>')
        
    if request.user.is_authenticated() == False : 
        teacherRequests = request.user.teacherrequest_set.all()
        return render_to_response('teacher.html', RequestContext(request, {'isInGroup' : isInGroup, 'teachers' : teachers, 'user' : request.user, 'teacherRequests' : teacherRequests }))
    else :
        return render_to_response('teacher.html', RequestContext(request, {'isInGroup' : isInGroup, 'teachers' : teachers}))

def teacherSubmit_page(request):
    if request.user.is_authenticated() == False:
        return render_to_response('teacherSubmit.html', RequestContext(request,{'Confirmed' : 0}))

    try :
        request.user.teacher
    except ObjectDoesNotExist :
        return render_to_response('teacherSubmit.html', RequestContext(request))

    return render_to_response('teacherSubmit.html', RequestContext(request, {'Confirmed' : 1, 'name' : request.user.teacher.name}))

def student_page(request):
    students = Student.objects.all()
    return render_to_response('student.html', RequestContext(request, {'students' : students}))

def studentSubmit_page(request):
    if request.user.is_authenticated() == False:
        return render_to_response('studentSubmit.html', RequestContext(request,{'Confirmed' : 0}))

    return render_to_response('studentSubmit.html', RequestContext(request))

def lecture_page(request):
    #lectures = None
    if request.user.is_authenticated() == False:
            return render_to_response('lecture.html', RequestContext(request, {'Confirmed' : 0 }))
    try : 
        lectures = request.user.teacher.lecture_set.all()
        return render_to_response('lecture.html', RequestContext(request, {'lectures' : lectures}))
    except ObjectDoesNotExist :
        return render_to_response('lecture.html', RequestContext(request))

def lectureSubmit_page(request):
    if request.user.is_authenticated() == False:
        return render_to_response('lectureSubmit.html', RequestContext(request, {'months' : range(1, 12), 'Confirmed' : 0}))

    #Teacher Attribute Check 
    try :
        request.user.teacher 
    except ObjectDoesNotExist :
        return render_to_response('lectureSubmit.html', RequestContext(request, {'months' : range(1, 13), 'Confirmed' : 1}))

    return render_to_response('lectureSubmit.html', RequestContext(request, {'months' : range(1, 13)}))       

def contact_page(request):
    return render_to_response('contact.html', RequestContext(request))

def my_profile_page(request):
    isTeacher = False
    isStudent = False
    careers = None
    print request.user.student_set.all()
    for group in request.user.groups.all():
        if group.name == 'Teacher' :
            isTeacher = True
            careers =  request.user.teacher.career.split('\r')
        elif group.name == 'Student' :
            isStudent = True


    return render_to_response('myProfile.html', RequestContext(request, {'user' : request.user, 'isTeacher' : isTeacher, 'isStudent' : isStudent, 'careers' : careers }))

def submit_list_page(request):
    studentRequests = None
    studentRequestsToMe = None
    students = None 
    try : 
        studentRequests = request.user.teacher.studentrequest_set.all()
    except ObjectDoesNotExist : 
        studentRequests = []

    teacherRequests = request.user.teacherrequest_set.all()
    try : 
        studentRequestsToMe = request.user.teacher.teacherrequest_set.all()
    except ObjectDoesNotExist : 
        studentRequestsToMe = []
    try : 
        students = request.user.student_set.all()
    except ObjectDoesNotExist : 
        students = []
    
    return render_to_response('submitList.html', RequestContext(request, {'studentRequests' : studentRequests, 'teacherRequests' : teacherRequests, 'studentRequestsToMe' : studentRequestsToMe, 'students' : students}))

#Account Setting
@csrf_exempt
def login_page(request):
    if request.method == 'POST' : 
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
            return HttpResponseRedirect('/')
        else:
            return render_to_response('index.html', RequestContext(request, {'loginerror' : True, 'login' : True}))
    else:
        return render_to_response('index.html', RequestContext(request, {'loginerror' : False, 'login' : True}))
    

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/')

def register_page(request):
    if request.method == 'POST' :
       form = RegistrationForm(request.POST)
       if form.is_valid() :
          user = User.objects.create_user(
                  username=request.POST['username'],
                  password=request.POST['password'],
                  email=request.POST['email']
                 )
          if user is not None: 
              user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
              if user.is_active:
                  auth.login(request, user)

          return HttpResponseRedirect('/')
       else :
          return render_to_response('index.html', RequestContext(request, {'signuperror' : True, 'signup' : True}))
    else :
        return HttpResponseRedirect('/studentSubmit')
    

#Teacher PostMethod
def teacher_register_page(request):
    if request.method == 'POST' :
        form = TeacherRegistrationForm(request.POST)

        sex = 0
        if request.POST['sex'] == 'male':
            sex = 0
        else :
            sex = 1

        teacher = Teacher.objects.create_teacher(
            name = request.POST['name'],
            highschool = request.POST['highschool'],
            university = request.POST['university'],
            age = request.POST['age'],
            sex = sex,
            career = request.POST['career'],
            money = request.POST['money'],
            tutorTime = request.POST['tutorTimeIdx'],
            tutorType = request.POST['tutorTypeIdx'],
            user = request.user
            )

        return HttpResponseRedirect('/')

def student_register_page(request):
    if request.method == 'POST' :        
        sex = 0
        if request.POST['sex'] == 'male':
            sex = 0
        else: 
            sex = 1
        
        student = Student.objects.create_student(
            name = request.POST['name'],
            grade = request.POST['gradeIdx'],
            sex = sex,
            money = request.POST['money'],
            tutorTime = request.POST['tutorTimeIdx'],
            comment = request.POST['comment'],
            user = request.user
            )
        
        return HttpResponseRedirect('/')

def lecture_register_page(request):
    if request.method == 'POST':
        student = None
        try : 
            student =  Student.objects.get(id__exact=request.POST['sid'])
        except : 
            return render_to_response('lectureSubmit.html', RequestContext(request, {'error' : True, 'months' : range(1,13)}))
        

        lecture = Lecture.objects.create_lecture(
                     teacher = request.user.teacher,
                     student = student,
                     startDate = request.POST['startDate'],
                     endDate = request.POST['endDate'],
                     totalTime = request.POST['count'],
                     spentTime = 0
                     )

        return HttpResponseRedirect('/')
    else :
        return render_to_response('lectureSubmit.html', RequestContext(request, {'months' : range(1,13)}));

# Request
def teacher_request_page(request):
    if request.method == 'POST' :
        teacher = Teacher.objects.get(id__exact=request.POST['teacherID'])
        TeacherRequest.objects.create_teacher_request(
            teacher = teacher,
            student = request.user,
            comment = "Hi",
            permission = 0)
        
        return HttpResponseRedirect('/')
            
    else :
        return HttpResponseRedirect('/')

def student_request_page(request):
    if request.method == 'POST' : 
        student = Student.objects.get(id__exact=request.POST['studentID'])
        StudentRequest.objects.create_student_request(
            student = student,
            teacher = request.user.teacher,
            comment = "Hi",
            permission = False)
        
        return HttpResponseRedirect('/')
    else :
        return HttpResponseRedirect('/')

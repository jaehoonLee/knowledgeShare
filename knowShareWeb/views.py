# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import Context, RequestContext 
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth import *
from django.contrib.auth.models import *
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import *
from knowShareWeb.forms import * 
from knowShareWeb.models import *
from knowShareWeb.utils import *

#HTML ACCESS
def main_page(request):
    return render_to_response('index.html', RequestContext(request, permission(request)))

def howto_page(request):
    return render_to_response('howto.html', RequestContext(request, permission(request)))

def teacher_page(request):
    isInGroup = False
    for group in request.user.groups.all():
        if group.name == 'Teacher' or group.name == 'Student':
            isInGroup = True 
    teachers =  Teacher.objects.all()
    for teacher in teachers:
        teacher.career =  teacher.career.replace('\r', '</br>')

    teacherUserRels = []
    idx = 0
    for teacher in teachers:
        teacherUserRels.append(False)
        for teacherrequest in teacher.teacherrequest_set.all():
            if teacherrequest.student == request.user : 
                 teacherUserRels[idx] = True
        idx += 1
        
    if request.user.is_authenticated() == True : 
        teacherRequests = request.user.teacherrequest_set.all()

        return render_to_response('teacher.html', RequestContext(request, addPerm(request, {'isInGroup' : isInGroup, 'teachers' : teachers, 'user' : request.user, 'teacherRequests' : teacherRequests, 'teacherUserRels' : teacherUserRels, "user" : request.user})))
    else :
        return render_to_response('teacher.html', RequestContext(request, addPerm(request, {'isInGroup' : isInGroup, 'teachers' : teachers})))

def teacherSubmit_page(request):
    if request.user.is_authenticated() == False:
        return render_to_response('teacherSubmit.html', RequestContext(request, addPerm(request, {'Confirmed' : 0})))

    try :
        request.user.teacher
    except ObjectDoesNotExist :
        return render_to_response('teacherSubmit.html', RequestContext(request, permission(request)))

    return render_to_response('teacherSubmit.html', RequestContext(request, addPerm(request, {'Confirmed' : 1, 'name' : request.user.teacher.name})))

def student_page(request):
    students = Student.objects.all()
    studentreq = []

    if request.user.is_authenticated() == True : 
        studentRequests = []
        try : 
            studentRequests = request.user.teacher.studentrequest_set.all()
        except ObjectDoesNotExist : 
            return render_to_response('student.html', RequestContext(request, addPerm(request, {'students' : students})))

        for student in students : 
            exist = False
            for studentRequest in studentRequests : 
                if(student.id == studentRequest.student.id) :
                    studentreq.append(True)
                    exist = True
                    
            if exist == False :
                studentreq.append(False)

        return render_to_response('student.html', RequestContext(request, addPerm(request, {'students' : students, 'user' : request.user, 'studentreq' : studentreq})))
    else :
        return render_to_response('student.html', RequestContext(request, addPerm(request, {'students' : students})))

def studentSubmit_page(request):
    if request.user.is_authenticated() == False:
        return render_to_response('studentSubmit.html', RequestContext(request, addPerm(request, {'Confirmed' : 0})))

    return render_to_response('studentSubmit.html', RequestContext(request, permission(request)))

def lecture_page(request):
    #lectures = None
    if request.user.is_authenticated() == False:
            return render_to_response('lecture.html', RequestContext(request, addPerm(request,{'Confirmed' : 0 })))
    try : 
        lectures = request.user.teacher.lecture_set.all()
        return render_to_response('lecture.html', RequestContext(request, addPerm(request,{'lectures' : lectures})))
    except ObjectDoesNotExist :
        return render_to_response('lecture.html', RequestContext(request, permission(request)))

def lectureSubmit_page(request):
    if request.user.is_authenticated() == False:
        return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request, {'months' : range(1, 12), 'Confirmed' : 0})))

    #Teacher Attribute Check 
    try :
        request.user.teacher 
    except ObjectDoesNotExist :
        return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request,{'months' : range(1, 13), 'Confirmed' : 1})))

    studentID = request.GET.get('studentID', '')

    return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request,{'months' : range(1, 13), 'Confirmed' : 2, 'studentID' : studentID})))

def contact_page(request):
    return render_to_response('contact.html', RequestContext(request, permission(request)))

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


    return render_to_response('myProfile.html', RequestContext(request, addPerm(request,{'user' : request.user, 'isTeacher' : isTeacher, 'isStudent' : isStudent, 'careers' : careers })))

def submit_list_page(request):
    studentRequests = None
    try : 
        studentRequests = request.user.teacher.studentrequest_set.all()
        for studentRequest in studentRequests :
            studentRequest.comment = studentRequest.comment.replace('\r', '</br>').replace('\n','')
    except ObjectDoesNotExist : 
        studentRequests = []

    teacherRequests = request.user.teacherrequest_set.all()
    for teacherRequest in teacherRequests :
        teacherRequest.comment = teacherRequest.comment.replace('\r', '</br>').replace('\n','')
    try : 
        students = request.user.student_set.all()
    except ObjectDoesNotExist : 
        students = []
    
    return render_to_response('submitList.html', RequestContext(request, addPerm(request,{'studentRequests' : studentRequests, 'teacherRequests' : teacherRequests})))

def receive_list_page(request):
    studentRequestsToMe = None
    students = None 
    try : 
        studentRequestsToMe = request.user.teacher.teacherrequest_set.all()
        for teacherRequest in studentRequestsToMe :
            teacherRequest.comment = teacherRequest.comment.replace('\r', '</br>').replace('\n','')
    except ObjectDoesNotExist : 
        studentRequestsToMe = []
    try : 
        students = request.user.student_set.all()
        for student in students :
            for studentRequest in student.studentrequest_set.all() :
                studentRequest.comment = studentRequest.comment.replace('\r', '</br>').replace('\n','')

    except ObjectDoesNotExist : 
        students = []
    
    return render_to_response('receiveList.html', RequestContext(request, addPerm(request, {'studentRequestsToMe' : studentRequestsToMe, 'students' : students})))


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
            return render_to_response('index.html', RequestContext(request, addPerm(request,{'loginerror' : True, 'login' : True})))
    else:
        return render_to_response('index.html', RequestContext(request, addPerm(request,{'loginerror' : False, 'login' : True})))
    

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
          return render_to_response('index.html', RequestContext(request, addPerm(request,{'signuperror' : True, 'signup' : True})))
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
        
        # add in TeacherGroup 
        g = Group.objects.get_or_create(name='Teacher')[0]
        request.user.groups.add(g)
        g.save()

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

        # add in StudentGroup 
        g = Group.objects.get_or_create(name='Student')[0]
        request.user.groups.add(g)
        g.save()
        
        return HttpResponseRedirect('/')

def lecture_register_page(request):
    if request.method == 'POST':
        student = None
        try : 
            student =  Student.objects.get(id__exact=request.POST['sid'])
        except : 
            return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request, {'error' : True, 'months' : range(1,13)})))
        

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
        return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request,{'months' : range(1,13)})))

# Request
def teacher_request_page(request):
    if request.method == 'POST' :
        print "request" + request.POST['teacherID']
        teacher = Teacher.objects.get(id__exact=request.POST['teacherID'])
        if int(request.POST['addErase']) == 1 :
            TeacherRequest.objects.create_teacher_request(
                teacher = teacher,
                student = request.user,
                comment = request.POST['comment'],
                permission = 0)
        else :
            teacherRequest = TeacherRequest.objects.get(teacher=teacher, student=request.user)
            teacherRequest.delete()
        
        return HttpResponseRedirect('/teacher')
            
    else :
        return HttpResponseRedirect('/teacher')

def student_request_page(request):
    if request.method == 'POST' : 
        student = Student.objects.get(id__exact=request.POST['studentID'])
        if int(request.POST['addErase']) == 1:
            StudentRequest.objects.create_student_request(
                student = student,
                teacher = request.user.teacher,
                comment = request.POST['comment'],
                permission = 0)
        else :
            studentRequest = StudentRequest.objects.get(student=student, teacher=request.user.teacher)
            studentRequest.delete()
        
        return HttpResponseRedirect('/student')
    else :
        return HttpResponseRedirect('/student')


def teacher_request_permission(request):
    if request.method == 'POST' : 
        student = User.objects.get(id__exact=request.POST['studentID'])
        teacherRequest = TeacherRequest.objects.get(teacher=request.user.teacher, student=student)
        teacherRequest.permission = request.POST['permission']
        teacherRequest.save()
        return HttpResponseRedirect('/receiveList')

def student_request_permission(request):
    if request.method == 'POST' : 
        student = Student.objects.get(id__exact=request.POST['userStudentID'])
        teacher = Teacher.objects.get(id__exact=request.POST['teacherID'])
        studentRequest = StudentRequest.objects.get(student=student, teacher=teacher)
        studentRequest.permission = request.POST['permission']
        studentRequest.save()
        return HttpResponseRedirect('/receiveList')


# Lecture Creation
#def lecture_creation(request):
#    return HttpResponseRidirect('/')
        
        
    


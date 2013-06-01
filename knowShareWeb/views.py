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
from BigBlue.views import *

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

def teacherInfoChange_page(request):
    Teacher = None
    if request.user.is_authenticated() == False:
        return render_to_response('teacherInfoChange.html', RequestContext(request, addPerm(request, {'Confirmed' : 0})))

    try :
        Teacher = request.user.teacher
    except ObjectDoesNotExist :
        return render_to_response('teacherInfoChange.html', RequestContext(request, permission(request)))

    return render_to_response('teacherInfoChange.html', RequestContext(request, addPerm(request, {'name' : Teacher.name, 'age' : Teacher.age, 'highschool' : Teacher.highschool, 'university' : Teacher.university, 'age' : Teacher.age, 'sex' : Teacher.sex, 'career' : Teacher.career, 'money' : Teacher.money, 'tutorTime' : Teacher.tutorTime, 'tutorType' : Teacher.tutorType})))

def student_page(request):
    students = Student.objects.all()
    studentLectureOffers = StudentLectureOffer.objects.all()
    studentreq = []
    if request.user.is_authenticated() == True : 
        studentRequests = []

        try : 
            studentRequests = request.user.teacher.studentrequest_set.all()
        except ObjectDoesNotExist : 
            for studentOffer in studentLectureOffers : 
                print studentOffer.student.name
                studentreq.append(False)
            return render_to_response('student.html', RequestContext(request, addPerm(request, {'students' : studentLectureOffers, 'studentreq' : studentreq, 'user' : request.user})))

        for studentOffer in studentLectureOffers : 
            exist = False
            for studentRequest in studentRequests : 
                if(studentOffer.student.id == studentRequest.student.id) :
                    studentreq.append(True)
                    exist = True
                    
            if exist == False :
                studentreq.append(False)


        return render_to_response('student.html', RequestContext(request, addPerm(request, {'students' : studentLectureOffers, 'user' : request.user, 'studentreq' : studentreq})))
    else :
        return render_to_response('student.html', RequestContext(request, addPerm(request, {'students' : students})))

def studentSubmit_page(request):
    studentLectureOffers = []

    if request.user.is_authenticated() == False:
        return render_to_response('studentSubmit.html', RequestContext(request, addPerm(request, {'Confirmed' : 0})))

    try:
        student = request.user.student;
        studentLectureOffers = request.user.student.studentlectureoffer_set.all()
    except :
        return render_to_response('studentSubmit.html', RequestContext(request, addPerm(request, {'studentLectureOffers' : studentLectureOffers, 'student' : student})))

    return render_to_response('studentSubmit.html', RequestContext(request, addPerm(request, {'studentLectureOffers' : studentLectureOffers, 'student' : student})))

def lecture_page(request):
    #lectures = None
    if request.user.is_authenticated() == False:
            return render_to_response('lecture.html', RequestContext(request, addPerm(request,{'Confirmed' : 0 })))
    try : 
        lectures = []
        if isTeacher(request) : 
            lectures = request.user.teacher.lecture_set.all()
        else  : 
            for student in request.user.student_set.all() : 
                lectures.extend(student.lecture_set.all())                
        runnings = isLectureRunning(['1'])
        return render_to_response('lecture.html', RequestContext(request, addPerm(request,{'lectures' : lectures, 'runnings' : runnings})))
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

    count = request.GET.get('count', 0)
    students = []
    studentID = None 
    studentIDs = []
    for i in range(0, int(count)) :  
        sID = "studentID%02d" % (i+1)
        studentID = request.GET.get(sID, '')
        student  = Studen.objects.get(id__exact=int(studentID))
        studentIDs.append(studentID)
        students.append(student)
    
    sets = [16, 32, 54, 64]
    return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request,{'months' : range(1, 13), 'Confirmed' : 2, 'sets' : sets, 'students' : students, 'count' : count, 'studentIDs' : studentIDs})))

def contact_page(request):
    return render_to_response('contact.html', RequestContext(request, permission(request)))

def my_profile_page(request):
    isTeacherBool = False
    isStudentBool = False
    careers = None
    
    for group in request.user.groups.all():
        if isTeacher(request) :
            isTeacherBool = True
            careers =  request.user.teacher.career.split('\r')
        elif isStudent(request):
            isStudentBool = True


    return render_to_response('myProfile.html', RequestContext(request, addPerm(request,{'user' : request.user, 'isTeacher' : isTeacherBool, 'isStudent' : isStudentBool, 'careers' : careers })))

def submit_list_page(request):
    studentRequests = None
    try : 
        studentRequests = request.user.teacher.studentrequest_set.all()
        for studentRequest in studentRequests :
            studentRequest.comment = studentRequest.comment.replace('\r', '</br>').replace('\n','')
    except : 
        studentRequests = []

    teacherRequests = request.user.teacherrequest_set.all()
    for teacherRequest in teacherRequests :
        teacherRequest.comment = teacherRequest.comment.replace('\r', '</br>').replace('\n','')
    try : 
        students = request.user.student_set.all()
    except : 
        students = []
    
    return render_to_response('submitList.html', RequestContext(request, addPerm(request,{'studentRequests' : studentRequests, 'teacherRequests' : teacherRequests})))

def receive_list_page(request):
    studentRequestsToMe = None
    students = None 
    try : 
        studentRequestsToMe = request.user.teacher.teacherrequest_set.all()
        for teacherRequest in studentRequestsToMe :
            teacherRequest.comment = teacherRequest.comment.replace('\r', '</br>').replace('\n','')
    except :
        studentRequestsToMe = []
    try : 
        students = request.user.student_set.all()
        for student in students :
            for studentRequest in student.studentrequest_set.all() :
                studentRequest.comment = studentRequest.comment.replace('\r', '</br>').replace('\n','')

    except :
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

def teacher_profile_change_page(request):
    if request.method == 'POST' : 
        sex = 0
        if request.POST['sex'] == 'male':
            sex = 0
        else :
            sex = 1

        teacher = Teacher.objects.change_teacher(
            id = request.user.teacher.id,
            name = request.POST['name'],
            highschool = request.POST['highschool'],
            university = request.POST['university'],
            age = request.POST['age'],
            sex = sex,
            career = request.POST['career'],
            money = request.POST['money'],
            tutorTime = request.POST['tutorTimeIdx'],
            tutorType = request.POST['tutorTypeIdx']
        )
        return HttpResponseRedirect('/teacher')



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
            user = request.user
            )

        # add in StudentGroup 
        g = Group.objects.get_or_create(name='Student')[0]
        request.user.groups.add(g)
        g.save()
        
        return HttpResponseRedirect('/studentSubmit')

def student_lecture_offer_page(request):
    if request.method == 'POST' :        
        
        studentLectureOffer = StudentLectureOffer.objects.create(
            money = request.POST['money'],
            tutorTime = request.POST['tutorTimeIdx'],
            comment = request.POST['comment'],
            student = request.user.student
            )
        
        return HttpResponseRedirect('/studentSubmit')

def lecture_register_page(request):
    sets = [16, 32, 48, 64]
    if request.method == 'POST':
        student = None
        try : 
            student =  Student.objects.get(id__exact=request.POST['sid'])
        except : 
            return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request, {'error' : True, 'sets' : sets})))
        

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
        return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request,{'sets' : sets})))

# Request
def teacher_request_page(request):
    if request.method == 'POST' :
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

        
        
    


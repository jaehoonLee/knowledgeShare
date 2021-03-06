# -*- coding: utf-8 -*-
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
from sets import Set

#HTML ACCESS
def main_page(request):
    return render_to_response('index.html', RequestContext(request, permission(request)))

def howto_page(request):
    return render_to_response('howto.html', RequestContext(request, permission(request)))

def teacher_page(request):
    isStuRegistered = True;

    # HTML부분 변경 
    teachers =  Teacher.objects.all()
    for teacher in teachers:
        teacher.career =  teacher.career.replace('\r', '</br>')

    teacherUserRels = []
    idx = 0

    # 선생님께 신청한 부분 구별
    try : 
        if isStudent(request) :
            for teacher in teachers:
                teacherUserRels.append(False)
                for teacherrequest in teacher.teacherrequest_set.all():
                    if teacherrequest.student == request.user.student : 
                        teacherUserRels[idx] = True
                idx += 1
                print teacher.name 
    except : 
        isStuRegistered = False;
        
    # 로그인 되어있는 경우 선생님
    if request.user.is_authenticated() == True :
        teacherRequests = []
        if isStudent(request):
            try :
                teacherRequests = request.user.student.teacherrequest_set.all()
            except : 
                teacherRequests = []

        
        return render_to_response('teacher.html', RequestContext(request, addPerm(request, {'teachers' : teachers, 'user' : request.user, 'teacherUserRels' : teacherUserRels, 'isStuRegistered' : isStuRegistered})))
        
    else :
        return render_to_response('teacher.html', RequestContext(request, addPerm(request, {'teachers' : teachers})))

def teacherSubmit_page(request):
    # 로그인이 되어 있지 않은 경우
    if request.user.is_authenticated() == False:
        return render_to_response('teacherSubmit.html', RequestContext(request, addPerm(request, {'Confirmed' : 0})))

    # 선생님 정보가 있는지 여부 확인
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
    
    return render_to_response('teacherInfoChange.html', RequestContext(request, addPerm(request, {'name' : Teacher.name, 'age' : Teacher.age, 'highschool' : Teacher.highschool, 'university' : Teacher.university, 'age' : Teacher.age, 'sex' : Teacher.sex, 'career' : Teacher.career, 'money' : Teacher.money, 'tutorTime' : Teacher.tutorTime, 'tutorType' : Teacher.tutorType, 'phoneNumber' : Teacher.phoneNumber })))

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
    
    #Login을 안했다면 
    if request.user.is_authenticated() == False:
        return render_to_response('studentSubmit.html', RequestContext(request, addPerm(request, {'Confirmed' : 0})))

    #학생 프로필이 있는지 여부 확인
    student = None
    try:
        student = request.user.student;
        studentLectureOffers = request.user.student.studentlectureoffer_set.all()
    except :
        return render_to_response('studentSubmit.html', RequestContext(request, addPerm(request, {'studentLectureOffers' : studentLectureOffers})))
    
    return render_to_response('studentOfferSubmit.html', RequestContext(request, addPerm(request, {'studentLectureOffers' : studentLectureOffers, 'student' : student})))

def lecture_page(request):
    #lectures = None
    if request.user.is_authenticated() == False:
            return render_to_response('lecture.html', RequestContext(request, addPerm(request,{'Confirmed' : 0 })))
    try : 
        lectures = []
        if isTeacher(request) : 
            lectures = request.user.teacher.lecture_set.all()
        else  : 
            lectures = request.user.student.lecture_set.all()
        
        lectureIDs = []
        for lecture in lectures : 
            lectureIDs.append(lecture.id)
        runnings = isLectureRunning(lectureIDs)
        print runnings
        return render_to_response('lecture.html', RequestContext(request, addPerm(request,{'lectures' : lectures, 'runnings' : runnings, 'user' : request.user})))
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
        student  = Student.objects.get(id__exact=int(studentID))
        studentIDs.append(studentID)
        students.append(student)
    
    allOffer = Set([])
    for offer in request.user.teacher.studentrequest_set.all():
        allOffer.add(offer.student)
    for offer in request.user.teacher.teacherrequest_set.all():
        allOffer.add(offer.student)

    sets = [16, 32, 54, 64]
    return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request,{'months' : range(1, 13), 'Confirmed' : 2, 'sets' : sets, 'students' : students, 'count' : count, 'studentIDs' : studentIDs, 'allOffer' : allOffer})))

def contact_page(request):
    return render_to_response('contact.html', RequestContext(request, permission(request)))

def my_profile_page(request):
    isTeacherBool = False
    isStudentBool = False
    careers = None
    
    for group in request.user.groups.all():
        if isTeacher(request) :
            isTeacherBool = True
            try : 
                careers =  request.user.teacher.career.split('\r')
            except : 
                isTeacherBool = False
        elif isStudent(request):
            isStudentBool = True


    return render_to_response('myProfile.html', RequestContext(request, addPerm(request,{'user' : request.user, 'isTeacherBool' : isTeacherBool, 'isStudentBool' : isStudentBool, 'careers' : careers })))

def submit_list_page(request):
    studentRequests = None
    teacherRequests = None
    try : 
        studentRequests = request.user.teacher.studentrequest_set.all()
        for studentRequest in studentRequests :
            studentRequest.comment = studentRequest.comment.replace('\r', '</br>').replace('\n','')
    except : 
        studentRequests = []
    
    try :
        teacherRequests = request.user.student.teacherrequest_set.all()
        for teacherRequest in teacherRequests :
            teacherRequest.comment = teacherRequest.comment.replace('\r', '</br>').replace('\n','')
    except : 
        teacherRequests = []

    try : 
        students = request.user.student.student_set.all()
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

def admin_page(request):
    return render_to_response('admin.html', RequestContext(request, {"User" : User.objects.all()}))


#Account Setting
@csrf_exempt
def login_page(request):
    if request.method == 'POST' : 
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                if request.POST.has_key('remember') == False:
                    request.session.set_expiry(0)

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
            if int(request.POST['signupType']) == 0 :
                addTeacherType(user)
            else : 
                addStudentType(user)
            
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
            phoneNumber = request.POST['phoneNumber'],
            user = request.user
            )
        
        # add in TeacherGroup 
        g = Group.objects.get_or_create(name='Teacher')[0]
        request.user.groups.add(g)
        g.save()

        return HttpResponseRedirect('/')

def teacher_profile_change_page(request):
    print request.POST['phoneNumber']
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
            tutorType = request.POST['tutorTypeIdx'],
            phoneNumber = request.POST['phoneNumber']
        )
        return HttpResponseRedirect('/teacher')



def student_register_page(request):
    if request.method == 'POST' :        
        sex = 0
        if request.POST['sex'] == 'male':
            sex = 0
        else: 
            sex = 1

        if request.POST['registerType'] == "0" :        
            student = Student.objects.create_student(
            name = request.POST['name'],
            grade = request.POST['gradeIdx'],
            sex = sex,
            phoneNumber = request.POST['phoneNumber'],
            user = request.user
            )
        else :
            student = request.user.student
            student.name = request.POST['name']
            student.grade = request.POST['gradeIdx']
            student.sex = sex
            student.phoneNumber = request.POST['phoneNumber']
            student.save()
        
    return HttpResponseRedirect('/studentSubmit')

def student_lecture_offer_page(request):
    if request.method == 'POST' :        
        if int(request.POST['addErase']) == 1 :
            studentLectureOffer = StudentLectureOffer.objects.create(
                money = request.POST['money'],
                tutorTime = request.POST['tutorTimeIdx'],
                comment = request.POST['comment'],
                student = request.user.student
            )
        else :
            studentLectureOffer = StudentLectureOffer.objects.get(id__exact=request.POST['id'], student=request.user.student)
            studentLectureOffer.delete()
        
        return HttpResponseRedirect('/studentSubmit')

def lecture_register_page(request):
    sets = [16, 32, 48, 64]
    if request.method == 'POST':
        try : 
            students = request.POST.getlist('input[]')
        except : 
            return render_to_response('lectureSubmit.html', RequestContext(request, addPerm(request, {'error' : True, 'sets' : sets})))
        

        lecture = Lecture.objects.create_lecture(
                     teacher = request.user.teacher,
                     students = students,
                     #startDate = request.POST['startDate'],
                     #endDate = request.POST['endDate'],
                     startDate = "2013-01-01",
                     endDate = "2013-01-01",
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
                student = request.user.student,
                comment = request.POST['comment'],
                permission = 0)
        else :
            teacherRequest = TeacherRequest.objects.get(teacher=teacher, student=request.user.student)
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



#TEMP
def temp_lecture_page(request):
    if request.method == 'POST' :
        if request.POST["lectureState"] == "off" : 
            temp_create_meeting(request)
            return render_to_response('tempLecture.html', RequestContext(request, addPerm(request, {'opened' : True})))
        elif request.POST["lectureState"] == "wantOff" :
            return temp_end_meeting(request)
        else : 
            return temp_join_meeting(request.user.username, request.user.username)
        
    else : 
        return render_to_response('tempLecture.html', RequestContext(request, permission(request)))

def temp_lecture_join(request):
    return temp_join_meeting(request.GET["name"], request.GET["meetingID"])

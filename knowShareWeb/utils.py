from knowShareWeb.models import * 

#Permission
def isTeacher(request):
    isTeacher = False
    for group in request.user.groups.all():
        if group.name == 'Teacher' : 
            isTeacher = True
    return isTeacher

def isStudent(request):
    isStudent = False
    for group in request.user.groups.all():
        if group.name == 'Student' : 
            isStudent = True
    return isStudent

def permission(request):
    return {'isTeacher' : isTeacher(request), 'isStudent' : isStudent(request)}

def addTeacherType(user):
    g = Group.objects.get_or_create(name='Teacher')[0]
    user.groups.add(g)
    g.save()

def addStudentType(user):
    g = Group.objects.get_or_create(name='Student')[0]
    user.groups.add(g)
    g.save()


#dict add
def addDict(dict1, dict2):
    dict1.update(dict2)
    return dict1

def addPerm(request, dict):
    return addDict(permission(request), dict)

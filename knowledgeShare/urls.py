from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from knowShareWeb.views import * 
from BigBlue.views import *
from django.views.generic import RedirectView
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', main_page),
    url(r'^howto/', howto_page),
    url(r'^teacher/$', teacher_page),
    url(r'^teacherSubmit/$', teacherSubmit_page),
    url(r'^teacherInfoChange/$', teacherInfoChange_page),                    
    url(r'^student/$', student_page),
    url(r'^studentSubmit/$', studentSubmit_page),
    url(r'^lecture/$', lecture_page),
    url(r'^lectureSubmit/$', lectureSubmit_page),                      
    url(r'^contact/$', contact_page),
    url(r'^myProfile/$', my_profile_page),
    url(r'^submitList/$', submit_list_page),
    url(r'^receiveList/$', receive_list_page),

    # url(r'^knowledgeShare/', include('knowledgeShare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    # Account
    url(r'^register/$', register_page),
    url(r'^logout/$', logout_page),
    url(r'^login/$', login_page),

    # Register
    url(r'^teacherRegister/$', teacher_register_page),
    url(r'^teacherProfileChange/$', teacher_profile_change_page),
    url(r'^studentRegister/$', student_register_page),
    url(r'^lectureRegister/$', lecture_register_page),
    url(r'^studentLectureOffer/$', student_lecture_offer_page),
                       
    # Request
    url(r'^teacherRequest/$', teacher_request_page),
    url(r'^studentRequest/$', student_request_page),

    url(r'^teacherRequestPermission/$', teacher_request_permission),
    url(r'^studentRequestPermission/$', student_request_permission),

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/img/favicon.ico', permanent=False)),

    # BigBlue
    url(r'^createMeeting/$', create_meeting),
    url(r'^endMeeting/$', end_meeting),
    url(r'^joinMeeting/$', join_meeting),
    url(r'^isMeetingRunning/$', isMeetingRunning),
    url(r'^getMeetingInfo/$', getMeetingInfo),
    url(r'^getMeetings/$', getMeetings),

)

urlpatterns += staticfiles_urlpatterns()

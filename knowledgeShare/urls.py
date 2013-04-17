from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from knowShareWeb.views import * 
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', main_page),
    url(r'^howto/', howto_page),
    url(r'^teacher/$', teacher_page),
    url(r'^teacherSubmit/$', teacherSubmit_page),
    url(r'^student/$', student_page),
    url(r'^studentSubmit/$', studentSubmit_page),
    url(r'^lecture/$', lecture_page),
    url(r'^lectureSubmit/$', lectureSubmit_page),                      
    url(r'^contact/$', contact_page),
    url(r'^myProfile/$', my_profile_page),
    url(r'^submitList/$', submit_list_page),

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
    url(r'^studentRegister/$', student_register_page),
    url(r'^lectureRegister/$', lecture_register_page),
                       
    # Request
    url(r'^teacherRequest/$', teacher_request_page),
    url(r'^studentRequest/$', student_request_page),
)

urlpatterns += staticfiles_urlpatterns()

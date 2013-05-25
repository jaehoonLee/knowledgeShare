from django.shortcuts import render
from BigBlue.utils import *
from django.http import HttpResponseRedirect

# Create your views here.
def create_meeting(request):
    print checksum('create', 'createName=Test')
    return HttpResponseRedirect('http://1.226.82.11:8002/bigbluebutton/api/create')

from django.shortcuts import render
from BigBlue.utils import *
from django.http import HttpResponseRedirect

# Create your views here.
def create_meeting(request):
    query = 'name=TEST&meetingID=1&attendeePW=1&moderatorPW=1'
    checksumPar =  checksum('create',query)
    return HttpResponseRedirect('http://1.226.82.11/bigbluebutton/api/create?' + query + '&checksum=' + checksumPar)

def join_meeting(request):
    query = 'fullName=TEST&meetingID=1&password=1'
    checksumPar = checksum('join', query)
    return HttpResponseRedirect('http://1.226.82.11/bigbluebutton/api/join?' + query + '&checksum=' + checksumPar)

def end_meeting(request):
    query = 'meetingID=1&password=1'
    checksumPar = checksum('end', query)
    return HttpResponseRedirect('http://1.226.82.11/bigbluebutton/api/end?' + query + '&checksum=' + checksumPar)

    

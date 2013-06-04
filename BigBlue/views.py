# -*- coding: utf-8 -*-
from django.shortcuts import render
from BigBlue.utils import *
from django.http import HttpResponseRedirect
from xml.dom.minidom import parseString
import requests
import urllib

#Http Request with BBB
def create_meeting(request):
    name = request.POST['name']
    meetingID = request.POST['lectureID']
    parameters = {'name': safe_str(name),
                  'meetingID' : safe_str(meetingID),
                  'attendeePW' : safe_str(1),
                  'moderatorPW' : safe_str(1),
#                  'voiceBridge' : safe_str(voiceBridge),
#                  'logoutURL' : safe_str(logoutURL),
                  }

    parameters = urllib.urlencode(parameters)

#    return HttpResponseRedirect(getBBBURL('create', parameters))
    resp = requests.get(getBBBURL('create', parameters))
    return join_meeting(request)

def end_meeting(request):
    meetingID = request.POST['lectureID']
    parameters = {'meetingID' : safe_str(meetingID),
                  'password' : safe_str(1),
                 }
    parameters = urllib.urlencode(parameters)
    #return HttpResponseRedirect(getBBBURL('end', parameters))
    resp = requests.get(getBBBURL('end', parameters))
    return HttpResponseRedirect('/lecture')

def join_meeting(request):
    name = request.POST['name']
    meetingID = request.POST['lectureID']
    query = 'fullName=' + name + '&meetingID=' + request.POST['lectureID'] + '&password=1'
    parameters = {'meetingID' : safe_str(meetingID),
                  'fullName' : safe_str(name),
                  'password' : safe_str(1),
                  }

    parameters = urllib.urlencode(parameters)
    return HttpResponseRedirect(getBBBURL('join', parameters))

def isMeetingRunning(request):
    query = 'meetingID=1'
    resp = requests.get(getBBBURL('isMeetingRunning', query))
    dom = parseString(resp.text)
    response = dom.getElementsByTagName('response')
    running = response[0].getElementsByTagName('running')
    print running[0].firstChild.data
    return HttpResponseRedirect(getBBBURL('isMeetingRunning', query))

def getMeetingInfo(request):
    query = 'meetingID=1&password=1'
    return HttpResponseRedirect(getBBBURL('getMeetingInfo', query))

def getMeetings(request):
    query = ''
    return HttpResponseRedirect(getBBBURL('getMeetings', query))


#Userful API for BBB        
def isLectureRunning(meetingIDs):
    runnings = []
    for meetingID in meetingIDs :
        try : 
            resp = requests.get(getBBBURL('isMeetingRunning', 'meetingID=' + str(meetingID)))
            dom = parseString(resp.text)
            response = dom.getElementsByTagName('response')
            running = response[0].getElementsByTagName('running')
            if running[0].firstChild.data  == 'true':
                runnings.append(True)
            else : 
                runnings.append(False)
        except : 
            runnings.append(False)
    return runnings



def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        return unicode(obj).encode('UTF-8')

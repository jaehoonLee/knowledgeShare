from django.shortcuts import render
from BigBlue.utils import *
from django.http import HttpResponseRedirect
from xml.dom.minidom import parseString
import requests

#Http Request with BBB
def create_meeting(request):
    query = 'name=TEST&meetingID=1&attendeePW=1&moderatorPW=1'
    return HttpResponseRedirect(getBBBURL('create', query))

def end_meeting(request):
    query = 'meetingID=1&password=1'
    return HttpResponseRedirect(getBBBURL('end', query))

def join_meeting(request):
    query = 'fullName=TEST&meetingID=1&password=1'
    return HttpResponseRedirect(getBBBURL('join', query))

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
        resp = requests.get(getBBBURL('isMeetingRunning', 'meetingID=' + meetingID))
        dom = parseString(resp.text)
        response = dom.getElementsByTagName('response')
        running = response[0].getElementsByTagName('running')
        if running[0].firstChild.data  == 'true':
            runnings.append(True)
        else : 
            runnings.append(False)
    return runnings





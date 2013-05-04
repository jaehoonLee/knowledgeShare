from django.shortcuts import render
from BigBlue.utils import *
from django.http import HttpResponseRedirect

# Create your views here.
def create_meeting(request):
    print checksum('a', 'b', 'c')
    return HttpResponseRedirect('/')
    

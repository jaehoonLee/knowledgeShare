# -*- coding: utf-8 -*-
from django.conf import settings 
from hashlib import sha1

def checksum(call, query):
    prepared = "%s%s%s" % (call, query, settings.SALT)
#    checksum = sha1(prepared).hexdigest()
    checksum = sha1(prepared.encode('utf-8')).hexdigest()
    return checksum

def getBBBURL(call, query):
    checksumPar = checksum(call, query)
    return 'http://1.226.82.11/bigbluebutton/api/' + call + '?' + query + '&checksum=' + checksumPar

from django.conf import settings 
from hashlib import sha1

def checksum(call, query):
    prepared = "%s%s%s" % (call, query, settings.SALT)
    checksum = sha1(prepared).hexdigest()
    return checksum

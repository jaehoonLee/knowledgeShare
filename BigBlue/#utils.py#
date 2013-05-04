from hashlib import sha1

def checksum(call, query, salt):
    prepared = "%s%s%s" % (call, query, salt)
    checksum = sha1(prepared).hexdigest()
    return checksum

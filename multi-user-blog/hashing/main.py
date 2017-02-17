import hashlib
import hmac

SECRET = 'imsosecret'

def hash_str(s):


def make_secure_val(s):
	return "%s|%s" % (s, hash_str(S))

def check_secure_val(h):
	val = h.split('|')[0]
	if h == make_secure_val(val):
		return val
# utils.py
from __future__ import print_function
from functools import wraps
from decimal import Decimal
import os
import logging
import json
log = logging.getLogger()
log.setLevel(logging.DEBUG)

class DecimalEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Decimal):
			# depending on the application
			# we might want this as a string
			return float(obj)
		return super(DecimalEncoder, self).default(obj)

def undecimalify(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            event, context = args 
            log.info(str(context))
            response = f(*args, **kwargs)
        except Exception as e:
            log.error("General failure: %s" % e)
            response = None

        if response is None:
        	return
        if 'isBase64Encoded' not in response:
        	response['isBase64Encoded'] = False
        if 'headers' not in response:
        	response['headers'] = {}
        if 'body' in response:
        	response['body'] = json.dumps(response['body'], cls=DecimalEncoder)
        return response
    return wrapper


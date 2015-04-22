from __future__ import absolute_import
from django_twilio.decorators import twilio_view
from twilio.rest import TwilioRestClient
from twilio.twiml import Response
from .settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from celery import task
from .api import *

@task()
def ivr_outbound_call(to_number, time_delay=0):
    message = "success"
    print type(to_number)
    if isinstance(to_number, unicode):
    	to_number = to_number
    else:
    	to_number = "+"+str(to_number.country_code)+str(to_number.national_number)
    
    print time_delay, to_number
    print 'time delay done'
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    try:
    # Make the call
        call = client.calls.create(to=to_number, from_="+18329245668", url="https://2605c80f.ngrok.io/gather/")
        save_call_record(to_number, call.sid, time_delay)
    except Exception as e:
        message='error'
    return message
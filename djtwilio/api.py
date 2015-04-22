from django.core import serializers
from .models import IVRCall
from django.http import HttpResponse

def save_call_record(phone_number, call_sid, time_delay):
    try:
        call_record = IVRCall(phone_number=phone_number, time_delay = time_delay, call_sid = call_sid, call_state='Incomplete')
        call_record.save()
        print call_record.id, 'record saved'
    except Exception as e:
        print 'exception in saving call record', e

def update_call_record(phone_number, call_sid, digits):
    try:
        call_record = IVRCall.objects.get(phone_number=phone_number, call_sid = call_sid, call_state='Complete')
        call_record.digit_entered = digits
        call_record.save()
        print call_record.id, 'record updated with time delay'
    except Exception as e:
        print 'exception in updating call record', e

def call_records_json(request):
    calls = IVRCall.objects.all()
    data = serializers.serialize("json", calls)
    return HttpResponse(data, content_type='application/json')
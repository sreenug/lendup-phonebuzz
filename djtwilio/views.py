# -*- coding: utf-8 -*-
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect

from .forms import NameForm, Phase3Form
from .models import IVRCall
from twilio.rest import TwilioRestClient
from settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
import time

import json
from django.http import HttpResponse
from django.core import serializers

def home(request):
    # home page loading..Final Phase
    return render_to_response('home.html')

def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            phone_number = form.cleaned_data['phone_number']
            sid = make_outbound_call(phone_number)
            return HttpResponseRedirect('/fizzbuzz')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()

    return render(request, 'name.html', {'form': form})

def make_call(request):
    # Going to make a call
    if request.method == 'GET':
        # create a form instance and populate it with data from the request:
        phone_number = request.GET['phone_number']
        time_delay = request.GET['time_delay']
        print 'make call',phone_number, time_delay
        sid = make_outbound_call(phone_number, int(time_delay))
        return HttpResponse('Call successfully placed')


def phase3(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = Phase3Form(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            phone_number = form.cleaned_data['phone_number']
            time_delay = form.cleaned_data['time_delay']
            print phone_number, time_delay
            sid = make_outbound_call(phone_number, time_delay)
            return HttpResponseRedirect('/phase3')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = Phase3Form()

    return render(request, 'name.html', {'form': form})

def make_outbound_call(to_number, time_delay=0):
    print type(to_number)
    if isinstance(to_number, unicode):
    	to_number = to_number
    else:
    	to_number = "+"+str(to_number.country_code)+str(to_number.national_number)
    
    print time_delay, to_number
    time.sleep(time_delay)
    print 'time delay done'
    
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    # Make the call
    call = client.calls.create(to=to_number,  # Any phone number
                           from_="+18329245668", # Must be a valid Twilio number
                          url="https://2605c80f.ngrok.io/gather/")
    ##Save call in Database
    save_call_record(to_number, call.sid, time_delay)
    return call.sid


def save_call_record(phone_number, call_sid, time_delay):
    try:
        call_record = IVRCall(phone_number=phone_number, time_delay = time_delay, call_sid = call_sid)
        call_record.save()
        print call_record.id, 'record saved'
    except Exception as e:
        print 'exception in saving call record', e

def update_call_record(phone_number, call_sid, digits):
    try:
        call_record = IVRCall.objects.get(phone_number=phone_number, call_sid = call_sid)
        call_record.digit_entered = digits
        call_record.save()
        print call_record.id, 'record updated with time delay'
    except Exception as e:
        print 'exception in updating call record', e

def call_records_json(request):
    calls = IVRCall.objects.all()
    data = serializers.serialize("json", calls)
    return HttpResponse(data, content_type='application/json')

def previous_call(request):
    call_id = request.GET['id']
    call_object = IVRCall.objects.get(pk = call_id)
    to_number = call_object.phone_number
    digit_entered = call_object.digit_entered
    print 'in previous call func', to_number, digit_entered
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    # Make the call
    call = client.calls.create(to=to_number,  # Any phone number
                           from_="+18329245668", # Must be a valid Twilio number
                          url="https://2605c80f.ngrok.io/replay/?digits="+str(digit_entered))
    return HttpResponse('success')

@twilio_view
def handle_replay_message(request):
    digits = request.GET['digits']
    print 'through replay',digits

    msg = get_fizzbuzz_message(int(digits))

    twilio_response = Response()
    twilio_response.say(msg)

    return twilio_response

@twilio_view
def gather_digits(request):

    msg = 'Oye. Press a number to enter the world of Fizz Buzz'

    twilio_response = Response()
    with twilio_response.gather(action='/respond/', numDigits=1) as g:
        g.say(msg)
        g.pause(length=1)
        g.say(msg)

    return twilio_response


@twilio_view
def handle_response(request):

    digits = request.POST.get('Digits', '')
    to_number = request.POST.get('To', '')
    call_sid = request.POST.get('CallSid', '')
    print 'digits', digits, to_number, call_sid

    twilio_response = Response()
    return_message = get_fizzbuzz_message(int(digits))
    print return_message
    twilio_response.say(return_message)
    update_call_record(to_number, call_sid, digits)

    return twilio_response

def get_fizzbuzz_message(number):
    message = " "
    for num in xrange(number,0,-1):
        if num % 5 == 0 and num % 3 == 0:
            msg = "FizzBuzz "
        elif num % 3 == 0:
            msg = "Fizz "
        elif num % 5 == 0:
            msg = "Buzz "
        else:
            msg = str(num) + " "
        message = msg + message
    return message
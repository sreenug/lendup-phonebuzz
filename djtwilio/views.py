# -*- coding: utf-8 -*-
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from django.shortcuts import render
from django.http import HttpResponseRedirect

from .forms import NameForm, Phase3Form
from twilio.rest import TwilioRestClient
from settings import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
import time


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
    print time_delay, str(to_number), "+"+str(to_number.country_code)+str(to_number.national_number)
    time.sleep(time_delay)
    print 'time delay done'
    to_number = "+"+str(to_number.country_code)+str(to_number.national_number)
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
    
    # Make the call
    call = client.calls.create(to=to_number,  # Any phone number
                           from_="+18329245668", # Must be a valid Twilio number
                          url="https://49777df2.ngrok.io/gather/")
    ##Save call in Database
    return call.sid

@twilio_view
def gather_digits(request):

    msg = 'Ahoy. Press a number to enter the world of Fizz Buzz'

    twilio_response = Response()
    with twilio_response.gather(action='/respond/', numDigits=1) as g:
        g.say(msg)
        g.pause(length=1)
        g.say(msg)

    return twilio_response


@twilio_view
def handle_response(request):

    digits = request.POST.get('Digits', '')
    print 'digits', digits

    twilio_response = Response()
    return_message = get_fizzbuzz_message(int(digits))
    print return_message
    twilio_response.say(return_message)

    # if digits == '1':
    #     twilio_response.play('http://bit.ly/phaltsw')

    # if digits == '2':
    #     number = request.POST.get('From', '')
    #     twilio_response.say('A text message is on its way')
    #     twilio_response.sms('You looking lovely today!', to=number)

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
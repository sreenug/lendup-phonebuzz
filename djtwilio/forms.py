from django import forms
from phonenumber_field.formfields import PhoneNumberField

class NameForm(forms.Form):
	phone_number = forms.CharField(label='Enter Phone Number', min_length=10, max_length=10)

class Phase3Form(forms.Form):
	phone_number = PhoneNumberField(label='Enter Phone Number', help_text='(Please Include country code. EX:+15712017611)')
	time_delay = forms.IntegerField(label='Enter Time Delay in Seconds', initial=0)
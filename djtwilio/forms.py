from django import forms
from phonenumber_field.formfields import PhoneNumberField

class PhoneForm(forms.Form):
	phone_number = PhoneNumberField(label='Enter Phone Number', help_text='(Please Include country code. EX:+15712017611 or enter number in E.164 format)')

class Phase3Form(forms.Form):
	phone_number = PhoneNumberField(label='Enter Phone Number', help_text='(Please Include country code. EX:+15712017611 or enter number in E.164 format)')
	time_delay = forms.IntegerField(label='Enter Time Delay in Seconds', initial=0)
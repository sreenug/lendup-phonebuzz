from django import forms

class NameForm(forms.Form):
	phone_number = forms.CharField(label='Enter Phone Number', max_length=10)
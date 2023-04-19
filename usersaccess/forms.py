from django import forms
from django.forms import ModelForm
from .models import wills, TestChange


#comapny details form to fill in
class wills_form(ModelForm):
	class Meta:
		model=wills
		fields = ['will_owner','excutor','lawyer','will']

class newWillForm(ModelForm):
	class Meta:
		model=TestChange
		fields = ['will_owner', 'excutor', 'lawyer', 'my_field']
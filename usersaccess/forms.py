from django import forms
from django.forms import ModelForm
from .models import wills, TestChange
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

#comapny details form to fill in
class wills_form(ModelForm):
	class Meta:
		model=wills
		fields = ['will_owner','excutor','lawyer','will']

class newWillForm(ModelForm):
	class Meta:
		model=TestChange
		fields = ['will_owner', 'excutor', 'lawyer', 'my_field', 'dc_image']


class RegisterForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=150)
	last_name = forms.CharField(max_length=150)
	# is_staff = forms.BooleanField()
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class RegisterLawyerForm(UserCreationForm):
	email = forms.EmailField()
	first_name = forms.CharField(max_length=150)
	last_name = forms.CharField(max_length=150)
	is_staff = forms.BooleanField()
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'is_staff','password1', 'password2']



class dCertForm(ModelForm):
	class Meta:
		model=TestChange
		fields = ['dc_image']
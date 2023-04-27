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

		widgets = {
            'will_owner': forms.Select(attrs={'class': 'form-control'}),
            'excutor': forms.Select(attrs={'class': 'form-control'}),
            'lawyer': forms.Select(attrs={'class': 'form-control'}),
            # 'my_field': forms.TextInput(attrs={'class': 'form-control'}),
            'dc_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }
class RegisterLawyerForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
	first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
	last_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
	is_staff = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), required=False)
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email', 'is_staff','password1', 'password2']

		widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }



class dCertForm(ModelForm):
	class Meta:
		model=TestChange
		fields = ['dc_image']

		widgets = {
            'dc_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }



# class LoginForm(AuthenticationForm):
#     username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
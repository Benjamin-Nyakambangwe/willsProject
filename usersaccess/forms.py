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

# class newWillForm(ModelForm):
# 	class Meta:
# 		model=TestChange
# 		fields = ['will_owner', 'excutor', 'lawyer', 'my_field', 'dc_image']

# 		widgets = {
#             'will_owner': forms.Select(attrs={'class': 'form-control'}),
#             'excutor': forms.Select(attrs={'class': 'form-control'}),
#             'lawyer': forms.Select(attrs={'class': 'form-control'}),
#             # 'my_field': forms.TextInput(attrs={'class': 'form-control'}),
#             'dc_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
#         }


from django.contrib.auth import get_user_model
# from myapp.models import MyProfileModel

User = get_user_model()
from django.db.models import Q

class newWillForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(newWillForm, self).__init__(*args, **kwargs)
        
        # Filter the will_owner select field
        self.fields['will_owner'].queryset = User.objects.filter(
            Q(userprofile__is_witness=False) | Q(userprofile__is_witness__isnull=True),
            is_active=True,
            is_staff=False,
            
        )
        
        # Filter the excutor select field
        self.fields['excutor'].queryset = User.objects.filter(
            is_active=True,
            is_staff=False,
            userprofile__is_witness=True
        )
        
        # Filter the lawyer select field
        self.fields['lawyer'].queryset = User.objects.filter(
            is_active=True,
            is_staff=True,
            # myprofilemodel__is_lawyer=True
        )

    class Meta:
        model = TestChange
        fields = ['will_owner', 'excutor', 'lawyer', 'my_field', 'dc_image']

        widgets = {
            'will_owner': forms.Select(attrs={'class': 'form-control'}),
            'excutor': forms.Select(attrs={'class': 'form-control'}),
            'lawyer': forms.Select(attrs={'class': 'form-control'}),
            # 'my_field': forms.TextInput(attrs={'class': 'form-control'}),
            'dc_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ownerSignWillForm(ModelForm):
	class Meta:
		model=TestChange
		fields = ['will_owner_sign']

		widgets = {
            'will_owner_sign': forms.TextInput(attrs={'class': 'form-control'}),

        }

class executorSignWillForm(ModelForm):
	class Meta:
		model=TestChange
		fields = ['executor_sign']

		widgets = {
            'executor_sign': forms.TextInput(attrs={'class': 'form-control'}),

        }


class lawyerSignWillForm(ModelForm):
	class Meta:
		model=TestChange
		fields = ['lawyer_sign']

		widgets = {
            'lawyer_sign': forms.TextInput(attrs={'class': 'form-control'}),

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


class RegisterExecutorForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['last_name'].initial = 'Witness'  # Set the initial value of last_name to 'Doe'
        self.fields['last_name'].widget = forms.HiddenInput()  # Hide the last_name field in the template
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        
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
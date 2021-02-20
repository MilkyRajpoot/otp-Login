from django import forms  
from . models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
from crispy_forms.helper import FormHelper

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, required=True)
    mobile = forms.CharField(min_length=10,max_length=12,required=True)
    email = forms.EmailField(max_length=255,required=True)

    class Meta:
        model = User
        fields = ('username', 'email','mobile','password1', 'password2')

    widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter School-Code','class':'form-control'}),
            'email': forms.TextInput(attrs={'placeholder': 'Enter User-Id','class':'form-control'}),
            'password1': forms.TextInput(attrs={'placeholder': 'Enter School-Code','class':'form-control'}),
            'password2': forms.TextInput(attrs={'placeholder': 'Enter School-Code','class':'form-control'}),
            'mobile': forms.Textarea(attrs={'cols':10,'rows':5,'placeholder': 'Enter Your Feedback','class':'form-control'}),
        }

class OTP_Verification(forms.ModelForm):
    otp = forms.CharField(max_length=6,required=True)

    class Meta:
        model = Email_verification
        fields = ('otp',)

class OTP_Login(forms.ModelForm):
    email = forms.EmailField(max_length=255,required=True)
    otp = forms.CharField(max_length=6,required=True)

    class Meta:
        model = Email_verification
        fields = ('email','otp',)

from django import forms
from django.contrib.auth.models import User
from app.models import MyUser
from django.contrib.auth.forms import UserCreationForm
		
from registration.forms import RegistrationFormUniqueEmail
class MyRegForm(RegistrationFormUniqueEmail):
    first_name = forms.CharField(max_length=30, required=True)
    phone_number = forms.CharField(max_length=50, required=True)
    
    class Meta:
        model = MyUser
        fields = ['email','first_name','phone_number']

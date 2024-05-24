from .models import *
from django import forms
    

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        
        fields =['username','email','password']
        
class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['email','password']
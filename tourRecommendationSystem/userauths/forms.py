from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"password"}))

    
    class Meta:
        
        model = User
        fields = ['username', 'email', 'password']




		
		



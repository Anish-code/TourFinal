from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError 
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Enter Password"}))
    password2 = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Conform Password"}))
    

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError("Invalid email address")
        return email

    class Meta:
        model = User
        fields = ['username', 'email']
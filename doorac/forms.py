from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Log, Door, Tag

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", required=True, max_length=30, widget=forms.TextInput(attrs={'name': 'username'}))
    password = forms.CharField(label="Password", required=True, max_length=30, widget=forms.PasswordInput(attrs={'name': 'password'}))

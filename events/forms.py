from django import forms
from .models import Event
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'location']

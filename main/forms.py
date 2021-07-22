import json
from django import forms
from django.forms import ModelForm
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils.dateparse import parse_duration
from datetime import timedelta
from .models import User

PERIOD_CHOICES = (
    (timedelta(minutes=1), '1 minute'),
    (timedelta(hours=1), '1 hour'),
    (timedelta(hours=3), '3 hour'),
    (timedelta(hours=6), '6 hour'),
    (timedelta(hours=12), '12 hour')
)

NOTIFICATIONS_CHOICES = (
    (True, 'Yes'),
    (False, 'No')
)


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = '__all__'


class RegistrationForm(ModelForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}))

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def save(self, commit=True):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email']
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.save()
        return new_user, password


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

    fields = ['username', 'password']

    def sign_in(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        user = authenticate(username=username, password=password)
        return user, password


class SearchForm(forms.Form):
    city = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Searched City'}))

    fields = ['city']


class PeriodForm(forms.Form):
    period = forms.ChoiceField(choices=PERIOD_CHOICES, label="Choice period")
    notifications = forms.ChoiceField(choices=NOTIFICATIONS_CHOICES)

    fields = ['period', 'notifications']

    def edit(self, pk):
        user = User.objects.get(id=pk)
        user.period = parse_duration(self.cleaned_data['period'])
        user.notifications = json.loads(
            self.cleaned_data['notifications'].lower())
        user.save()
        return user

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password')


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('profile_pic',)

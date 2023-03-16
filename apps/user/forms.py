from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from apps.user.models import User


class UserLoginForm(AuthenticationForm):
    username_or_email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    password = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form__input'}))

    class Meta:
        model = User
        fields = ('username_or_email', 'password')


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form__input'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form__input'}))
    password1 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form__input'}))
    password2 = forms.CharField(strip=False, widget=forms.PasswordInput(attrs={'class': 'form__input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       AuthenticationForm)
from .models import User


class UserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = User
        fields = ('email',)


class UserChangeForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ('date_joined',)


class PrettyAuthenticationForm(AuthenticationForm):
    '''
    Default authentication form with widgets
    '''
    username = forms.CharField(
        label='Адрес электронной почты:',
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(
        label='Пароль:',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}))

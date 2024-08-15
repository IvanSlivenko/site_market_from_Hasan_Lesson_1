from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import *

class LoginForm(AuthenticationForm):
    """Аутентифікація користувача"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': "Ім'я користувача"
                                                             }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'placeholder': "Пароль"
                                                             }))
    
class RegistrationForm(UserCreationForm):
    """Реєстрація користувача"""



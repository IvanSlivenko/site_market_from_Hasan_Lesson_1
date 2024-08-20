from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserModel

from .models import Category, Product, Gallery, Review

class LoginForm(AuthenticationForm):
    """Аутентифікація користувача"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',                                                      
                                                             'placeholder': "Ім'я користувача" }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'placeholder': "Пароль"
                                                             }))
    
class RegistrationForm(UserCreationForm):
    """Реєстрація користувача"""
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'placeholder': "Пароль"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                             'placeholder': "Підтвердіть Пароль"}))
    class Meta:
        model = UserModel
        fields = ('username', 'email')
        widgets= {
            'username': forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': "Ім'я користувача"
                                                             }),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': "Введіть пошту"})                                                              
        }
class FeedbackForm(AuthenticationForm):
    """Зворотній зв'язок"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',                                                      
                                                             'placeholder': "Ім'я користувача" }))

    text_feedback = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                             'placeholder': "Напишіть відгук"   
                                                             }))
    
    number_phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                             'placeholder': "Номер телефону"   
                                                             }))
    
class ReviewForm(forms.ModelForm):
    """Форма для відгуків"""
    class Meta:
        model = Review
        fields = ('text','grade',)
        widgets= {
            'text': forms.Textarea(attrs={'class': 'form-control',
                                            'placeholder': "Ваш відгук для нас важливий"
                                            }),
            'grade': forms.Select(attrs={'class': 'form-control',
                                            'placeholder': "Ваша оцінка"
                                            }),                                           
        }



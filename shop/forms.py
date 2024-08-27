from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserModel

from .models import Category, Product, Gallery, Review, Emails, Customer, \
Order, OrderProduct, ShippingAddress


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

class CustomerForm(forms.ModelForm):
    """Контактна інформація"""
    class Meta:
        model = Customer
        fields = {
            'first_name',
            'last_name',
            'email',
            'phone',

            }
        widgets={
            'first_name': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': "Ваше ім'я"
                                            }),
            'last_name': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': "Ваше прізвище"
                                            }),
            'email': forms.EmailInput(attrs={'class': 'form-control',
                                            'placeholder': "Ваш email"
                                            }),
            'phone': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': "Ваш номер телефону"
                                            }),                                                                 

            }

class ShippingForm(forms.ModelForm):
    """Адреса доставки"""

    class Meta:
        model = ShippingAddress
        fields = (
            'sity',
            'state',
            'street',
        )
        widgets={
            'sity': forms.Select(attrs={'class': 'form-control',
                                            'placeholder': "Місто"}), 
            'state': forms.Select(attrs={'class': 'form-control',
                                'placeholder': "Район"}), 
            'street': forms.TextInput(attrs={'class': 'form-control',
                                            'placeholder': "Вулиця/Будинок/Квартира"
                                            }),                                                     
        }
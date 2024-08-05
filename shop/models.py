from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Назва категорії')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Зображення')
    

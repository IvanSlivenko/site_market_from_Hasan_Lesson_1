from django.shortcuts import render, redirect
from  django.views.generic import ListView, DetailView

from .models import Category, Product

class Index(ListView):
    """Головна сторінка"""
    model = Product
    extra_context = {'title': 'Головна сторінка'}
    template_name = 'shop/index.html'





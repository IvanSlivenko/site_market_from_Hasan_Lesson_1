from django.shortcuts import render, redirect
from  django.views.generic import ListView, DetailView

from .models import Category, Product

class Index(ListView):
    """Головна сторінка"""
    model = Product
    context_object_name = 'categories'
    extra_context = {'title': 'Головна сторінка'}
    template_name = 'shop/index.html'

    def get_queryset(self):
        """render батьківської категорії"""
        categories = Category.objects.filter(parent=None)
        return categories
    
class SubCategories(ListView):
    """Вивід підкатегорії на окремій сторінці"""
    model = Product
    context_object_name = 'products'
    template_name = 'shop/category_page.html'

    def get_queryset(self):
        """Отримання  всіх товарі підкатегорії"""
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subcategories.all()
        products = Product.objects.filter(category__in = subcategories).order_by('?')
        return products










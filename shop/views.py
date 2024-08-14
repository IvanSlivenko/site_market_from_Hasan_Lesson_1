from typing import Any
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
    def get_context_data(self, **kwargs):
        """Виведення на сторінку додаткових елементів"""
        context = super().get_context_data() # context = {}
        context['top_products'] = Product.objects.order_by('-watched')[:8]
        return context
    
class SubCategories(ListView):
    """Вивід підкатегорії на окремій сторінці"""
    model = Product
    context_object_name = 'products'
    template_name = 'shop/category_page.html'

    def get_queryset(self):
        """Отримання  всіх товарі підкатегорії"""
        type_fild = self.request.GET.get('type')
        if type_fild:
            products = Product.objects.filter(category__slug=type_fild)
            return products


        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        subcategories = parent_category.subcategories.all()
        products = Product.objects.filter(category__in = subcategories).order_by('?')

        sort_field = self.request.GET.get('sort')
        if sort_field:
            products = products.order_by(sort_field)
            



        return products
    
    def get_context_data(self, **kwargs):
        """Додаткові елементи"""
        context = super().get_context_data() # context = {}
        parent_category = Category.objects.get(slug=self.kwargs['slug'])
        context['category'] = parent_category
        context['title'] = parent_category.title
        return context
     
class ProductPage(DetailView):
    """Вивід товара на окремій сторінці"""

    model = Product

    context_object_name = 'product'
    template_name = 'shop/product_page.html'










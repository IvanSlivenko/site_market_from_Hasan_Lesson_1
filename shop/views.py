from random import randint
from typing import Any
from django.shortcuts import get_object_or_404, render, redirect
from  django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages

from .models import Category, Product
from .forms import FeedbackForm, LoginForm, RegistrationForm, ReviewForm

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

    def get_context_data(self, **kwargs):
       """Вивід на сторінку додаткових елементів"""

       context = super().get_context_data()
       
       product = Product.objects.get(slug=self.kwargs['slug'])
       context['title'] = product.title
       
       products = Product.objects.filter(category=product.category)

       data = []
       for i in range(5):
           random_index = randint(0, len(products) - 1)
           random_product = products[random_index]
           if random_product not in data and str(random_product) != product.title:
               data.append(random_product)
           

           
       context['products'] = data
       
       if self.request.user.is_authenticated:
           context['review_form'] = ReviewForm


       return context
    

def login_registration(request):
    context= {'title': 'Увійти чи зареєструватись',
              'login_form': LoginForm,
              'registration_form': RegistrationForm
              }

    return render (request, 'shop/login_requestion.html', context)

def feedback(request):
    context= {'title': 'Відправити відгук',
              'feedback_form': FeedbackForm,

              }

    return render (request, 'shop/feed_back.html', context)



def user_login(request):
    """Аутентифікація користувача"""
    form = LoginForm(data=request.POST)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('index')
    else:
        messages.error(request, "Перевірте ім'я та пароль" )    
        return redirect('login_registration')



def user_logout(request):
    """Вихід користувача"""
    logout(request)
    return redirect('index')
           
def user_registration(request):
    """Регістрація користувача"""
    form = RegistrationForm(data = request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, 'Акаунт користувача успішно створено')
    else:
        for error in form.errors:
            messages.error(request, form.errors[error].as_text())

        
            
        # messages.error(request, 'Перевірте поля форми') 

    return redirect('login_registration')




def save_review(request, product_pk):
    """Збереження  відгука"""
    form = ReviewForm(data=request.POST)
    if form.is_valid():
        review = form.save(commit=False)
        review.author=request.user
        product = Product.objects.get(pk=product_pk)
        review.product = product
        review.save()
        return redirect('product_page', product.slug)












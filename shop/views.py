from random import randint
from typing import Any
from django.shortcuts import get_object_or_404, render, redirect
from  django.views.generic import ListView, DetailView
from django.contrib.auth import login, logout
from django.contrib import messages
from django.db.utils import IntegrityError

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Product, Review, FavoriteProducts, Emails
from .forms import FeedbackForm, LoginForm, RegistrationForm, ReviewForm, \
CustomerForm, ShippingForm
from .utils import CartForAuthenticatedUser, get_cart_data

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
       context['reviews'] = Review.objects.filter(product=product).order_by('-pk')
       
       if self.request.user.is_authenticated:
           context['review_form'] = ReviewForm


       return context
    

def login_registration(request):
    context= {'title': 'Увійти чи зареєструватись',
              'login_form': LoginForm,
              'registration_form': RegistrationForm
              }

    return render (request, 'shop/login_registration.html', context)

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


def save_favorite_product(request, product_slug):
    """Додавання чи видалення товару з обраних"""
    if request.user.is_authenticated:
        current_user = request.user
        current_product = Product.objects.get(slug = product_slug)
        favorite_products = FavoriteProducts.objects.filter(user=current_user)


        if current_product in [i.product for i in favorite_products]:
            fav_product = FavoriteProducts.objects.get(user=current_user, product=current_product)
            fav_product.delete()
        else:
            FavoriteProducts.objects.create(user=current_user, product=current_product)

        next_page = request.META.get('HTTP_REFERER','category_detail')
        return redirect(next_page)



class FavoriteProductsViews(LoginRequiredMixin,ListView):
    """Для виведення обраних сторінок"""
    
    model = FavoriteProducts
    context_object_name = 'products'
    template_name = 'shop/favorite_products.html'
    login_url = 'login_registration'

    def get_queryset(self):
        """Отримуємо товари конкретного користувача"""
        user = self.request.user
        favs = FavoriteProducts.objects.filter(user=user)
        products = [i.product for i in favs] 
        return  products
    

def save_subscribers(request):
    """Збирач поштових адрес"""
    email = request.POST.get('email')
    user = request.user if request.user.is_authenticated else None
    phone_number=request.POST.get('phone_number')
    viber_number=request.POST.get('viber_number')
    telegram_number=request.POST.get('telegram_number')
    if email:
        try:
            Emails.objects.create(
                mail=email, 
                user=user, 
                phone_number=phone_number,
                viber_number=viber_number,
                telegram_number=telegram_number

                )
            messages.info(request, 'Дякуємо ваші данні отримані, будемо раді повідомляти вас про новинки та акції')
        # except Exception as E:

        except IntegrityError:
            # print(E.__class__)
            messages.error(request, "Такий email вже зареєстрований, спробуйте інший email" ) 
    return redirect('index')   

def send_mail_to_subscribesrs(request): 
    """Відправка листів підписникам"""
    from conf import settings
    from django.core.mail import send_mail
    if request.method == 'POST':
        text = request.POST.get('text')
        mail_lists=Emails.objects.all()
        for email in mail_lists:
            email_address = email.mail  # Отримуємо адресу електронної пошти з об'єкта
            send_mail(
                subject='Акція',
                message=text,
                from_email=settings.EMAIL_HOST_USER,  # Від кого
                recipient_list=[email_address],  # До кого
                fail_silently=False,
            )
            print(f'Повідомлення відправлене на пошту {email_address}-----------------{bool(send_mail)}')
    context = {'title':'Спамер',}
    return render(request,'shop/send_mail.html', context ) 


def cart(request):
    """Сторінка Кошика"""
    cart_info = get_cart_data(request)
    context = {
        'order' : cart_info['order'],
        'order_products' : cart_info['order_products'],
        'cart_total_quantity' : cart_info['cart_total_quantity'],
    }
    return render(request, 'shop/cart.html', context)


def to_cart(request, product_id, action):
    """додати товар до Кошика"""
    if request.user.is_authenticated:
        CartForAuthenticatedUser(request, product_id, action)
        return redirect('cart')
    else:
        messages.error(request, "Авторизуйтесь чи зареєструйтесь, щоб завершити придбання")
        return redirect('login_registration')








            





    

    










from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Назва категорії')
    image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name='Зображення')
    slug = models.SlugField(unique=True, null=True)
    parent = models.ForeignKey('self', 
                               on_delete=models.CASCADE, 
                               null=True, 
                               blank=True, 
                               verbose_name='Категорія',
                               related_name='subcategories')
    
    def get_absolute_url(self):
        """Посилання на сторінку категорій"""
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f'Категорія: pk={self.pk}, title={self.title}'
    
    def get_parent_category_photo(self):
        """Для отримання малюнка батьківської категорії """
        if self.image:
            return self.image.url
        else:
            return 'https://korobkionline.com.ua/content/images/33/390x390l95mc0/68619443721548.webp'
    
    class Meta:
        verbose_name = 'Категорія'
        verbose_name_plural= 'Категорії'

class Product(models.Model):
    title = models.CharField(max_length=255, verbose_name='Назва товару')
    price = models.FloatField(verbose_name='Ціна')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата створення')
    watched = models.IntegerField(default=0, verbose_name='перегляди')
    quantity = models.IntegerField(default=0, verbose_name='Кількість в наявності')
    description = models.TextField(default='Тут буде опис товару', verbose_name='Опис товару')
    info = models.TextField(default='Тут буде інформація про товар', verbose_name='Інформація про товар')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категорія', related_name='products')
    slug = models.SlugField(unique=True, null=True)
    size = models.IntegerField(default=30,verbose_name='Розмір в мм')
    color = models.CharField(max_length=30, default='Срібло', verbose_name='Колір/Матеріал')
    

    def get_absolute_url(self):
        pass

    def __str__(self) -> str:
        return self.title

    def __repr__(self) -> str:
        return f'Товар: pk={self.pk}, title={self.title}, price = {self.price}'
    
    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural= 'Товари'


class Gallery(models.Model):
    image = models.ImageField(upload_to='products/',  verbose_name='Зображення')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')

    
    class Meta:
        verbose_name = 'Зображення'
        verbose_name_plural= 'Галерея зображень'


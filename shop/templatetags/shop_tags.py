from django import template
from shop.models import Category, FavoriteProducts 
from  django.template.defaulttags import register as range_register 


register = template.Library()

@register.simple_tag()
def get_subcategories(category):
    return Category.objects.filter(parent=category)

@register.simple_tag()
def get_sorted():
    sortes = [
       {
           'title': 'Ціна',
            'sorters': [
                ('price', 'за зростанням'),
                ('-price', 'за спаданням')
            ]
       },
        {
           'title': 'Колір',
            'sorters': [
                ('color', 'від А до Я'),
                ('-color', 'від Я до А')
            ]
       },
        {
           'title': 'Розмір',
            'sorters': [
                ('size', 'за зростанням'),
                ('-size', 'за спаданням')
            ]
       }, 
    ]

    return sortes

@range_register.filter
def get_positive_range(value):
    return range(int(value))

@range_register.filter
def get_negative_range(value):
    return range(5 - int(value))



@register.simple_tag()
def get_favorite_products(user):
    """Вивід обраних товарі на сторінку"""
    fav = FavoriteProducts.objects.filter(user=user)
    products = [i.product for i in fav]
    return products




from django import template
from shop.models import Category

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




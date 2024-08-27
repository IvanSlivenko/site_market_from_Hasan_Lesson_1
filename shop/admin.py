from django.contrib import admin

from .models import Product, Category, Gallery, Review, Emails, Customer, Order, OrderProduct, ShippingAddress
from django.utils.safestring import mark_safe


class GallerryInline(admin.TabularInline):
    fk_name = 'product'
    model = Gallery
    extra = 1



# admin.site.register(Category)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'get_products_count')
    prepopulated_fields = {'slug': ('title',)}

    def get_products_count(self, obj):
        if  obj.products:
            return str(len(obj.products.all()))
        else:
            return '0'
    get_products_count.short_description='Кількість у категорії'


# admin.site.register(Product)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'title',
        'category',
        'quantity',
        'price',
        'created_at',
        'size',
        'color',
        'get_photo')
    list_editable=('price', 'quantity', 'size', 'color')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('title', 'price')
    list_display_links=('pk', 'title', )
    inlines = (GallerryInline,)
    readonly_fields=('watched',)

    def get_photo(self, obj):
        if obj.images.all():
            print(obj.images.all(),'-------------0')
            print(obj.images.all()[0],'-------1')
            print(obj.images.all()[0].image, '-------------image---2')
            print(obj.images.all()[0].image.url, '--------------- url------3')
            return mark_safe(f'<img src="{obj.images.all()[0].image.url}" width="75">')
            
        else:
            return '-'

    get_photo.short_description='Мініфото'

admin.site.register(Gallery)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Відображення відгуків в адмінці"""
    list_display=(
        'pk',
        'author',
        'created_at'
    )
    readonly_fields=('pk',
        'author',
        'created_at'
        )
    

@admin.register(Emails)
class ReviewMail(admin.ModelAdmin):
    """Відображення Emai в адмінці"""
    list_display=(
        'pk',
        'mail',
        'user',
        'phone_number',
        'viber_number',
        'telegram_number',

    )
    readonly_fields=(
        'pk',
        'mail',
        'user',
        'phone_number',
        'viber_number',
        'telegram_number',
        )

@admin.register(Customer)
class ReviewCustomer(admin.ModelAdmin):
    """Відображення Покупців в адмінці"""
    list_display=(
        'user',
        'first_name',
        'last_name',
        'email',
        'phone'
    )
    readonly_fields=(
        'user',
        'first_name',
        'last_name',
        'email',
        'phone'
        )
    list_filter=(
        'user',
        'email',
        'phone'
    )

@admin.register(Order)
class ReviewOrder(admin.ModelAdmin):
    """Відображення Корзини в адмінці"""
    list_display=(
        'customer',
        'created_at',
        'is_completed',
        'shipping',
    )
    readonly_fields=(
        'customer',
        'is_completed',
        'shipping',
        )
    list_filter=(
        'customer',
        'is_completed',
    )

@admin.register(OrderProduct)
class ReviewOrderProduct(admin.ModelAdmin):
    """Відображення Товарів Корзини в адмінці"""
    list_display=(
        'product',
        'order',
        'quantity',
        'addet_at',
        )
    readonly_fields=(
        'product',
        'order',
        'quantity',
        'addet_at',
        )
    list_filter=(
        'product',
        )

@admin.register(ShippingAddress)
class ReviewShippingAddress(admin.ModelAdmin):
    """Відображення Адрес доставки в адмінці"""
    list_display=(
        'customer',
        'order',
        'sity',
        'state',
        'street',
        'created_at',
        )
    readonly_fields=(
        'customer',
        'order',
        'sity',
        'state',
        'street',
        'created_at',
        )
    list_filter=(
        'customer',
        )     

# admin.site.register(Customer)
# admin.site.register(Order)
# admin.site.register(OrderProduct)
# admin.site.register(ShippingAddress)

    



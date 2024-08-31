from .models import Product, OrderProduct, Order, Customer



class CartForAuthenticatedUser:
    """Логіка корзини"""
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user
        if product_id and action:
            self.add_or_delete(product_id, action)

    def custom_number_format(self, value):
        try:
            value = float(value)
            formatted_value = f"{value:,.2f}".replace(',', ' ').replace('.', ',')
            print(formatted_value,'-------------------------------------------------------')
            return formatted_value
        except (ValueError, TypeError):
            return value        
         

    def get_cart_info(self):
        """Отримання інформації про корзину (кількість і сума товарів) і про замовника"""
        customer, created = Customer.objects.get_or_create(user=self.user)
        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.ordered.all()
        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            'order' : order, # id кошика
            'order_products' : order_products, # Queryset - об'єкт товарів у кошику
            'cart_total_quantity' : cart_total_quantity, # загальна кількість товарів в кошику
            'cart_total_price' : cart_total_price, # загальна вартість товарів в кошику

        }


    def add_or_delete(self, product_id, action):
        """Додавання чи видалення товарів при натисканні на плюс чи мінус"""
        order = self.get_cart_info()['order']
        # order = self.get_cart_info().get('order')
        product = Product.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(order=order, product=product)

        if action == 'add' and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1
        elif action == 'delete':
            order_product.quantity -= 1
            product.quantity += 1
        elif action == 'remove':
            product.quantity += order_product.quantity
            order_product.quantity -= order_product.quantity

        product.save()
        order_product.save()

        if order_product.quantity < 1:
            order_product.delete()

def get_cart_data(request):
    """Вивід товара з корзини на сторінку"""
    cart = CartForAuthenticatedUser(request)
    cart_info = cart.get_cart_info()

    return {
        'order' : cart_info['order'],
        'order_products' : cart_info['order_products'],
        'cart_total_quantity' : cart_info['cart_total_quantity'],
        'cart_total_price' : cart_info['cart_total_price'],

    }

    


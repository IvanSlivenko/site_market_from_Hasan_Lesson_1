from .models import Product, OrderProduct, Order, Customer

class CartForAuthenticatedUser:
    """Логіка корзини"""
    def __init__(self, request, product_id=None, action=None):
        self.user = request.user
        if product_id and action:
            self.add_or_delete(product_id, action)    

          


    def get_cart_info(self):
        """Отримання інформації про корзину (кількість і сума товарів) і про замовника"""
        customer, created = Customer.objects.get_or_create(user=self.user)
        order, created = Order.objects.get_or_create(customer=customer)
        order_products = order.ordered.all()
        cart_total_quantity = order.get_cart_total_quantity




    def add_or_delete(self, product_id, action):
        """Додавання чи видалення товарів при натисканні на плюс чи мінус"""
        pass


def get_cart_data(request):
    """Вивід товара з корзини на сторінку"""
    pass


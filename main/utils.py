from .models import *

def cartData(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, cart_complete=False)
        order_products = Order_Product.objects.filter(order=order)
        
    return {'order_products':order_products, 'order':order}
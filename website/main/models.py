from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=False, null=True)
    unit = models.CharField(max_length=200,blank=True)
    image = models.ImageField(null=False, blank=False,upload_to="static/images")

    def __str__(self):
        return self.name

class Customer(models.Model):
    username = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.username
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    cart_complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=30, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        order_products = self.order_product_set.all()
        total_price = sum([order_product.get_total for order_product in order_products])
        return total_price

    @property
    def get_total_quantity(self):
        order_products = self.order_product_set.all()
        total_quantity = sum([order_product.quantity for order_product in order_products])
        return total_quantity
    
class Order_Product(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_ordered = models.TimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total 

    
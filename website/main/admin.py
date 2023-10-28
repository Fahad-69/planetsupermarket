from django.contrib import admin
from .models import *

class ProductAdmin(admin.ModelAdmin):
    list_display=('id','name','price','category','unit','image')

admin.site.register(Product,ProductAdmin)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(Order_Product)
admin.site.register(Customer)

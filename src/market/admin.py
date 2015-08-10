from django.contrib import admin
from market.models import Customer, Seller, Order, Product

# Register your models here.
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Order)

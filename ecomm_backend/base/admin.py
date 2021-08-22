from django.contrib import admin
from .models import Order, OrderItem, Product, ShippingAddress, Variant

# Register your models here.
admin.site.register([Product, Variant, Order, OrderItem, ShippingAddress ])

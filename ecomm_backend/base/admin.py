from django.contrib import admin
from .models import Product, Variant

# Register your models here.
admin.site.register([Product, Variant])

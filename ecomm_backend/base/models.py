from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.id}_{self.name}')

# Will have foreignField in "many" side


class Variant(models.Model):
    id = models.PositiveIntegerField(unique=True, primary_key=True)
    name = models.CharField(max_length=200, null=False, blank=False)
    # When the product gets deleted, delete all its variants
    # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200, null=False, blank=False)
    sku = models.CharField(max_length=50, null=False, blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    currency = models.CharField(
        max_length=10, null=False, blank=False, default="CAD")
    image_url = models.URLField(max_length=200)
    thumbnail_url = models.URLField(max_length=200, null=True, blank=True)
    likes = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(f'{self.id}_{self.name}')


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    payment_method = models.CharField(max_length=200, null=False, blank=False)
    tax_price = models.DecimalField(max_digits=7, decimal_places=2)
    shipping_price = models.DecimalField(max_digits=7, decimal_places=2)
    total_price = models.DecimalField(max_digits=7, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.created_at)


class OrderItem(models.Model):
    variant = models.ForeignKey(Variant, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    qty = models.PositiveIntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return str(self.variant.name)


class ShippingAddress(models.Model):
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=20)
    postalcode = models.CharField(max_length=20)
    country = models.CharField(max_length=20)
    shipping_price = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return str(self.address)

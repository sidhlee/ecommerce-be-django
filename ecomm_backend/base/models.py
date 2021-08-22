from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
  product_id = models.CharField(max_length=20, null=False, blank=False, primary_key=True, editable=False)
  name = models.CharField(max_length=200, null=False, blank=False)
  image_url = models.URLField(max_length=200)
  likes = likes = models.PositiveIntegerField(default=0)
  created = models.DateTimeField(auto_now_add=True)

# Will have foreignField in "many" side
class Variant(models.Model):
  variant_id= models.CharField(max_length=20, null=False, blank=False, primary_key=True, editable=False)
  name = models.CharField(max_length=200, null=False, blank=False)
  # When the product gets deleted, delete all its variants
  # https://docs.djangoproject.com/en/3.2/topics/db/examples/many_to_one/
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  product_name= models.CharField(max_length=200, null=False, blank=False)
  sku= models.CharField(max_length=50, null=False, blank=False)
  price = models.PositiveIntegerField() 
  currency = models.CharField(max_length=10, null=False, blank=False, default="CAD")
  image_url = models.URLField(max_length=200)
  likes = models.PositiveIntegerField(default=0)
  created = models.DateTimeField(auto_now_add=True)

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Variant


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify which field to include when serializing
        model = Product
        fields = '__all__'  # Can specify fields in a list


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

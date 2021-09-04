from rest_framework import serializers
# from django.contrib.auth.models import User
from .models import Product, Variant
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify which field to include when serializing
        model = Product
        fields = '__all__'  # Can specify fields in a list


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    # https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield
    # 'name' field gets read-only value by calling get_<field_name> method
    name = serializers.SerializerMethodField(read_only=True)
    isAdmin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        # User model has a lot of fields
        fields = ['id', 'username', 'email', 'name', 'isAdmin']

    # DRF will call this method and set it as the value for 'name' field
    def get_name(self, obj: User):
        name = obj.username

        if name == '':
            name = obj.email

        return name

    def get_isAdmin(self, obj: User):
        return obj.is_staff


# Serialize user information with new token
class UserSerializerWithToken(UserSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'isAdmin', 'token']

    def get_token(self, obj: User):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

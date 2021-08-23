from .serializers import ProductSerializer, VariantSerializer
from .models import Product, Variant
from django.http import JsonResponse
from decouple import config
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .products import products


# Create your views here.

# Pass in allowed methods
@api_view(['GET'])
def getRoute(request):
    routes = [
        '/api/products',
        '/api/products/sync/'
        '/api/products/top/',

        '/api/products/<id>',

        '/api/products/<update>/<id>/',
    ]

    # If safe=True (default) only dictionary is allowed to be serialized
    return Response(routes)


@api_view(['GET'])
def getProducts(request):
    # Query all products
    products = Product.objects.all()
    serialized_products = ProductSerializer(products, many=True).data
    # Query related variants and add to product
    for i in serialized_products:
        variants = Variant.objects.filter(product=i["id"]).order_by('-likes')
        serialized_variants = VariantSerializer(variants, many=True).data
        i["variants"] = serialized_variants

    return Response(serialized_products)


@api_view(['GET'])
# pk for primary key because id is an inbuilt function in python.
def getProduct(request, pk):
    """
    Send individual product.

          Parameters:
            pk: primary key
    """
    # Query the product by product id
    product = Product.objects.get(id=pk)
    # Query related variants by product id
    variants = Variant.objects.filter(product=pk).order_by('-likes')

    serialized_product = ProductSerializer(product, many=False).data
    serialized_variants = VariantSerializer(variants, many=True).data

    serialized_product["variants"] = serialized_variants

    return Response(serialized_product)


@api_view(['GET'])
def sync_products(request):
    """
    Sync products and variants in the database with the data from the printful api
    """
    headers = {'Authorization': config('PRINTFUL_KEY')}
    response = requests.get('https://api.printful.com/store/products',
                            headers=headers)
    products = response.json()["result"]
    products_with_variant = []

    # Flush existing rows
    Product.objects.all().delete()
    Variant.objects.all().delete()

    # Re-populate from PrintfulAPI
    for i in products:
        product_id = i["id"]
        response = requests.get(
            f'https://api.printful.com/store/products/{product_id}', headers=headers)
        pwv = response.json()["result"]

        sync_product = pwv["sync_product"]
        sync_variants = pwv["sync_variants"]

        product = Product(
            id=sync_product["id"],
            name=sync_product["name"],
        )
        product.save()

        variants = []
        for v in sync_variants:
            variant = Variant(
                id=v["id"],
                name=v["name"],
                product=product,
                product_name=v["product"]["name"],
                sku=v["sku"],
                price=v["retail_price"],
                currency=v["currency"],
                image_url=v["files"][1]["preview_url"],
            )
            variant.save()

            serialized_variant = VariantSerializer(variant, many=False).data
            variants.append(serialized_variant)

        serialized_product = ProductSerializer(product, many=False).data

        serialized_product["variants"] = variants

        products_with_variant.append(serialized_product)

    return Response({"products": products_with_variant})

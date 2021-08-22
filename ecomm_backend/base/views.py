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
    response = requests.get('https://api.printful.com/store/products',
                            headers={'Authorization': config('PRINTFUL_KEY')})

    products = response.json()["result"]
    return Response(products)


@api_view(['GET'])
# pk for primary key because id is an inbuilt function in python.
def getProduct(request, pk):
    """
    Send individual product.

          Parameters:
            pk: primary key
    """

    product = None
    for p in products:
        if p['sync_product']['id'] == pk:
            product = p
            break

    return Response(product)


@api_view(['GET'])
def sync_products(request):
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
            product_id=sync_product["id"],
            name=sync_product["name"],
        )
        product.save()

        variants = []
        for v in sync_variants:
            variant = Variant(
                variant_id=v["id"],
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

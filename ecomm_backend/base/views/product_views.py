from decouple import config
import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response
from ..models import Product, Variant
from ..serializers import ProductSerializer, VariantSerializer

# Pass in allowed methods


@api_view(['GET'])
def getRoute(request):
    routes = [
        '/api/products',
        '/api/products/sync/'
        '/api/products/top/',

        '/api/products/<id>',
        '/api/variant/<id>',

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
def getVariant(request, pk):
    variant = Variant.objects.get(id=pk)
    serialized_variant = VariantSerializer(variant, many=False).data

    return Response(serialized_variant)


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
                variant_id=v["variant_id"],
                name=v["name"],
                product=product,
                product_name=v["product"]["name"],
                sku=v["sku"],
                price=v["retail_price"],
                currency=v["currency"],
                image_url=v["files"][1]["preview_url"],
                thumbnail_url=v["files"][1]["thumbnail_url"]
            )
            variant.save()

            serialized_variant = VariantSerializer(variant, many=False).data
            variants.append(serialized_variant)

        serialized_product = ProductSerializer(product, many=False).data

        serialized_product["variants"] = variants

        products_with_variant.append(serialized_product)

    return Response({"products": products_with_variant})


# TODO: re-write syncProducts so that if the synching fails, it leaves the db as it was.
# Now, it wipes the db before the operation, so we end up with an empty db if it fails.


# fetch product list from API

# create & store Product instances in a list

# loop over list and fetch detailed detailed info including variants
    # Create a new class instances: DetailedProduct - product with all variants as subfield
    # Append the instances into a list: detailed_products

    # Create Variant instances and append them to a list


# If it didn't throw up to this point, clear Products & Variants in db
# and save the list of Variant and Product into db with Model.objects.bulk_create(list)

# Respond with detailed_products

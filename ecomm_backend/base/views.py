from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .products import products



# Create your views here.

# Pass in allowed methods
@api_view(['GET'])
def getRoute(request):
  routes = [
    '/api/products',
    '/api/products/create',

    '/api/products/upload/',

    '/api/products/<id>/reviews/',

    '/spi/products/top/',
    '/api/products/<id>/',

    '/api/products/delete/<id>',
    '/api/products/<update>/<id>/',
  ]

  # If safe=True (default) only dictionary is allowed to be serialized
  return Response(routes)

@api_view(['GET'])
def getProducts(request):
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

from django.urls import path
from . import views

urlpatterns = [
    path('', views.getRoute, name="routes"),
    path('products', views.getProducts, name="products"),
    path('products/sync/', views.sync_products,
         name="sync_products"),
    path('products/<str:pk>/', views.getProduct, name="product"),
    path('variant/<str:pk>/', views.getVariant, name="variant")
]

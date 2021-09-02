from django.urls import path
from ..views import product_views as views

urlpatterns = [
    path('sync/', views.sync_products,
         name="sync_products"),
    path('', views.getProducts, name="products"),
    path('variant/<str:pk>/', views.getVariant, name="variant"),
    path('<str:pk>/', views.getProduct, name="product"),
]

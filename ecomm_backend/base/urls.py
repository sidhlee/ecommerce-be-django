from django.urls import path
from . import views

urlpatterns = [
    path('users/login/', views.MyTokenObtainPairView.as_view(),
         name="token_obtain_pair"),
    path('users/profile/', views.getUserProfile, name="user-profile"),
    path('', views.getRoute, name="routes"),
    path('products/sync/', views.sync_products,
         name="sync_products"),
    path('products', views.getProducts, name="products"),
    path('products/<str:pk>/', views.getProduct, name="product"),
    path('variant/<str:pk>/', views.getVariant, name="variant"),
]

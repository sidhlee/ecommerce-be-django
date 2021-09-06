from django.urls import path
from ..views import shipping_views as views

urlpatterns = [
    path('countries/', views.get_country_codes, name="countries")
]

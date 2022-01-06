from django.urls import path

from . import views

urlpatterns = [
    path('products', views.get_products, name='products'),
    path('orders', views.get_orders, name='orders'),
]

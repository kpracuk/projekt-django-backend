from django.urls import path

from . import views

urlpatterns = [
    path('products', views.get_products, name='products'),
    path('orders', views.orders_routes, name='orders_routes'),
]

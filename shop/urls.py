from django.urls import path

from . import views

urlpatterns = [
    path('products', views.get_products, name='products'),
    path('orders', views.orders_routes, name='orders_routes'),
    path('orders/<int:order_id>', views.update_order_data, name='update_order_data'),
]

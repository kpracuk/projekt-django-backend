import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from shop.models import Product
from shop.models import Order
from shop.helpers.responses import generate_response_from_product, generate_response_from_order


@login_required()
def get_products(request):
    products_query = Product.objects.all()
    products = []
    for product in products_query:
        products.append(generate_response_from_product(product))

    return JsonResponse(products, safe=False)


@login_required()
def get_orders(request):
    orders_query = Order.objects.prefetch_related('user', 'product').all()
    orders = []
    for order in orders_query:
        orders.append(generate_response_from_order(order))

    return JsonResponse(orders, safe=False)

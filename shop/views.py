import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from shop.models import Product
from django.core.serializers import serialize
from shop.helpers.responses import generate_response_from_product


@login_required()
def get_products(request):
    products_query = Product.objects.all()
    products = []
    for product in products_query:
        products.append(generate_response_from_product(product))

    return JsonResponse(products, safe=False)

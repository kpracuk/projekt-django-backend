import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from validation.validation import Validate
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


def orders_routes(request):
    if request.method == 'GET':
        return get_orders(request)
    if request.method == 'POST':
        return create_order(request)


@require_http_methods(['GET'])
@login_required()
def get_orders(request):
    orders_query = Order.objects.prefetch_related('user', 'product').all()
    orders = []
    for order in orders_query:
        orders.append(generate_response_from_order(order))

    return JsonResponse(orders, safe=False)


@require_http_methods(['POST'])
@login_required()
def create_order(request):
    user = request.user
    params = json.loads(request.body.decode('utf-8'))
    schema = {
        'product_id': 'required',
        'quantity': 'required'
    }

    validator = Validate()
    validation_result = validator.check(params, schema)
    if not validation_result['is_valid']:
        return JsonResponse(validation_result['data'], status=422, safe=False)

    product = Product.objects.get(pk=params['product_id'])
    if product is None:
        return JsonResponse({'errors': {'product_id': ['Błędne ID produktu']}}, status=422, safe=False)

    if product.quantity < params['quantity']:
        return JsonResponse({'errors': {'quantity': ['Zbyt duża ilość']}}, status=422, safe=False)

    order = Order.objects.create(
        product=product,
        price_at_buy=product.price,
        quantity=params['quantity'],
        user=user,
        status='placed'
    )
    if order is None:
        return JsonResponse({}, status=500, safe=False)

    product.quantity = product.quantity - params['quantity']
    product.save()


    return JsonResponse(generate_response_from_order(order), safe=False)

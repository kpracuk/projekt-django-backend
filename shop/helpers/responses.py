from shop.models import Product
from shop.models import Order
from authentication.helpers.responses import generate_response_from_user


def generate_response_from_product(product: Product):
    return {
        'id': product.id,
        'name': product.name,
        'description': product.description,
        'price': product.price,
        'quantity': product.quantity,
        'created_at': product.created_at,
        'updated_at': product.updated_at
    }


def generate_response_from_order(order: Order):
    return {
        'id': order.id,
        'status': order.status,
        'price_at_buy':  order.price_at_buy,
        'quantity':  order.quantity,
        'product_id': order.product_id,
        'product': generate_response_from_product(order.product),
        'user_id': order.user_id,
        'user': generate_response_from_user(order.user),
        'created_at':  order.created_at,
        'updated_at':  order.updated_at
    }

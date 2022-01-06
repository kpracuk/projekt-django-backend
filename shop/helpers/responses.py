from shop.models import Product


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

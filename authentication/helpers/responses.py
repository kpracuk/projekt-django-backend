from authentication.models import User


def generate_response_from_user(user: User):
    return {
        'id': user.id,
        'name': user.username,
        'email': user.email,
        'email_verified_at': user.date_joined,
        'role': user.is_staff and 'admin' or 'user',
        'created_at': user.date_joined,
        'updated_at': user.last_login
    }

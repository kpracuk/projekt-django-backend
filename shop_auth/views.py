import json
from django.core.serializers import serialize
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
from django.middleware.csrf import get_token
from shop_auth.models import User
from shop_auth.helpers.responses import generate_response_from_user


def get_csrf_token(request):
    get_token(request)
    return JsonResponse({})


def get_user(request):
    user = request.user
    if user.is_authenticated:
        return JsonResponse(generate_response_from_user(user))
    else:
        return JsonResponse({}, status=401)


def login_user(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse(generate_response_from_user(user))
    else:
        return JsonResponse({}, status=422)


def register_user(request):
    params = json.loads(request.body.decode('utf-8'))
    user = User.objects.create_user(params['name'], params['email'], params['password'])
    if user is not None:
        login(request, user)
        return JsonResponse(generate_response_from_user(user))
    else:
        return JsonResponse({}, status=422)


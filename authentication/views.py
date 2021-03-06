import json
from validation.validation import Validate
from django.http import JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from authentication.models import User
from authentication.helpers.responses import generate_response_from_user


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
    params = json.loads(request.body.decode('utf-8'))
    schema = {
        'email': 'required',
        'password': 'required'
    }
    validator = Validate()
    validation_result = validator.check(params, schema)
    if validation_result['is_valid']:
        user = authenticate(request, username=params['email'], password=params['password'])
        if user is not None:
            login(request, user)
            return JsonResponse(generate_response_from_user(user))
        else:
            return JsonResponse({'errors': {'email': ['Błędne dane logowania']}}, status=422, safe=False)
    else:
        return JsonResponse(validation_result['data'], status=422, safe=False)


def register_user(request):
    params = json.loads(request.body.decode('utf-8'))
    schema = {
        'name': 'required',
        'email': 'required|email',
        'password': 'required|confirmed'
    }
    validator = Validate()
    validation_result = validator.check(params, schema)
    if validation_result['is_valid']:
        if User.objects.filter(email=params['email']).exists():
            return JsonResponse({'errors': {'email': ['Email jest już zajęty']}}, status=422, safe=False)
        user = User.objects.create_user(params['name'], params['email'], params['password'])
        if user is not None:
            login(request, user)
            return JsonResponse(generate_response_from_user(user))
    else:
        return JsonResponse(validation_result['data'], status=422, safe=False)


def logout_user(request):
    logout(request)
    return JsonResponse({}, status=200)


@login_required()
def update_user_data(request):
    user = request.user
    params = json.loads(request.body.decode('utf-8'))
    schema = {
        'name': 'required',
        'email': 'required|email'
    }
    validator = Validate()
    validation_result = validator.check(params, schema)
    if not validation_result['is_valid']:
        return JsonResponse(validation_result['data'], status=422, safe=False)

    if user.email != params['email'] and User.objects.filter(email=params['email']).exists():
        return JsonResponse({'errors': {'email': ['Email jest już zajęty']}}, status=422, safe=False)

    user.email = params['email']
    user.username = params['name']
    user.save()

    return JsonResponse(generate_response_from_user(user))


@login_required()
def update_user_password(request):
    user = request.user
    params = json.loads(request.body.decode('utf-8'))
    schema = {
        'current_password': 'required',
        'password': 'required|confirmed'
    }
    validator = Validate()
    validation_result = validator.check(params, schema)
    if not validation_result['is_valid']:
        return JsonResponse(validation_result['data'], status=422, safe=False)

    if not user.check_password(params['current_password']):
        return JsonResponse({'errors': {'current_password': ['Obecne hasło jest niepoprawne']}}, status=422, safe=False)

    user.set_password(params['password'])
    user.save()

    return JsonResponse({})

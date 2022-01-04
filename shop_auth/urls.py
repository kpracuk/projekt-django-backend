from django.urls import path

from . import views

urlpatterns = [
    path('csrf-cookie', views.get_csrf_token, name='csrf-cookie'),
    path('user', views.get_user, name='user'),
    path('register', views.register_user, name='register'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('csrf-cookie', views.get_csrf_token, name='csrf-cookie'),
    path('user', views.get_user, name='user'),
    path('login', views.login_user, name='login'),
    path('register', views.register_user, name='register'),
    path('logout', views.logout_user, name='logout'),
    path('user/profile-information', views.update_user_data, name='profile-information'),
    path('user/password', views.update_user_password, name='password')
]

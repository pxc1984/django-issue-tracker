from django.urls import path
from rest_framework_simplejwt.views import token_obtain_pair, token_refresh

from auth_api.views import register, ping

urlpatterns = [
    # Registration
    path('register/', register, name='register'),
    path('ping/', ping, name='ping'),

    # JWT built-in endpoints
    path('token/', token_obtain_pair, name='token_obtain_pair'),
    path('token/refresh/', token_refresh, name='token_refresh'),
]
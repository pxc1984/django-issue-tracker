from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def register(request):
    """Register a new user and return a JWT pair."""
    username = request.data.get("username")
    if not username:
        return Response({"error": "Provide username."}, status=status.HTTP_400_BAD_REQUEST)

    password = request.data.get("password")
    if not password or type(password) is not str:
        return Response({"error": "Provide password"}, status=status.HTTP_400_BAD_REQUEST)
    if len(password) < 6:
        return Response({"error": "Password is too weak"}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({"error": "User already exists."}, status=status.HTTP_400_BAD_REQUEST)

    user = User(username=username, password=make_password(password))
    user.save()

    refresh = RefreshToken.for_user(user)
    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def ping(request):
    """Веб-сервис, позволяющий проверить корректность работы Token-based авторизации."""
    return Response({'message': 'pong'}, status=status.HTTP_200_OK)

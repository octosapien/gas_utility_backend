from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import get_user_model

@api_view(["POST"])
@permission_classes([AllowAny])  # ✅ Allow anyone to register
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")
    role = request.data.get("role", "USER").upper()  # ✅ Ensure role is uppercase

    if get_user_model().objects.filter(username=username).exists():
        return Response({"error": "Username already taken"}, status=400)

    user = get_user_model().objects.create_user(username=username, email=email, password=password, role=role)
    
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,  # ✅ Include email in response
        "role": user.role      # ✅ Include role in response
    }, status=201)

@api_view(["POST"])
@permission_classes([AllowAny])  # ✅ Allow anyone to login
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)
    if user is None:
        return Response({"error": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)

    # Serialize user data (excluding password)
    user_data = UserSerializer(user).data
    user_data.pop("password", None)  # Ensure password is not included

    return Response({
        "refresh": str(refresh),
        "access": str(refresh.access_token),
        **user_data  # ✅ Include all user data except password
    })
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from django.contrib.auth import get_user_model  # Updated import
from rest_framework.generics import CreateAPIView 
from rest_framework.permissions import AllowAny 
from rest_framework.serializers import ModelSerializer 

User = get_user_model()  # Dynamically fetch the user model
print(User)
class UserSerializer(ModelSerializer): 
    class Meta: 
        model = User 
        fields = ["id", "username", "email", "password"] 
        extra_kwargs = {"password": {"write_only": True}} 
 
    def create(self, validated_data): 
        user = get_user_model().objects.create_user(**validated_data)  # Updated reference
        return user 
 
class UserCreateView(CreateAPIView): 
    serializer_class = UserSerializer 
    permission_classes = [AllowAny]

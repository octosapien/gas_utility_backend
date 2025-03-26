from rest_framework import serializers
from .models import ServiceRequest, User  # ✅ Import User model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password"]  # ✅ Exclude password from response

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = "__all__"

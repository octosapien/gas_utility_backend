from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import ServiceRequest
from .serializers import ServiceRequestSerializer
from .serializers import UserSerializer, ServiceRequestSerializer

# Class-Based Views (Maintaining Authentication & User Filtering)
class ServiceRequestListCreateView(generics.ListCreateAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ServiceRequest.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ServiceRequestDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ServiceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ServiceRequest.objects.filter(user=self.request.user)


# Function-Based Views (User and Admin Requests Handling)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_requests(request):
    """Users can fetch their own account details and service requests."""
    
    # Serialize user data (excluding password)
    user_data = UserSerializer(request.user).data
    user_data.pop("password", None)  # Ensure password is not included

    # Get user's service requests
    requests = ServiceRequest.objects.filter(user=request.user)
    request_data = ServiceRequestSerializer(requests, many=True).data

    return Response({
        "user": user_data,  # ✅ Send user details
        "requests": request_data  # ✅ Send service requests
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_request(request):
    """Users can create service requests; automatically assign `user`."""
    print("Request Data:", request.data)  # ✅ Debug request payload

    serializer = ServiceRequestSerializer(data={**request.data, "user": request.user.id})
    
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    
    print("Serializer Errors:", serializer.errors)  # ✅ Debug errors
    return Response(serializer.errors, status=400)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_all_requests(request):
    """Admins can fetch all service requests."""
    if request.user.role != "ADMIN":
        return Response({"error": "Unauthorized"}, status=403)

    requests = ServiceRequest.objects.all()
    return Response(ServiceRequestSerializer(requests, many=True).data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_request_status(request, req_id):
    """Admins can update the status of service requests."""
    if request.user.role != "ADMIN":
        return Response({"error": "Unauthorized"}, status=403)

    try:
        service_request = ServiceRequest.objects.get(id=req_id)
        service_request.status = request.data.get("status", service_request.status)
        service_request.save()
        return Response(ServiceRequestSerializer(service_request).data)
    except ServiceRequest.DoesNotExist:
        return Response({"error": "Not found"}, status=404)

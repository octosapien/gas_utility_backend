from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Rejected", "Rejected"),  # Changed from "Cancelled" to "Rejected"
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    request_type = models.CharField(max_length=255)  # This was missing in the prompt but needed
    details = models.TextField()
    attachment = models.FileField(upload_to="service_attachments/", blank=True, null=True)  # Keep if needed
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.request_type} ({self.status})"

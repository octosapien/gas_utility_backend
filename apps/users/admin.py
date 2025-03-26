from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

User = get_user_model()

# Register the custom user model explicitly
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    pass

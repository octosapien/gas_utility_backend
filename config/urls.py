from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.common.views import register, login
from apps.service_requests.views import get_user_requests, create_request, get_all_requests, update_request_status

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/register/", register),
    path("api/login/", login),
    path("api/requests/", get_user_requests),
    path("api/requests/create/", create_request),
    path("api/admin/requests/", get_all_requests),
    path("api/admin/requests/<int:req_id>/", update_request_status),
    path("api/users/", include("apps.users.urls")),
    path("api/", include("apps.service_requests.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL Configuration for spam_detector project.
Contains all the URL patterns for the project.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # JWT authentication endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App endpoints
    path('api/users/', include('apps.users.urls')),
    path('api/contacts/', include('apps.contacts.urls')),
    path('api/spam/', include('apps.spam.urls')),
]
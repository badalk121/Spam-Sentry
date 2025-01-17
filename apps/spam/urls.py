"""
URL patterns for the spam app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SpamReportViewSet

router = DefaultRouter()
router.register(r'', SpamReportViewSet, basename='spam')

urlpatterns = [
    path('', include(router.urls)),
]
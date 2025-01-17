"""
Views for the users app.
Contains ViewSets and API endpoints for user management.
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, UserSearchSerializer
from apps.spam.models import SpamReport

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing user instances.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'phone_number']

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    @action(detail=False, methods=['GET'])
    def search(self, request):
        """
        Search users by name or phone number.
        """
        try:
            query = request.query_params.get('q', '')
            search_type = request.query_params.get('type', 'name')
            
            cache_key = f'search_{search_type}_{query}'
            results = cache.get(cache_key)
            
            if not results:
                if search_type == 'name':
                    # First get exact matches
                    exact_matches = User.objects.filter(
                        Q(username__istartswith=query) |
                        Q(first_name__istartswith=query) |
                        Q(last_name__istartswith=query)
                    )
                    
                    # Then get partial matches
                    partial_matches = User.objects.filter(
                        Q(username__icontains=query) |
                        Q(first_name__icontains=query) |
                        Q(last_name__icontains=query)
                    ).exclude(id__in=exact_matches)
                    
                    results = list(exact_matches) + list(partial_matches)
                    
                elif search_type == 'phone':
                    results = User.objects.filter(phone_number__icontains=query)
                
                cache.set(cache_key, results, 60 * 15)  # Cache for 15 minutes
            
            serializer = UserSearchSerializer(results, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['GET'])
    def profile(self, request, pk=None):
        """
        Get user profile with additional details.
        """
        try:
            user = self.get_object()
            serializer = UserSerializer(user)
            data = serializer.data
            
            # Add spam reports count
            data['spam_reports_count'] = SpamReport.objects.filter(
                phone_number=user.phone_number
            ).count()
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
"""
Views for the contacts app.
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Q
from .models import Contact
from .serializers import ContactSerializer, ContactBulkCreateSerializer

class ContactViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing contacts.
    """
    
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'phone_number']

    def get_queryset(self):
        """
        Return contacts for the current user.
        """
        return Contact.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Save the contact with the current user.
        """
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['POST'])
    def bulk_create(self, request):
        """
        Create multiple contacts at once.
        """
        serializer = ContactBulkCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        
        if serializer.is_valid():
            contacts = serializer.save()
            return Response(
                ContactSerializer(contacts, many=True).data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['GET'])
    def search(self, request):
        """
        Search contacts by name or phone number.
        """
        query = request.query_params.get('q', '')
        cache_key = f'contact_search_{self.request.user.id}_{query}'
        
        results = cache.get(cache_key)
        
        if not results:
            results = self.get_queryset().filter(
                Q(name__icontains=query) |
                Q(phone_number__icontains=query)
            )
            cache.set(cache_key, results, 300)  # Cache for 5 minutes
        
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
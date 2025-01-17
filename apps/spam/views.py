"""
Views for the spam app.
"""

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from django.db.models import Count
from .models import SpamReport
from .serializers import SpamReportSerializer, SpamCheckSerializer

class SpamReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling spam reports.
    """
    
    serializer_class = SpamReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['phone_number']

    def get_queryset(self):
        """
        Return spam reports, optionally filtered by phone number.
        """
        queryset = SpamReport.objects.all()
        phone_number = self.request.query_params.get('phone_number', None)
        
        if phone_number:
            queryset = queryset.filter(phone_number=phone_number)
        
        return queryset

    def perform_create(self, serializer):
        """
        Create spam report with current user as reporter.
        """
        serializer.save(reporter=self.request.user)
        # Clear cache for this phone number
        cache.delete(f'spam_likelihood_{serializer.validated_data["phone_number"]}')

    @action(detail=False, methods=['POST'])
    def check(self, request):
        """
        Check spam likelihood for a phone number.
        """
        serializer = SpamCheckSerializer(data=request.data)
        
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            cache_key = f'spam_likelihood_{phone_number}'
            
            # Try to get from cache
            likelihood = cache.get(cache_key)
            
            if likelihood is None:
                # Calculate spam likelihood
                total_reports = SpamReport.objects.filter(
                    phone_number=phone_number
                ).count()
                
                # Get unique reporters count
                unique_reporters = SpamReport.objects.filter(
                    phone_number=phone_number
                ).values('reporter').distinct().count()
                
                # Calculate weighted likelihood
                likelihood = min(
                    (total_reports * 0.1) + (unique_reporters * 0.2),
                    1.0
                )
                
                # Cache for 1 hour
                cache.set(cache_key, likelihood, 3600)
            
            return Response({
                'phone_number': phone_number,
                'spam_likelihood': likelihood
            })
            
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=False, methods=['GET'])
    def statistics(self, request):
        """
        Get spam reporting statistics.
        """
        cache_key = 'spam_statistics'
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = {
                'total_reports': SpamReport.objects.count(),
                'unique_numbers': SpamReport.objects.values(
                    'phone_number'
                ).distinct().count(),
                'top_reported': SpamReport.objects.values(
                    'phone_number'
                ).annotate(
                    report_count=Count('id')
                ).order_by('-report_count')[:5]
            }
            
            # Cache for 1 hour
            cache.set(cache_key, stats, 3600)
        
        return Response(stats)
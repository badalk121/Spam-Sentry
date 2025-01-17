"""
Serializers for the spam app.
"""

from rest_framework import serializers
from .models import SpamReport

class SpamReportSerializer(serializers.ModelSerializer):
    """
    Serializer for SpamReport model.
    """
    
    reporter_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SpamReport
        fields = (
            'id', 'phone_number', 'description',
            'created_at', 'reporter_name'
        )
        read_only_fields = ('created_at', 'reporter_name')

    def get_reporter_name(self, obj):
        """
        Return the reporter's username.
        """
        return obj.reporter.username

    def validate_phone_number(self, value):
        """
        Validate phone number format and prevent self-reporting.
        """
        if not value.startswith('+'):
            raise serializers.ValidationError(
                "Phone number must start with '+' symbol."
            )
        
        user = self.context['request'].user
        if user.phone_number == value:
            raise serializers.ValidationError(
                "You cannot report your own number as spam."
            )
        
        return value

class SpamCheckSerializer(serializers.Serializer):
    """
    Serializer for checking spam likelihood of a phone number.
    """
    
    phone_number = serializers.CharField(max_length=17)
    
    def validate_phone_number(self, value):
        if not value.startswith('+'):
            raise serializers.ValidationError(
                "Phone number must start with '+' symbol."
            )
        return value
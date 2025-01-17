"""
Serializers for the contacts app.
"""

from rest_framework import serializers
from .models import Contact
from apps.spam.models import SpamReport

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model.
    Includes spam likelihood calculation.
    """
    
    spam_likelihood = serializers.SerializerMethodField()
    
    class Meta:
        model = Contact
        fields = (
            'id', 'name', 'phone_number', 
            'email', 'created_at', 'updated_at',
            'spam_likelihood'
        )
        read_only_fields = ('created_at', 'updated_at')

    def get_spam_likelihood(self, obj):
        """
        Calculate spam likelihood based on number of spam reports.
        """
        total_reports = SpamReport.objects.filter(
            phone_number=obj.phone_number
        ).count()
        return min(total_reports * 0.1, 1.0)

    def validate_phone_number(self, value):
        """
        Validate phone number format.
        """
        if not value.startswith('+'):
            raise serializers.ValidationError(
                "Phone number must start with '+' symbol."
            )
        return value

class ContactBulkCreateSerializer(serializers.Serializer):
    """
    Serializer for bulk contact creation.
    """
    
    contacts = ContactSerializer(many=True)

    def create(self, validated_data):
        contacts_data = validated_data.pop('contacts')
        user = self.context['request'].user
        contacts = []
        
        for contact_data in contacts_data:
            contact = Contact.objects.create(
                user=user,
                **contact_data
            )
            contacts.append(contact)
        
        return contacts
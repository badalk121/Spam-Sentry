"""
User-related serializers.
Contains serializers for User model and related functionality.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.spam.models import SpamReport

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Handles user registration and profile updates.
    """
    
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    spam_likelihood = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'phone_number', 'email',
            'password', 'first_name', 'last_name',
            'spam_likelihood'
        )
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': False}
        }

    def get_spam_likelihood(self, obj):
        """
        Calculate spam likelihood based on number of spam reports.
        """
        total_reports = SpamReport.objects.filter(
            phone_number=obj.phone_number
        ).count()
        return min(total_reports * 0.1, 1.0)  # 10 reports = 100% spam likelihood

    def create(self, validated_data):
        """
        Create and return a new user instance.
        """
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """
        Update and return an existing user instance.
        """
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class UserSearchSerializer(serializers.ModelSerializer):
    """
    Serializer for user search results.
    Contains limited user information for search results.
    """
    
    spam_likelihood = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'phone_number', 'spam_likelihood')

    def get_spam_likelihood(self, obj):
        """
        Calculate spam likelihood for search results.
        """
        total_reports = SpamReport.objects.filter(
            phone_number=obj.phone_number
        ).count()
        return min(total_reports * 0.1, 1.0)
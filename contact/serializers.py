from rest_framework import serializers
from .models import ContactMessage


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    class Meta:
        model = ContactMessage
        fields = ['id', 'name', 'email', 'language', 'message', 'created_at']
        read_only_fields = ['id', 'created_at']


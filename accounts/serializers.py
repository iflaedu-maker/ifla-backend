from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'is_student', 'email_verified', 'created_at']
        read_only_fields = ['id', 'created_at']


class SignupSerializer(serializers.Serializer):
    """Serializer for user registration"""
    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=False, allow_blank=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    
    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")
        return value


class LoginSerializer(serializers.Serializer):
    """Serializer for user login - accepts username or email"""
    username_or_email = serializers.CharField(required=True, help_text="Enter your username or email")
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )


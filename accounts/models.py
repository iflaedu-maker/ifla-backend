from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
from datetime import timedelta
import random
import string


class User(AbstractUser):
    """Custom User model extending Django's AbstractUser"""
    email = models.EmailField(unique=True)
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_student = models.BooleanField(default=True)
    email_verified = models.BooleanField(default=False)
    google_id = models.CharField(max_length=255, blank=True, null=True, unique=True, help_text="Google account ID for OAuth")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.email


class EmailOTP(models.Model):
    """Model to store email OTP for verification"""
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_verified = models.BooleanField(default=False)
    signup_data = models.JSONField(default=dict, null=True, blank=True)  # Store registration data temporarily
    
    class Meta:
        verbose_name = 'Email OTP'
        verbose_name_plural = 'Email OTPs'
        indexes = [
            models.Index(fields=['email', 'otp']),
        ]
    
    def __str__(self):
        return f"OTP for {self.email}"
    
    @staticmethod
    def generate_otp():
        """Generate a 6-digit OTP"""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_expired(self):
        """Check if OTP has expired"""
        return timezone.now() > self.expires_at
    
    def verify(self, entered_otp):
        """Verify the OTP"""
        if self.is_expired():
            return False, "OTP has expired. Please request a new one."
        if self.is_verified:
            return False, "OTP has already been used."
        if self.otp != entered_otp:
            return False, "Invalid OTP. Please try again."
        
        self.is_verified = True
        self.save()
        return True, "OTP verified successfully."


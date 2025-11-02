from django.contrib import admin
from .models import User, EmailOTP


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'email_verified', 'google_id', 'is_staff', 'is_student', 'created_at')
    list_filter = ('is_staff', 'is_student', 'email_verified', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'google_id')
    readonly_fields = ('google_id',)


@admin.register(EmailOTP)
class EmailOTPAdmin(admin.ModelAdmin):
    list_display = ('email', 'otp', 'is_verified', 'created_at', 'expires_at')
    list_filter = ('is_verified', 'created_at', 'expires_at')
    search_fields = ('email',)
    readonly_fields = ('created_at', 'expires_at')


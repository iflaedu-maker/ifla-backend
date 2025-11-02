from rest_framework import serializers
from .models import Language, CourseLevel, Enrollment, ClassSchedule, Certificate, Invoice, EnrollmentApplication


class CourseLevelSerializer(serializers.ModelSerializer):
    """Serializer for CourseLevel model"""
    level_display = serializers.CharField(source='get_level_display', read_only=True)
    language_name = serializers.CharField(source='language.name', read_only=True)
    
    class Meta:
        model = CourseLevel
        fields = ['id', 'level', 'level_display', 'price', 'duration_weeks', 'description', 'language_name', 'language']


class LanguageSerializer(serializers.ModelSerializer):
    """Serializer for Language model"""
    levels = CourseLevelSerializer(many=True, read_only=True)
    
    class Meta:
        model = Language
        fields = ['id', 'name', 'flag_emoji', 'description', 'category', 'image_url', 'image_file', 'levels']


class ClassScheduleSerializer(serializers.ModelSerializer):
    """Serializer for ClassSchedule model"""
    day_display = serializers.CharField(source='get_day_of_week_display', read_only=True)
    
    class Meta:
        model = ClassSchedule
        fields = ['id', 'day_of_week', 'day_display', 'start_time', 'end_time', 'instructor_name', 'room_number', 'is_online', 'meeting_link']


class InvoiceSerializer(serializers.ModelSerializer):
    """Serializer for Invoice model"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Invoice
        fields = ['id', 'invoice_number', 'amount', 'tax_amount', 'total_amount', 'status', 'status_display', 'issued_date', 'due_date', 'paid_date', 'payment_method', 'invoice_file']


class CertificateSerializer(serializers.ModelSerializer):
    """Serializer for Certificate model"""
    
    class Meta:
        model = Certificate
        fields = ['id', 'certificate_number', 'issued_date', 'certificate_file', 'verification_url']


class EnrollmentSerializer(serializers.ModelSerializer):
    """Serializer for Enrollment model"""
    course_level = CourseLevelSerializer(read_only=True)
    language_name = serializers.CharField(source='course_level.language.name', read_only=True)
    class_schedule = ClassScheduleSerializer(read_only=True)
    certificate = CertificateSerializer(read_only=True)
    invoices = InvoiceSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ['id', 'course_level', 'language_name', 'class_schedule', 'status', 'status_display', 'enrolled_at', 'completed_at', 'progress_percentage', 'certificate', 'invoices']


class EnrollmentApplicationSerializer(serializers.ModelSerializer):
    """Serializer for EnrollmentApplication model"""
    language_name = serializers.CharField(source='language.name', read_only=True)
    levels_data = CourseLevelSerializer(source='levels', many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = EnrollmentApplication
        fields = [
            'id', 'user', 'language', 'language_name', 'levels', 'levels_data',
            'full_name', 'date_of_birth', 'phone_number', 'email', 'address',
            'schedule_type', 'preferred_hour',
            'photo', 'verification_document', 'signature', 'status', 'status_display',
            'total_amount', 'payment_reference', 'created_at', 'submitted_at'
        ]
        read_only_fields = ['user', 'total_amount', 'created_at', 'submitted_at']


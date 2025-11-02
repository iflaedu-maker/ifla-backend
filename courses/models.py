from django.db import models
from django.core.validators import MinValueValidator


class Language(models.Model):
    """Language model"""
    LANGUAGE_CATEGORIES = [
        (1, 'Category 1'),
        (2, 'Category 2'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    flag_emoji = models.CharField(max_length=10, blank=True)
    description = models.TextField()
    category = models.IntegerField(choices=LANGUAGE_CATEGORIES, default=1)
    image_url = models.URLField(blank=True)
    image_file = models.ImageField(upload_to='languages/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class CourseLevel(models.Model):
    """Course level model"""
    LEVEL_CHOICES = [
        ('A1', 'A1 - Beginner'),
        ('A2', 'A2 - Elementary'),
        ('B1', 'B1 - Intermediate'),
        ('B2', 'B2 - Upper Intermediate'),
        ('C1', 'C1 - Advanced'),
        ('C2', 'C2 - Proficient'),
    ]
    
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='levels')
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    duration_weeks = models.IntegerField(default=12)
    description = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['language', 'level']
        ordering = ['language', 'level']
    
    def __str__(self):
        return f"{self.language.name} - {self.get_level_display()}"


class ClassSchedule(models.Model):
    """Class schedule/timing for a course level"""
    DAYS_OF_WEEK = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ]
    
    course_level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name='schedules')
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    instructor_name = models.CharField(max_length=100, blank=True)
    room_number = models.CharField(max_length=50, blank=True)
    is_online = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['day_of_week', 'start_time']
    
    def __str__(self):
        return f"{self.course_level} - {self.get_day_of_week_display()} {self.start_time}"


class Enrollment(models.Model):
    """Student enrollment in a course"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='enrollments')
    course_level = models.ForeignKey(CourseLevel, on_delete=models.CASCADE, related_name='enrollments')
    class_schedule = models.ForeignKey(ClassSchedule, on_delete=models.SET_NULL, null=True, blank=True, related_name='enrollments')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    progress_percentage = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    
    class Meta:
        unique_together = ['user', 'course_level']
        ordering = ['-enrolled_at']
    
    def __str__(self):
        return f"{self.user.email} - {self.course_level}"


class Certificate(models.Model):
    """Certificate issued to student upon course completion"""
    STATUS_CHOICES = [
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    enrollment = models.OneToOneField(Enrollment, on_delete=models.CASCADE, related_name='certificate')
    certificate_number = models.CharField(max_length=50, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issued_date = models.DateField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_certificates')
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)
    verification_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-issued_date']
    
    def __str__(self):
        return f"Certificate {self.certificate_number} - {self.enrollment.user.email}"


class Invoice(models.Model):
    """Invoice for course enrollment"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    ]
    
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='invoices')
    invoice_number = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    invoice_file = models.FileField(upload_to='invoices/', blank=True, null=True)
    
    class Meta:
        ordering = ['-issued_date']
    
    def __str__(self):
        return f"Invoice {self.invoice_number} - {self.enrollment.user.email}"


class EnrollmentApplication(models.Model):
    """Detailed enrollment application with all student information"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('payment_pending', 'Payment Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='enrollment_applications')
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='applications')
    levels = models.ManyToManyField(CourseLevel, related_name='applications')
    
    # Personal Information
    full_name = models.CharField(max_length=200)
    date_of_birth = models.DateField()
    phone_number = models.CharField(max_length=17)
    email = models.EmailField()
    address = models.TextField(help_text='Full address', blank=True)
    
    # Personal Photo
    photo = models.ImageField(
        upload_to='student_photos/',
        help_text='Upload your photo',
        blank=True,
        null=True
    )
    
    # Verification Documents
    verification_document = models.FileField(
        upload_to='verification_documents/',
        help_text='Upload ID proof (PDF, Image, or Document)',
        blank=True,
        null=True
    )
    signature = models.ImageField(
        upload_to='signatures/',
        help_text='Upload your signature image',
        blank=True,
        null=True
    )
    
    # Status and Metadata
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    # Payment fields
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=255, blank=True)
    payment_status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('refunded', 'Refunded'),
        ],
        default='pending'
    )
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Class Schedule Preferences
    SCHEDULE_TYPE_CHOICES = [
        ('weekday', 'Weekday (1 hour)'),
        ('weekend', 'Weekend (2 hours)'),
    ]
    schedule_type = models.CharField(
        max_length=10,
        choices=SCHEDULE_TYPE_CHOICES,
        blank=True,
        help_text='Preferred schedule type'
    )
    preferred_hour = models.CharField(
        max_length=10,
        blank=True,
        help_text='Preferred hour for weekday classes (e.g., "9:00 AM", "2:00 PM")'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    submitted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.full_name} - {self.language.name} ({self.status})"
    
    def calculate_total_amount(self):
        """Calculate total amount based on selected levels"""
        total = sum(level.price for level in self.levels.all())
        self.total_amount = total
        return total


from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Language, CourseLevel, Enrollment, EnrollmentApplication, ClassSchedule, Certificate, Invoice


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'flag_emoji', 'category', 'levels_count', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    
    def levels_count(self, obj):
        count = obj.levels.count()
        return format_html('<strong>{}</strong>', count)
    levels_count.short_description = 'Course Levels'


@admin.register(CourseLevel)
class CourseLevelAdmin(admin.ModelAdmin):
    list_display = ['language', 'level', 'price_display', 'duration_weeks', 'enrollments_count']
    list_filter = ['language', 'level']
    search_fields = ['language__name', 'level']
    
    def price_display(self, obj):
        return format_html('<strong>₹{:,}</strong>', obj.price)
    price_display.short_description = 'Price'
    
    def enrollments_count(self, obj):
        count = obj.enrollments.count()
        return format_html('<strong>{}</strong>', count)
    enrollments_count.short_description = 'Enrollments'


@admin.register(ClassSchedule)
class ClassScheduleAdmin(admin.ModelAdmin):
    list_display = ['course_level', 'day_of_week', 'time_display', 'instructor_name', 'is_online']
    list_filter = ['day_of_week', 'is_online', 'course_level__language']
    search_fields = ['course_level__language__name', 'instructor_name', 'room_number']
    
    def time_display(self, obj):
        return f"{obj.start_time.strftime('%I:%M %p')} - {obj.end_time.strftime('%I:%M %p')}"
    time_display.short_description = 'Time'


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['user_email', 'course_info', 'status_badge', 'status', 'progress_bar', 'enrolled_at']
    list_filter = ['status', 'enrolled_at', 'course_level__language']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'course_level__language__name']
    readonly_fields = ['enrolled_at']
    list_editable = ['status']
    actions = ['mark_active', 'mark_completed', 'mark_cancelled']
    
    def user_email(self, obj):
        return format_html('<strong>{}</strong>', obj.user.email)
    user_email.short_description = 'User'
    
    def course_info(self, obj):
        return format_html(
            '{} {} - {}',
            obj.course_level.language.flag_emoji,
            obj.course_level.language.name,
            obj.course_level.get_level_display()
        )
    course_info.short_description = 'Course'
    
    def status_badge(self, obj):
        colors = {
            'active': 'green',
            'pending': 'orange',
            'completed': 'blue',
            'cancelled': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def progress_bar(self, obj):
        return format_html(
            '<div style="width: 100px; height: 8px; background: #eee; border-radius: 4px; overflow: hidden;"><div style="width: {}%; height: 100%; background: linear-gradient(90deg, #4CAF50, #45a049);"></div></div> {}%',
            obj.progress_percentage,
            obj.progress_percentage
        )
    progress_bar.short_description = 'Progress'
    
    def mark_active(self, request, queryset):
        queryset.update(status='active')
    mark_active.short_description = 'Mark selected as Active'
    
    def mark_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_completed.short_description = 'Mark selected as Completed'
    
    def mark_cancelled(self, request, queryset):
        queryset.update(status='cancelled')
    mark_cancelled.short_description = 'Mark selected as Cancelled'


@admin.register(EnrollmentApplication)
class EnrollmentApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email_display', 'language_badge', 'status_badge', 'payment_status_badge', 'total_amount_display', 'created_at']
    list_filter = ['status', 'payment_status', 'language', 'created_at', 'submitted_at']
    search_fields = ['full_name', 'email', 'phone_number', 'user__email']
    readonly_fields = ['created_at', 'updated_at', 'submitted_at', 'paid_at', 'document_links']
    filter_horizontal = ['levels']
    actions = ['approve_applications', 'reject_applications', 'mark_payment_success']
    
    fieldsets = (
        ('Student Information', {
            'fields': ('user', 'full_name', 'email', 'phone_number', 'date_of_birth', 'address', 'photo')
        }),
        ('Course Details', {
            'fields': ('language', 'levels', 'total_amount', 'schedule_type', 'preferred_hour')
        }),
        ('Documents', {
            'fields': ('verification_document', 'signature', 'document_links')
        }),
        ('Status & Payment', {
            'fields': ('status', 'payment_status', 'payment_reference', 'razorpay_order_id', 'razorpay_payment_id', 'paid_at')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'submitted_at'),
            'classes': ('collapse',)
        }),
    )
    
    def email_display(self, obj):
        return format_html('<a href="mailto:{}">{}</a>', obj.email, obj.email)
    email_display.short_description = 'Email'
    
    def language_badge(self, obj):
        return format_html(
            '<span style="font-size: 18px;">{} {}</span>',
            obj.language.flag_emoji,
            obj.language.name
        )
    language_badge.short_description = 'Language'
    
    def status_badge(self, obj):
        colors = {
            'draft': 'gray',
            'submitted': 'blue',
            'payment_pending': 'orange',
            'approved': 'green',
            'rejected': 'red'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def payment_status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'success': 'green',
            'failed': 'red',
            'refunded': 'purple'
        }
        color = colors.get(obj.payment_status, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_payment_status_display()
        )
    payment_status_badge.short_description = 'Payment'
    
    def total_amount_display(self, obj):
        return format_html('<strong>₹{:,}</strong>', obj.total_amount)
    total_amount_display.short_description = 'Amount'
    
    def document_links(self, obj):
        links = []
        if obj.photo:
            links.append(format_html(
                '<a href="{}" target="_blank" style="display: inline-block; margin: 5px; padding: 8px 16px; background: #9C27B0; color: white; text-decoration: none; border-radius: 4px;">📷 View Photo</a>',
                obj.photo.url
            ))
        if obj.verification_document:
            links.append(format_html(
                '<a href="{}" target="_blank" style="display: inline-block; margin: 5px; padding: 8px 16px; background: #4CAF50; color: white; text-decoration: none; border-radius: 4px;">📄 View Verification Doc</a>',
                obj.verification_document.url
            ))
        if obj.signature:
            links.append(format_html(
                '<a href="{}" target="_blank" style="display: inline-block; margin: 5px; padding: 8px 16px; background: #2196F3; color: white; text-decoration: none; border-radius: 4px;">✍️ View Signature</a>',
                obj.signature.url
            ))
        return mark_safe(''.join(links)) if links else 'No documents'
    document_links.short_description = 'Documents'
    
    def approve_applications(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} applications approved.")
    approve_applications.short_description = 'Approve selected applications'
    
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} applications rejected.")
    reject_applications.short_description = 'Reject selected applications'
    
    def mark_payment_success(self, request, queryset):
        from django.utils import timezone
        queryset.update(payment_status='success', paid_at=timezone.now())
        self.message_user(request, f"Payment marked as success for {queryset.count()} applications.")
    mark_payment_success.short_description = 'Mark payment as success'


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ['certificate_number', 'enrollment_info', 'issued_date', 'certificate_link']
    list_filter = ['issued_date']
    search_fields = ['certificate_number', 'enrollment__user__email']
    readonly_fields = ['issued_date']
    
    def enrollment_info(self, obj):
        return format_html(
            '{} - {}',
            obj.enrollment.user.email,
            obj.enrollment.course_level
        )
    enrollment_info.short_description = 'Enrollment'
    
    def certificate_link(self, obj):
        if obj.certificate_file:
            return format_html('<a href="{}" target="_blank">📄 Download</a>', obj.certificate_file.url)
        return 'No file'
    certificate_link.short_description = 'Certificate'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'enrollment_info', 'total_amount_display', 'status_badge', 'issued_date', 'due_date']
    list_filter = ['status', 'issued_date', 'due_date']
    search_fields = ['invoice_number', 'enrollment__user__email']
    readonly_fields = ['issued_date']
    actions = ['mark_paid', 'mark_overdue']
    
    def enrollment_info(self, obj):
        return format_html('{} - {}', obj.enrollment.user.email, obj.enrollment.course_level)
    enrollment_info.short_description = 'Enrollment'
    
    def total_amount_display(self, obj):
        return format_html('<strong>₹{:,}</strong>', obj.total_amount)
    total_amount_display.short_description = 'Amount'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'paid': 'green',
            'overdue': 'red',
            'cancelled': 'gray'
        }
        color = colors.get(obj.status, 'gray')
        return format_html(
            '<span style="background: {}; color: white; padding: 4px 12px; border-radius: 12px; font-size: 11px; font-weight: bold;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def mark_paid(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='paid', paid_date=timezone.now().date())
        self.message_user(request, f"{queryset.count()} invoices marked as paid.")
    mark_paid.short_description = 'Mark selected as Paid'
    
    def mark_overdue(self, request, queryset):
        queryset.update(status='overdue')
        self.message_user(request, f"{queryset.count()} invoices marked as overdue.")
    mark_overdue.short_description = 'Mark selected as Overdue'


from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Count, Sum, Q
from django.utils import timezone
from django.http import JsonResponse
from django.conf import settings
from django.core.files import File
from accounts.models import User
from .models import (
    Language, CourseLevel, Enrollment, EnrollmentApplication,
    ClassSchedule, Certificate, Invoice
)


def is_staff(user):
    """Check if user is staff/admin"""
    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff, login_url='/auth/')
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    # Get statistics
    stats = {
        'total_languages': Language.objects.count(),
        'total_courses': CourseLevel.objects.count(),
        'total_enrollments': Enrollment.objects.count(),
        'active_enrollments': Enrollment.objects.filter(status='active').count(),
        'pending_applications': EnrollmentApplication.objects.filter(status__in=['submitted', 'payment_pending']).count(),
        'total_applications': EnrollmentApplication.objects.count(),
        'total_revenue': EnrollmentApplication.objects.filter(payment_status='success').aggregate(
            total=Sum('total_amount')
        )['total'] or 0,
        'certificates_issued': Certificate.objects.count(),
        'pending_invoices': Invoice.objects.filter(status='pending').count(),
        'total_users': User.objects.count(),
        'active_users': User.objects.filter(is_active=True).count(),
        'staff_users': User.objects.filter(is_staff=True).count(),
        'student_users': User.objects.filter(is_student=True).count(),
    }
    
    # Recent applications
    recent_applications = EnrollmentApplication.objects.select_related(
        'user', 'language'
    ).prefetch_related('levels').order_by('-created_at')[:10]
    
    # Recent enrollments
    recent_enrollments = Enrollment.objects.select_related(
        'user', 'course_level__language'
    ).order_by('-enrolled_at')[:10]
    
    # Applications by status
    applications_by_status = EnrollmentApplication.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Enrollments by status
    enrollments_by_status = Enrollment.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Enrollments by language - count how many people enrolled in each language
    enrollments_by_language = Enrollment.objects.values(
        'course_level__language__name',
        'course_level__language__flag_emoji'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    context = {
        'stats': stats,
        'recent_applications': recent_applications,
        'recent_enrollments': recent_enrollments,
        'applications_by_status': applications_by_status,
        'enrollments_by_status': enrollments_by_status,
        'enrollments_by_language': enrollments_by_language,
    }
    
    return render(request, 'admin/dashboard.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_applications(request):
    """List all enrollment applications"""
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    applications = EnrollmentApplication.objects.select_related(
        'user', 'language'
    ).prefetch_related('levels').all()
    
    if status_filter != 'all':
        applications = applications.filter(status=status_filter)
    
    if search_query:
        applications = applications.filter(
            full_name__icontains=search_query
        ) | applications.filter(
            email__icontains=search_query
        ) | applications.filter(
            phone_number__icontains=search_query
        )
    
    applications = applications.order_by('-created_at')
    
    context = {
        'applications': applications,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'admin/applications.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_application_detail(request, application_id):
    """View detailed enrollment application"""
    application = get_object_or_404(
        EnrollmentApplication.objects.select_related('user', 'language').prefetch_related('levels'),
        id=application_id
    )
    
    context = {
        'application': application,
        'levels': application.levels.all(),
    }
    
    return render(request, 'admin/application_detail.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_update_application_status(request, application_id):
    """Update application status"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    application = get_object_or_404(EnrollmentApplication, id=application_id)
    new_status = request.POST.get('status')
    
    if new_status not in dict(EnrollmentApplication.STATUS_CHOICES):
        return JsonResponse({'error': 'Invalid status'}, status=400)
    
    application.status = new_status
    application.save()
    
    messages.success(request, f'Application status updated to {application.get_status_display()}')
    
    # If approved, create enrollment records
    if new_status == 'approved':
        from .views import payment_success
        # Create enrollments similar to payment success
        levels = application.levels.all()
        for level in levels:
            Enrollment.objects.get_or_create(
                user=application.user,
                course_level=level,
                defaults={
                    'status': 'active',
                    'progress_percentage': 0,
                }
            )
    
    return JsonResponse({'success': True, 'status': new_status})


@user_passes_test(is_staff, login_url='/auth/')
def admin_enrollments(request):
    """List all enrollments"""
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    enrollments = Enrollment.objects.select_related(
        'user', 'course_level__language', 'class_schedule'
    ).prefetch_related('user__enrollment_applications').all()
    
    if status_filter != 'all':
        enrollments = enrollments.filter(status=status_filter)
    
    if search_query:
        enrollments = enrollments.filter(
            user__email__icontains=search_query
        ) | enrollments.filter(
            course_level__language__name__icontains=search_query
        )
    
    enrollments = enrollments.order_by('-enrolled_at')
    
    context = {
        'enrollments': enrollments,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'admin/enrollments.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_update_enrollment(request, enrollment_id):
    """Update enrollment status or progress"""
    from .models import Certificate
    import uuid
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    status = request.POST.get('status')
    progress = request.POST.get('progress_percentage')
    
    if status and status in dict(Enrollment.STATUS_CHOICES):
        enrollment.status = status
        if status == 'completed':
            enrollment.completed_at = timezone.now()
            
            # Create certificate if it doesn't exist when enrollment is completed
            if not hasattr(enrollment, 'certificate'):
                certificate_number = f"IFLA-{uuid.uuid4().hex[:8].upper()}"
                Certificate.objects.create(
                    enrollment=enrollment,
                    certificate_number=certificate_number,
                    status='pending'
                )
    
    if progress:
        try:
            progress = int(progress)
            if 0 <= progress <= 100:
                enrollment.progress_percentage = progress
        except ValueError:
            pass
    
    enrollment.save()
    
    messages.success(request, 'Enrollment updated successfully')
    return JsonResponse({'success': True})


@user_passes_test(is_staff, login_url='/auth/')
def admin_courses(request):
    """Manage courses and languages"""
    languages = Language.objects.prefetch_related('levels').all()
    
    context = {
        'languages': languages,
    }
    
    return render(request, 'admin/courses.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_certificates(request):
    """List all enrollments for certificate approval"""
    from .models import Certificate
    
    status_filter = request.GET.get('status', 'all')
    search_query = request.GET.get('search', '')
    
    # Get all enrollments with their certificates (if any)
    enrollments = Enrollment.objects.select_related(
        'user', 'course_level__language', 'class_schedule'
    ).all()
    
    # Filter by enrollment status
    if status_filter != 'all':
        enrollments = enrollments.filter(status=status_filter)
    
    # Search filter
    if search_query:
        enrollments = enrollments.filter(
            Q(user__email__icontains=search_query) |
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(course_level__language__name__icontains=search_query)
        )
    
    enrollments = enrollments.order_by('-enrolled_at')
    
    # Annotate each enrollment with certificate status
    enrollment_data = []
    for enrollment in enrollments:
        # Try to get certificate using OneToOne relationship
        cert = None
        try:
            cert = enrollment.certificate
        except Certificate.DoesNotExist:
            pass
        
        enrollment_data.append({
            'enrollment': enrollment,
            'certificate': cert,
            'has_certificate': cert is not None,
            'certificate_approved': cert.status == 'approved' if cert else False,
        })
    
    context = {
        'enrollments_data': enrollment_data,
        'status_filter': status_filter,
        'search_query': search_query,
    }
    
    return render(request, 'admin/certificates.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_approve_certificate(request, enrollment_id):
    """Create and approve certificate for an enrollment"""
    from .models import Certificate
    from .utils import generate_certificate_pdf
    import uuid
    
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if request.method == 'POST':
        # Check if certificate already exists
        certificate, created = Certificate.objects.get_or_create(
            enrollment=enrollment,
            defaults={
                'certificate_number': f"IFLA-{uuid.uuid4().hex[:8].upper()}",
                'status': 'pending'
            }
        )
        
        # Update certificate status to approved
        certificate.status = 'approved'
        certificate.approved_by = request.user
        certificate.approved_date = timezone.now()
        
        # Generate certificate number if not exists
        if not certificate.certificate_number:
            certificate.certificate_number = f"IFLA-{uuid.uuid4().hex[:8].upper()}"
        
        # Generate PDF certificate
        try:
            pdf_path = generate_certificate_pdf(certificate)
            from django.core.files import File
            import os
            
            # Open the generated file and save to FileField
            file_path = os.path.join(settings.MEDIA_ROOT, pdf_path)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    certificate.certificate_file.save(
                        os.path.basename(pdf_path),
                        File(f),
                        save=False
                    )
                certificate.save()
                messages.success(request, f'Certificate approved and PDF generated successfully for {enrollment.user.email}!')
            else:
                messages.error(request, f'PDF file was not created at {file_path}')
                certificate.save()  # Save status even if PDF fails
        except Exception as e:
            import traceback
            traceback.print_exc()
            messages.error(request, f'Error generating PDF: {str(e)}')
            certificate.save()  # Save status even if PDF fails
        
        return redirect('admin-certificates')
    
    return redirect('admin-certificates')


@user_passes_test(is_staff, login_url='/auth/')
def admin_reject_certificate(request, certificate_id):
    """Reject certificate"""
    from .models import Certificate
    
    certificate = get_object_or_404(Certificate, id=certificate_id)
    
    if request.method == 'POST':
        certificate.status = 'rejected'
        certificate.approved_by = request.user
        certificate.approved_date = timezone.now()
        certificate.save()
        
        messages.success(request, 'Certificate rejected.')
        return redirect('admin-certificates')
    
    return redirect('admin-certificates')


@user_passes_test(is_staff, login_url='/auth/')
def admin_update_user(request, user_id):
    """Update user status or permissions"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    user = get_object_or_404(User, id=user_id)
    
    # Only superusers can modify staff/superuser status
    if request.user.is_superuser:
        is_staff = request.POST.get('is_staff')
        is_student = request.POST.get('is_student')
        is_active = request.POST.get('is_active')
        
        if is_staff is not None:
            user.is_staff = is_staff.lower() == 'true'
        if is_student is not None:
            user.is_student = is_student.lower() == 'true'
        if is_active is not None:
            user.is_active = is_active.lower() == 'true'
    
    # Regular staff can update other fields
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    phone_number = request.POST.get('phone_number')
    
    if first_name:
        user.first_name = first_name
    if last_name:
        user.last_name = last_name
    if phone_number:
        user.phone_number = phone_number
    
    user.save()
    
    messages.success(request, f'User {user.email} updated successfully')
    return JsonResponse({'success': True})


@user_passes_test(is_staff, login_url='/auth/')
def admin_analytics(request):
    """Analytics and reports dashboard"""
    from django.utils import timezone
    from datetime import timedelta
    
    # Time ranges
    today = timezone.now().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    year_ago = today - timedelta(days=365)
    
    # Enrollment trends
    enrollments_today = Enrollment.objects.filter(enrolled_at__date=today).count()
    enrollments_week = Enrollment.objects.filter(enrolled_at__date__gte=week_ago).count()
    enrollments_month = Enrollment.objects.filter(enrolled_at__date__gte=month_ago).count()
    enrollments_year = Enrollment.objects.filter(enrolled_at__date__gte=year_ago).count()
    
    # Application trends
    applications_today = EnrollmentApplication.objects.filter(created_at__date=today).count()
    applications_week = EnrollmentApplication.objects.filter(created_at__date__gte=week_ago).count()
    applications_month = EnrollmentApplication.objects.filter(created_at__date__gte=month_ago).count()
    
    # Revenue trends
    revenue_today = EnrollmentApplication.objects.filter(
        payment_status='success',
        paid_at__date=today
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    revenue_week = EnrollmentApplication.objects.filter(
        payment_status='success',
        paid_at__date__gte=week_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    revenue_month = EnrollmentApplication.objects.filter(
        payment_status='success',
        paid_at__date__gte=month_ago
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Popular languages
    popular_languages = Language.objects.annotate(
        enrollment_count=Count('levels__enrollments')
    ).order_by('-enrollment_count')[:5]
    
    # Enrollment by status
    enrollments_by_status = Enrollment.objects.values('status').annotate(
        count=Count('id')
    )
    
    context = {
        'enrollments_today': enrollments_today,
        'enrollments_week': enrollments_week,
        'enrollments_month': enrollments_month,
        'enrollments_year': enrollments_year,
        'applications_today': applications_today,
        'applications_week': applications_week,
        'applications_month': applications_month,
        'revenue_today': revenue_today,
        'revenue_week': revenue_week,
        'revenue_month': revenue_month,
        'popular_languages': popular_languages,
        'enrollments_by_status': enrollments_by_status,
    }
    
    return render(request, 'admin/analytics.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_users(request):
    """User management - list all users with filtering"""
    # Get filter parameters
    search_query = request.GET.get('search', '').strip()
    role_filter = request.GET.get('role', 'all')
    
    # Base queryset with annotations
    users = User.objects.annotate(
        enrollments_count=Count('enrollments', distinct=True),
        applications_count=Count('enrollment_applications', distinct=True)
    ).prefetch_related('enrollment_applications').order_by('-date_joined')
    
    # Apply search filter
    if search_query:
        users = users.filter(
            Q(email__icontains=search_query) |
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        )
    
    # Apply role filter
    if role_filter == 'students':
        users = users.filter(is_student=True, is_staff=False)
    elif role_filter == 'staff':
        users = users.filter(is_staff=True)
    elif role_filter == 'superusers':
        users = users.filter(is_superuser=True)
    
    context = {
        'users': users,
        'search_query': search_query,
        'role_filter': role_filter,
        'total_users': User.objects.count(),
    }
    
    return render(request, 'admin/users.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_user_detail(request, user_id):
    """View detailed user information with enrollments"""
    user = get_object_or_404(User, id=user_id)
    
    # Get user's enrollments with related data
    enrollments = Enrollment.objects.filter(user=user).select_related(
        'course_level__language', 'class_schedule'
    ).order_by('-enrolled_at')
    
    # Get user's applications
    applications = EnrollmentApplication.objects.filter(user=user).select_related(
        'language'
    ).prefetch_related('levels').order_by('-created_at')
    
    # Get user's latest photo from enrollment application
    latest_application_with_photo = applications.filter(photo__isnull=False).first()
    user_photo = latest_application_with_photo.photo if latest_application_with_photo else None
    
    # Get user's certificates
    certificates = Certificate.objects.filter(
        enrollment__user=user
    ).select_related('enrollment__course_level__language')
    
    context = {
        'user_detail': user,
        'enrollments': enrollments,
        'applications': applications,
        'certificates': certificates,
        'user_photo': user_photo,
    }
    
    return render(request, 'admin/user_detail.html', context)


@user_passes_test(is_staff, login_url='/auth/')
def admin_add_user(request):
    """Add a new user"""
    if request.method == 'POST':
        try:
            email = request.POST.get('email', '').strip()
            username = request.POST.get('username', '').strip()
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            password = request.POST.get('password', '')
            is_staff = request.POST.get('is_staff') == 'on'
            is_student = request.POST.get('is_student') == 'on'
            
            # Validation
            if not email:
                messages.error(request, 'Email is required')
                return redirect('admin-users')
            
            if User.objects.filter(email=email).exists():
                messages.error(request, 'User with this email already exists')
                return redirect('admin-users')
            
            if not username:
                username = email.split('@')[0]
            
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('admin-users')
            
            # Create user
            user = User.objects.create(
                email=email,
                username=username,
                first_name=first_name,
                last_name=last_name,
                is_staff=is_staff,
                is_student=is_student,
            )
            
            if password:
                user.set_password(password)
            else:
                user.set_password('changeme123')  # Default password
            
            user.save()
            
            messages.success(request, f'User {email} created successfully!')
            return redirect('admin-user-detail', user_id=user.id)
            
        except Exception as e:
            messages.error(request, f'Error creating user: {str(e)}')
            return redirect('admin-users')
    
    return redirect('admin-users')


@user_passes_test(is_staff, login_url='/auth/')
def admin_delete_user(request, user_id):
    """Delete a user (soft delete by deactivating)"""
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            
            # Prevent deleting yourself
            if user.id == request.user.id:
                messages.error(request, 'You cannot delete your own account')
                return redirect('admin-users')
            
            # Soft delete - deactivate instead of deleting
            user.is_active = False
            user.save()
            
            messages.success(request, f'User {user.email} has been deactivated')
            
        except Exception as e:
            messages.error(request, f'Error deleting user: {str(e)}')
    
    return redirect('admin-users')


@user_passes_test(is_staff, login_url='/auth/')
def admin_toggle_user_status(request, user_id):
    """Toggle user active status"""
    if request.method == 'POST':
        try:
            user = get_object_or_404(User, id=user_id)
            
            if user.id == request.user.id:
                messages.error(request, 'You cannot deactivate your own account')
                return redirect('admin-users')
            
            user.is_active = not user.is_active
            user.save()
            
            status = 'activated' if user.is_active else 'deactivated'
            messages.success(request, f'User {user.email} has been {status}')
            
        except Exception as e:
            messages.error(request, f'Error updating user: {str(e)}')
    
    return redirect('admin-users')


# Language and Course Level Management
@user_passes_test(is_staff, login_url='/auth/')
def admin_add_language(request):
    """Add a new language"""
    if request.method == 'POST':
        try:
            name = request.POST.get('name', '').strip()
            flag_emoji = request.POST.get('flag_emoji', '').strip()
            description = request.POST.get('description', '').strip()
            category = int(request.POST.get('category', 1))
            image_url = request.POST.get('image_url', '').strip()
            
            if not name or not description:
                messages.error(request, 'Name and description are required')
                return redirect('admin-courses')
            
            if Language.objects.filter(name=name).exists():
                messages.error(request, 'Language with this name already exists')
                return redirect('admin-courses')
            
            language = Language.objects.create(
                name=name,
                flag_emoji=flag_emoji,
                description=description,
                category=category,
                image_url=image_url if image_url else ''
            )
            
            messages.success(request, f'Language "{name}" added successfully!')
        except Exception as e:
            messages.error(request, f'Error adding language: {str(e)}')
    
    return redirect('admin-courses')


@user_passes_test(is_staff, login_url='/auth/')
def admin_update_language(request, language_id):
    """Update an existing language"""
    if request.method == 'POST':
        try:
            language = get_object_or_404(Language, id=language_id)
            name = request.POST.get('name', '').strip()
            flag_emoji = request.POST.get('flag_emoji', '').strip()
            description = request.POST.get('description', '').strip()
            category = int(request.POST.get('category', 1))
            image_url = request.POST.get('image_url', '').strip()
            
            if not name or not description:
                messages.error(request, 'Name and description are required')
                return redirect('admin-courses')
            
            # Check if name conflicts with another language
            if Language.objects.filter(name=name).exclude(id=language_id).exists():
                messages.error(request, 'Language with this name already exists')
                return redirect('admin-courses')
            
            language.name = name
            language.flag_emoji = flag_emoji
            language.description = description
            language.category = category
            language.image_url = image_url if image_url else ''
            language.save()
            
            messages.success(request, f'Language "{name}" updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating language: {str(e)}')
    
    return redirect('admin-courses')


@user_passes_test(is_staff, login_url='/auth/')
def admin_delete_language(request, language_id):
    """Delete a language"""
    if request.method == 'POST':
        try:
            language = get_object_or_404(Language, id=language_id)
            language_name = language.name
            language.delete()
            messages.success(request, f'Language "{language_name}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting language: {str(e)}')
    
    return redirect('admin-courses')


@user_passes_test(is_staff, login_url='/auth/')
def admin_add_level(request):
    """Add a new course level"""
    if request.method == 'POST':
        try:
            language_id = request.POST.get('language_id')
            level = request.POST.get('level', '').strip()
            price = request.POST.get('price')
            duration_weeks = int(request.POST.get('duration_weeks', 12))
            description = request.POST.get('description', '').strip()
            
            if not language_id or not level or not price:
                messages.error(request, 'Language, level, and price are required')
                return redirect('admin-courses')
            
            language = get_object_or_404(Language, id=language_id)
            
            # Check if level already exists for this language
            if CourseLevel.objects.filter(language=language, level=level).exists():
                messages.error(request, f'Level {level} already exists for {language.name}')
                return redirect('admin-courses')
            
            CourseLevel.objects.create(
                language=language,
                level=level,
                price=price,
                duration_weeks=duration_weeks,
                description=description
            )
            
            messages.success(request, f'Course level {level} added to {language.name}!')
        except Exception as e:
            messages.error(request, f'Error adding course level: {str(e)}')
    
    return redirect('admin-courses')


@user_passes_test(is_staff, login_url='/auth/')
def admin_update_level(request, level_id):
    """Update an existing course level"""
    if request.method == 'POST':
        try:
            level_obj = get_object_or_404(CourseLevel, id=level_id)
            level = request.POST.get('level', '').strip()
            price = request.POST.get('price')
            duration_weeks = int(request.POST.get('duration_weeks', 12))
            description = request.POST.get('description', '').strip()
            
            if not level or not price:
                messages.error(request, 'Level and price are required')
                return redirect('admin-courses')
            
            # Check if level conflicts with another level for the same language
            if CourseLevel.objects.filter(language=level_obj.language, level=level).exclude(id=level_id).exists():
                messages.error(request, f'Level {level} already exists for {level_obj.language.name}')
                return redirect('admin-courses')
            
            level_obj.level = level
            level_obj.price = price
            level_obj.duration_weeks = duration_weeks
            level_obj.description = description
            level_obj.save()
            
            messages.success(request, f'Course level updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating course level: {str(e)}')
    
    return redirect('admin-courses')


@user_passes_test(is_staff, login_url='/auth/')
def admin_delete_level(request, level_id):
    """Delete a course level"""
    if request.method == 'POST':
        try:
            level_obj = get_object_or_404(CourseLevel, id=level_id)
            level_name = level_obj.get_level_display()
            level_obj.delete()
            messages.success(request, f'Course level "{level_name}" deleted successfully!')
        except Exception as e:
            messages.error(request, f'Error deleting course level: {str(e)}')
    
    return redirect('admin-courses')


# API endpoints for fetching language/level data
@user_passes_test(is_staff, login_url='/auth/')
def admin_get_language(request, language_id):
    """Get language data as JSON"""
    from .serializers import LanguageSerializer
    language = get_object_or_404(Language, id=language_id)
    serializer = LanguageSerializer(language)
    return JsonResponse(serializer.data)


@user_passes_test(is_staff, login_url='/auth/')
def admin_get_level(request, level_id):
    """Get course level data as JSON"""
    from .serializers import CourseLevelSerializer
    level = get_object_or_404(CourseLevel, id=level_id)
    serializer = CourseLevelSerializer(level)
    return JsonResponse(serializer.data)


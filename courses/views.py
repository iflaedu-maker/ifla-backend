from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import FileResponse, Http404
from django.conf import settings
import os
from .models import Language, CourseLevel, Enrollment, ClassSchedule, Certificate, Invoice
from .serializers import LanguageSerializer, CourseLevelSerializer, EnrollmentSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def language_list(request):
    """Get all languages"""
    languages = Language.objects.all()
    serializer = LanguageSerializer(languages, many=True)
    return Response(serializer.data)


def languages_page(request):
    """Render the languages page with database data"""
    languages = Language.objects.prefetch_related('levels').all().order_by('category', 'name')
    
    # Calculate price ranges for each language
    languages_with_prices = []
    for lang in languages:
        levels = lang.levels.all()
        if levels.exists():
            prices = [float(level.price) for level in levels]
            min_price = min(prices)
            max_price = max(prices)
            price_range = f"₹{int(min_price/1000)}K - ₹{int(max_price/1000)}K"
        else:
            price_range = "Price TBD"
        
        languages_with_prices.append({
            'language': lang,
            'price_range': price_range,
            'levels_count': levels.count()
        })
    
    context = {
        'languages_data': languages_with_prices,
        'languages': languages,  # Keep for backward compatibility
    }
    
    return render(request, 'languages.html', context)


@api_view(['GET'])
@permission_classes([AllowAny])
def language_detail(request, pk):
    """Get language details with course levels"""
    try:
        language = Language.objects.get(pk=pk)
        serializer = LanguageSerializer(language)
        return Response(serializer.data)
    except Language.DoesNotExist:
        return Response(
            {'error': 'Language not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@permission_classes([AllowAny])
def course_levels_by_language(request, language_id):
    """Get all course levels for a specific language"""
    try:
        language = Language.objects.get(pk=language_id)
        levels = CourseLevel.objects.filter(language=language)
        serializer = CourseLevelSerializer(levels, many=True)
        return Response(serializer.data)
    except Language.DoesNotExist:
        return Response(
            {'error': 'Language not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['POST'])
def enroll(request):
    """Enroll user in a course"""
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Authentication required'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    course_level_id = request.data.get('course_level_id')
    
    if not course_level_id:
        return Response(
            {'error': 'course_level_id is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        course_level = CourseLevel.objects.get(pk=course_level_id)
        
        # Check if already enrolled
        enrollment, created = Enrollment.objects.get_or_create(
            user=request.user,
            course_level=course_level,
            defaults={'status': 'pending'}
        )
        
        if not created:
            return Response(
                {'error': 'Already enrolled in this course'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = EnrollmentSerializer(enrollment)
        return Response(
            {'message': 'Enrollment successful', 'enrollment': serializer.data},
            status=status.HTTP_201_CREATED
        )
    except CourseLevel.DoesNotExist:
        return Response(
            {'error': 'Course level not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def my_enrollments(request):
    """Get current user's enrollments"""
    if not request.user.is_authenticated:
        return Response(
            {'error': 'Authentication required'},
            status=status.HTTP_401_UNAUTHORIZED
        )
    
    enrollments = Enrollment.objects.filter(user=request.user)
    serializer = EnrollmentSerializer(enrollments, many=True)
    return Response(serializer.data)


@login_required
def dashboard(request):
    """User dashboard view - Optimized for performance"""
    user = request.user
    
    # Optimize: Single query with all related data fetched
    enrollments_queryset = Enrollment.objects.filter(user=user).select_related(
        'course_level__language', 'class_schedule', 'certificate'
    ).prefetch_related('invoices')
    
    # Convert to list to avoid multiple queries - evaluate once
    enrollments_list = list(enrollments_queryset)
    
    # Get enrollment applications for the user - optimized
    enrollment_applications = EnrollmentApplication.objects.filter(user=user).select_related(
        'language'
    ).prefetch_related('levels').order_by('-created_at')[:50]  # Limit to recent 50
    
    # Get user's latest photo from enrollment application
    latest_application_with_photo = EnrollmentApplication.objects.filter(
        user=user,
        photo__isnull=False
    ).order_by('-created_at').first()
    user_photo = latest_application_with_photo.photo if latest_application_with_photo else None
    
    # Get only approved certificates that can be downloaded - optimized
    approved_certificates = Certificate.objects.filter(
        enrollment__user=user,
        status='approved',
        certificate_file__isnull=False
    ).select_related('enrollment__course_level__language')
    
    # Get invoices - optimized with select_related
    invoices = Invoice.objects.filter(enrollment__user=user).select_related('enrollment')
    
    # Pre-calculate counts to avoid queryset.count() in template (which causes extra queries)
    enrollments_count = len(enrollments_list)
    active_enrollments_count = sum(1 for e in enrollments_list if e.status == 'active')
    completed_enrollments_count = sum(1 for e in enrollments_list if e.status == 'completed')
    certificates_count = approved_certificates.count()  # Single count query
    invoices_count = invoices.count()  # Single count query
    
    # Organize data for template
    dashboard_data = {
        'user': user,
        'enrollments': enrollments_list,
        'active_enrollments': [e for e in enrollments_list if e.status == 'active'],
        'completed_enrollments': [e for e in enrollments_list if e.status == 'completed'],
        'certificates': approved_certificates,
        'invoices': invoices,
        'enrollment_applications': enrollment_applications,
        'user_photo': user_photo,
        # Pre-calculated counts
        'enrollments_count': enrollments_count,
        'active_enrollments_count': active_enrollments_count,
        'completed_enrollments_count': completed_enrollments_count,
        'certificates_count': certificates_count,
        'invoices_count': invoices_count,
    }
    
    return render(request, 'dashboard.html', dashboard_data)


from django.utils import timezone
from .models import EnrollmentApplication
from .serializers import EnrollmentApplicationSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import razorpay
import json

@login_required
def enrollment_form(request):
    """Enrollment form view - requires authentication"""
    if request.method == 'GET':
        # Get preselected language if provided
        language_id = request.GET.get('language_id')
        language_name = request.GET.get('language')
        
        # Get all languages for the dropdown
        languages = Language.objects.all().prefetch_related('levels')
        
        # If language_id provided, get the specific language
        selected_language = None
        if language_id:
            try:
                selected_language = Language.objects.get(id=language_id)
            except Language.DoesNotExist:
                pass
        elif language_name:
            # Try exact match first, then case-insensitive
            try:
                selected_language = Language.objects.get(name=language_name)
            except Language.DoesNotExist:
                try:
                    selected_language = Language.objects.get(name__iexact=language_name)
                except Language.DoesNotExist:
                    # Try partial match
                    try:
                        selected_language = Language.objects.filter(name__icontains=language_name).first()
                    except:
                        pass
        
        context = {
            'user': request.user,
            'languages': languages,
            'selected_language': selected_language,
            'selected_language_id': language_id,
        }
        
        # Check if this is an AJAX request (for modal)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.GET.get('modal') == 'true':
            return render(request, 'enrollment_form_content.html', context)
        
        return render(request, 'enrollment_form.html', context)
    
    elif request.method == 'POST':
        # Handle form submission
        try:
            # Get form data
            language_id = request.POST.get('language')
            level_ids = request.POST.getlist('levels')
            full_name = request.POST.get('full_name')
            date_of_birth = request.POST.get('date_of_birth')
            phone_number = request.POST.get('phone_number')
            email = request.POST.get('email')
            address = request.POST.get('address')
            schedule_type = request.POST.get('schedule_type')
            preferred_hour = request.POST.get('preferred_hour', '')
            
            # Get uploaded files
            photo = request.FILES.get('photo')
            verification_doc = request.FILES.get('verification_document')
            signature = request.FILES.get('signature')
            
            # Validate required fields
            if not all([language_id, level_ids, full_name, date_of_birth, phone_number, email, address, schedule_type, photo, verification_doc, signature]):
                return render(request, 'enrollment_form.html', {
                    'error': 'All fields are required',
                    'languages': Language.objects.all().prefetch_related('levels'),
                })
            
            # Validate preferred_hour for weekday schedule
            if schedule_type == 'weekday' and not preferred_hour:
                return render(request, 'enrollment_form.html', {
                    'error': 'Please select a preferred hour for weekday classes',
                    'languages': Language.objects.all().prefetch_related('levels'),
                })
            
            # Get language and levels
            language = Language.objects.get(id=language_id)
            levels = CourseLevel.objects.filter(id__in=level_ids, language=language)
            
            if not levels.exists():
                return render(request, 'enrollment_form.html', {
                    'error': 'Please select at least one valid level',
                    'languages': Language.objects.all().prefetch_related('levels'),
                })
            
            # Create enrollment application
            application = EnrollmentApplication.objects.create(
                user=request.user,
                language=language,
                full_name=full_name,
                date_of_birth=date_of_birth,
                phone_number=phone_number,
                email=email,
                address=address,
                schedule_type=schedule_type,
                preferred_hour=preferred_hour if schedule_type == 'weekday' else '',
                photo=photo,
                verification_document=verification_doc,
                signature=signature,
                status='submitted',
                submitted_at=timezone.now()
            )
            
            # Add selected levels
            application.levels.set(levels)
            
            # Calculate total amount
            total_amount = application.calculate_total_amount()
            application.save()
            
            # Redirect to payment portal with application details
            return redirect(reverse('payment-portal') + f'?application_id={application.id}')
            
        except Exception as e:
            return render(request, 'enrollment_form.html', {
                'error': f'An error occurred: {str(e)}',
                'languages': Language.objects.all().prefetch_related('levels'),
            })
    
    return render(request, 'enrollment_form.html', {
        'languages': Language.objects.all().prefetch_related('levels'),
    })


@login_required
def payment_portal(request):
    """Payment portal view"""
    application_id = request.GET.get('application_id')
    
    if not application_id:
        return redirect('languages')
    
    try:
        application = EnrollmentApplication.objects.get(
            id=application_id,
            user=request.user
        )
        
        # Get Razorpay key from settings
        razorpay_key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
        
        context = {
            'application': application,
            'levels': application.levels.all(),
            'total_amount': application.total_amount,
            'razorpay_key_id': razorpay_key_id,
            'application_id': application.id,
        }
        
        return render(request, 'payment_portal.html', context)
        
    except EnrollmentApplication.DoesNotExist:
        return redirect('languages')


@login_required
def create_payment_order(request):
    """Create Razorpay order for payment"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        application_id = request.POST.get('application_id')
        
        if not application_id:
            return JsonResponse({'error': 'Application ID is required'}, status=400)
        
        application = EnrollmentApplication.objects.get(
            id=application_id,
            user=request.user
        )
        
        # Check if payment already completed
        if application.payment_status == 'success':
            return JsonResponse({'error': 'Payment already completed'}, status=400)
        
        # Initialize Razorpay client
        razorpay_key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
        razorpay_key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        
        if not razorpay_key_id or not razorpay_key_secret:
            return JsonResponse({'error': 'Payment gateway not configured'}, status=500)
        
        client = razorpay.Client(auth=(razorpay_key_id, razorpay_key_secret))
        
        # Create order
        # Convert amount to paise (Razorpay uses smallest currency unit)
        amount = int(float(application.total_amount) * 100)
        
        order_data = {
            'amount': amount,
            'currency': 'INR',
            'receipt': f'IFLA_{application.id}',
            'notes': {
                'application_id': str(application.id),
                'user_email': application.email,
                'user_name': application.full_name,
            }
        }
        
        order = client.order.create(data=order_data)
        
        # Save order ID to application
        application.razorpay_order_id = order['id']
        application.payment_status = 'pending'
        application.status = 'payment_pending'
        application.save()
        
        return JsonResponse({
            'order_id': order['id'],
            'amount': order['amount'],
            'currency': order['currency'],
            'key_id': razorpay_key_id,
        })
        
    except EnrollmentApplication.DoesNotExist:
        return JsonResponse({'error': 'Application not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def payment_webhook(request):
    """Handle Razorpay webhook callbacks"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        # Get webhook data
        webhook_data = json.loads(request.body)
        event = webhook_data.get('event')
        payload = webhook_data.get('payload', {})
        payment = payload.get('payment', {})
        order = payload.get('order', {})
        
        # Verify webhook signature (recommended for production)
        razorpay_key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        
        # Find application by order ID
        order_id = order.get('id') or payment.get('order_id')
        if order_id:
            try:
                application = EnrollmentApplication.objects.get(razorpay_order_id=order_id)
                
                if event == 'payment.captured':
                    # Payment successful
                    application.payment_status = 'success'
                    application.payment_reference = payment.get('id', '')
                    application.razorpay_payment_id = payment.get('id', '')
                    application.status = 'submitted'  # Change back to submitted after payment
                    application.paid_at = timezone.now()
                    application.save()
                    
                elif event == 'payment.failed':
                    # Payment failed
                    application.payment_status = 'failed'
                    application.save()
                    
            except EnrollmentApplication.DoesNotExist:
                pass
        
        return JsonResponse({'status': 'ok'})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def payment_success(request):
    """Handle successful payment redirect - Simplified version without actual payment"""
    application_id = request.GET.get('application_id')
    
    if not application_id:
        return redirect('languages')
    
    try:
        application = EnrollmentApplication.objects.get(
            id=application_id,
            user=request.user
        )
        
        # Update application status to approved and payment status to success
        application.status = 'approved'
        application.payment_status = 'success'
        application.paid_at = timezone.now()
        application.save()
        
        # Create Enrollment records for each course level in the application
        # This makes them appear in the "Enrolled Courses" section of the dashboard
        levels = application.levels.all()
        created_enrollments = []
        
        for level in levels:
            # Check if enrollment already exists (avoid duplicates)
            enrollment, created = Enrollment.objects.get_or_create(
                user=request.user,
                course_level=level,
                defaults={
                    'status': 'active',  # Set to active since payment is successful
                    'progress_percentage': 0,
                }
            )
            
            if created:
                created_enrollments.append(enrollment)
        
        # Redirect to dashboard where enrollments will now be visible
        return redirect(reverse('dashboard'))
        
    except EnrollmentApplication.DoesNotExist:
        return redirect('languages')


@login_required
def download_certificate(request, certificate_id):
    """Download certificate PDF - secure endpoint with user verification"""
    try:
        # Get the certificate and verify it belongs to the logged-in user
        certificate = get_object_or_404(
            Certificate,
            id=certificate_id,
            enrollment__user=request.user,
            status='approved'
        )
        
        # Check if certificate file exists
        if not certificate.certificate_file:
            raise Http404("Certificate file not found")
        
        # Get the file using Django's storage system
        file_obj = certificate.certificate_file
        
        # Prepare filename
        filename = f'certificate_{certificate.certificate_number}.pdf'
        
        # Try to get the file path for local storage, otherwise use the file object directly
        try:
            file_path = file_obj.path
            if os.path.exists(file_path):
                # Local file system - open file directly
                file_handle = open(file_path, 'rb')
                response = FileResponse(
                    file_handle,
                    content_type='application/pdf',
                    as_attachment=True,
                    filename=filename
                )
            else:
                raise FileNotFoundError()
        except (NotImplementedError, AttributeError, FileNotFoundError):
            # Remote storage or path not available - use file object directly
            file_obj.open('rb')
            response = FileResponse(
                file_obj,
                content_type='application/pdf',
                as_attachment=True,
                filename=filename
            )
        
        # Set Content-Disposition header for download (ensure proper filename encoding)
        import urllib.parse
        encoded_filename = urllib.parse.quote(filename)
        response['Content-Disposition'] = f'attachment; filename="{filename}"; filename*=UTF-8\'\'{encoded_filename}'
        
        return response
        
    except Http404:
        raise
    except Exception as e:
        # Log the error for debugging
        import traceback
        import sys
        print(f"Error downloading certificate: {str(e)}", file=sys.stderr)
        traceback.print_exc()
        raise Http404(f"Certificate not found or access denied")


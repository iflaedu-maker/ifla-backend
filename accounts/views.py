from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect
from datetime import timedelta
import requests
from .models import User, EmailOTP
from .serializers import UserSerializer, LoginSerializer, SignupSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    """Send OTP to email for registration"""
    try:
        serializer = SignupSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            username = serializer.validated_data.get('username', '').strip()
            
            # Check if user already exists by email
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'User with this email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # If username not provided, use email as username
            if not username:
                username = email
            
            # Check if username already exists
            if User.objects.filter(username=username).exists():
                return Response(
                    {'error': 'This username is already taken. Please choose another.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generate OTP
            otp = EmailOTP.generate_otp()
            expires_at = timezone.now() + timedelta(minutes=10)  # OTP expires in 10 minutes
            
            # Delete any existing unverified OTPs for this email
            EmailOTP.objects.filter(email=email, is_verified=False).delete()
            
            # Store signup data temporarily
            signup_data = {
                'email': email,
                'username': username,
                'first_name': serializer.validated_data.get('first_name', ''),
                'last_name': serializer.validated_data.get('last_name', ''),
                'password': serializer.validated_data['password']
            }
            
            # Create OTP record
            email_otp = EmailOTP.objects.create(
                email=email,
                otp=otp,
                expires_at=expires_at,
                signup_data=signup_data
            )
            
            # Send OTP email
            subject = 'IFLA - Email Verification OTP'
            message = f'''
Hello,

Thank you for registering with IFLA!

Your verification code is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
IFLA Team
            '''
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ifla.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                # If email sending fails, still return success in development
                # In production, you should handle this properly
                print(f"Email sending failed: {str(e)}")
                if settings.DEBUG:
                    print(f"OTP for {email}: {otp}")  # Print OTP in console for development
            
            return Response(
                {
                    'message': 'OTP sent to your email. Please check your inbox.',
                    'email': email
                },
                status=status.HTTP_200_OK
            )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp_and_signup(request):
    """Verify OTP and create user account"""
    try:
        email = request.data.get('email', '').strip()
        otp = request.data.get('otp', '').strip()
        
        if not email or not otp:
            return Response(
                {'error': 'Email and OTP are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find the OTP record
        try:
            email_otp = EmailOTP.objects.filter(email=email, is_verified=False).order_by('-created_at').first()
            
            if not email_otp:
                return Response(
                    {'error': 'No OTP found for this email. Please request a new one.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Verify OTP
            is_valid, message = email_otp.verify(otp)
            
            if not is_valid:
                return Response(
                    {'error': message},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Get signup data
            signup_data = email_otp.signup_data
            
            # Check if user already exists (race condition check)
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'User with this email already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create user
            user = User.objects.create(
                username=signup_data['username'],
                email=signup_data['email'],
                first_name=signup_data.get('first_name', ''),
                last_name=signup_data.get('last_name', ''),
                password=make_password(signup_data['password']),
                email_verified=True
            )
            
            # Login user automatically
            login(request, user)
            
            user_data = UserSerializer(user).data
            user_data['is_staff'] = user.is_staff
            user_data['is_superuser'] = user.is_superuser
            
            return Response(
                {
                    'message': 'Account created successfully',
                    'user': user_data
                },
                status=status.HTTP_201_CREATED
            )
            
        except EmailOTP.DoesNotExist:
            return Response(
                {'error': 'Invalid OTP or email'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def resend_otp(request):
    """Resend OTP to email"""
    try:
        email = request.data.get('email', '').strip()
        
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Find existing OTP record with signup data
        email_otp = EmailOTP.objects.filter(email=email, is_verified=False).order_by('-created_at').first()
        
        if not email_otp or not email_otp.signup_data:
            return Response(
                {'error': 'No registration found for this email. Please start the registration process again.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate new OTP
        otp = EmailOTP.generate_otp()
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Update existing OTP or create new one
        email_otp.otp = otp
        email_otp.expires_at = expires_at
        email_otp.is_verified = False
        email_otp.created_at = timezone.now()
        email_otp.save()
        
        # Send OTP email
        subject = 'IFLA - Email Verification OTP'
        message = f'''
Hello,

Thank you for registering with IFLA!

Your verification code is: {otp}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
IFLA Team
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ifla.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email sending failed: {str(e)}")
            if settings.DEBUG:
                print(f"OTP for {email}: {otp}")
        
        return Response(
            {
                'message': 'OTP resent to your email. Please check your inbox.',
                'email': email
            },
            status=status.HTTP_200_OK
        )
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """User login endpoint"""
    try:
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            username_or_email = serializer.validated_data['username_or_email']
            password = serializer.validated_data['password']
            
            # Try to authenticate with email first (since USERNAME_FIELD is email)
            user = authenticate(request, username=username_or_email, password=password)
            
            # If authentication failed, try with username
            if user is None:
                # Check if it might be a username instead
                try:
                    user_obj = User.objects.get(username=username_or_email)
                    user = authenticate(request, username=user_obj.email, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                user_data = UserSerializer(user).data
                user_data['is_staff'] = user.is_staff
                user_data['is_superuser'] = user.is_superuser
                return Response(
                    {
                        'message': 'Login successful',
                        'user': user_data
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Invalid email or password'},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response(
            {'error': f'An error occurred: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def logout_view(request):
    """User logout endpoint"""
    logout(request)
    return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)


from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect

@require_http_methods(["GET", "POST"])
def logout_redirect(request):
    """Logout and redirect to home"""
    logout(request)
    return redirect('index')


@api_view(['GET'])
def user_profile(request):
    """Get current user profile"""
    if request.user.is_authenticated:
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
    return Response(
        {'error': 'Not authenticated'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def google_oauth_login(request):
    """Initiate Google OAuth login flow"""
    if not settings.GOOGLE_OAUTH2_CLIENT_ID:
        return Response(
            {'error': 'Google OAuth is not configured. Please set GOOGLE_OAUTH2_CLIENT_ID in settings.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    
    # Build Google OAuth URL
    redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
    scope = 'openid email profile'
    google_auth_url = (
        f'https://accounts.google.com/o/oauth2/v2/auth?'
        f'client_id={settings.GOOGLE_OAUTH2_CLIENT_ID}&'
        f'redirect_uri={redirect_uri}&'
        f'response_type=code&'
        f'scope={scope}&'
        f'access_type=online&'
        f'prompt=consent'
    )
    
    return Response(
        {'auth_url': google_auth_url},
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
@permission_classes([AllowAny])
def google_oauth_callback(request):
    """Handle Google OAuth callback"""
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    if error:
        # User denied access or other error
        return redirect(f'/auth/?error={error}&message=Google authentication was cancelled')
    
    if not code:
        return redirect('/auth/?error=no_code&message=No authorization code received')
    
    if not settings.GOOGLE_OAUTH2_CLIENT_ID or not settings.GOOGLE_OAUTH2_CLIENT_SECRET:
        return redirect('/auth/?error=config&message=Google OAuth is not properly configured')
    
    try:
        # Exchange authorization code for access token
        token_url = 'https://oauth2.googleapis.com/token'
        token_data = {
            'code': code,
            'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
            'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
            'redirect_uri': settings.GOOGLE_OAUTH2_REDIRECT_URI,
            'grant_type': 'authorization_code',
        }
        
        token_response = requests.post(token_url, data=token_data)
        token_response.raise_for_status()
        token_json = token_response.json()
        access_token = token_json.get('access_token')
        
        if not access_token:
            return redirect('/auth/?error=token&message=Failed to get access token')
        
        # Get user info from Google
        user_info_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
        headers = {'Authorization': f'Bearer {access_token}'}
        user_info_response = requests.get(user_info_url, headers=headers)
        user_info_response.raise_for_status()
        user_info = user_info_response.json()
        
        google_id = user_info.get('id')
        email = user_info.get('email')
        first_name = user_info.get('given_name', '')
        last_name = user_info.get('family_name', '')
        picture = user_info.get('picture', '')
        verified_email = user_info.get('verified_email', False)
        
        if not email:
            return redirect('/auth/?error=email&message=Email not provided by Google')
        
        # Check if user exists with this Google ID
        user = None
        if google_id:
            try:
                user = User.objects.get(google_id=google_id)
            except User.DoesNotExist:
                pass
        
        # If not found by Google ID, check by email
        if not user:
            try:
                user = User.objects.get(email=email)
                # Link Google account to existing user
                if not user.google_id:
                    user.google_id = google_id
                    user.save()
            except User.DoesNotExist:
                # Create new user
                username = email.split('@')[0]
                # Ensure username is unique
                base_username = username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                user = User.objects.create(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                    google_id=google_id,
                    email_verified=verified_email,
                    is_student=True
                )
        
        # Log the user in
        login(request, user)
        
        # Redirect based on user type
        if user.is_staff or user.is_superuser:
            return redirect('/api/courses/admin/dashboard/')
        else:
            return redirect('/dashboard/')
            
    except requests.exceptions.RequestException as e:
        return redirect(f'/auth/?error=network&message=Error connecting to Google: {str(e)}')
    except Exception as e:
        import traceback
        traceback.print_exc()
        return redirect(f'/auth/?error=server&message=Server error: {str(e)}')


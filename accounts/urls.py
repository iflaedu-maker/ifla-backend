from django.urls import path
from . import views

urlpatterns = [
    path('send-otp/', views.send_otp, name='send_otp'),
    path('verify-otp/', views.verify_otp_and_signup, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('signup/', views.verify_otp_and_signup, name='signup'),  # Keep for backward compatibility
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.user_profile, name='profile'),
    path('logout-redirect/', views.logout_redirect, name='logout_redirect'),
    
    # Google OAuth
    path('google/', views.google_oauth_login, name='google_oauth_login'),
    path('google/callback/', views.google_oauth_callback, name='google_oauth_callback'),
]


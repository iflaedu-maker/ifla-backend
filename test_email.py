"""
Quick email test script for production
Run this to test your email configuration:
    python test_email.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ifla_backend.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings

def test_email():
    """Test email sending configuration"""
    
    print("=" * 50)
    print("Email Configuration Test")
    print("=" * 50)
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"Email Backend: {settings.EMAIL_BACKEND}")
    print(f"Email Host: {getattr(settings, 'EMAIL_HOST', 'N/A')}")
    print(f"Email Port: {getattr(settings, 'EMAIL_PORT', 'N/A')}")
    print(f"From Email: {settings.DEFAULT_FROM_EMAIL}")
    print("=" * 50)
    
    # Get test email from user or use default
    test_email = input("\nEnter your test email address (or press Enter to skip): ").strip()
    
    if not test_email:
        print("❌ No email provided. Skipping test.")
        return
    
    if '@' not in test_email:
        print("❌ Invalid email address.")
        return
    
    print(f"\nSending test email to {test_email}...")
    
    try:
        send_mail(
            subject='IFLA - Email Test',
            message='This is a test email from IFLA. If you received this, your email configuration is working correctly!',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[test_email],
            fail_silently=False,
        )
        print("✅ Email sent successfully!")
        print(f"📧 Check your inbox at {test_email}")
        
        if settings.EMAIL_BACKEND == 'django.core.mail.backends.console.EmailBackend':
            print("\n⚠️  NOTE: You're using console backend (development mode).")
            print("   The email was printed above, not actually sent.")
            print("   Set ENVIRONMENT=production to send real emails.")
        else:
            print("\n✅ Real email was sent via SMTP!")
            
    except Exception as e:
        print(f"\n❌ Error sending email: {e}")
        print("\nTroubleshooting tips:")
        print("1. Check your EMAIL_HOST and EMAIL_PORT settings")
        print("2. Verify EMAIL_HOST_USER and EMAIL_HOST_PASSWORD")
        print("3. Ensure ENVIRONMENT=production is set")
        print("4. Check firewall/network settings")
        print("5. Review EMAIL_PRODUCTION_SETUP.md for detailed guide")

if __name__ == '__main__':
    test_email()


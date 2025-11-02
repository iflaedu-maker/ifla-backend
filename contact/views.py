from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage
from .serializers import ContactMessageSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def submit_contact(request):
    """Submit contact form"""
    serializer = ContactMessageSerializer(data=request.data)
    
    if serializer.is_valid():
        message = serializer.save()
        
        # Send email notification (if email is configured)
        try:
            send_mail(
                subject=f'New Contact Form Submission from {message.name}',
                message=f'''
You have received a new message from your IFLA website contact form:

From: {message.name}
Email: {message.email}
Language Interested In: {message.language or "Not specified"}

Message:
{message.message}

---
This email was sent from your IFLA website contact form.
                ''',
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@ifla.com',
                recipient_list=[settings.EMAIL_HOST_USER] if hasattr(settings, 'EMAIL_HOST_USER') and settings.EMAIL_HOST_USER else ['admin@ifla.com'],
                fail_silently=True,
            )
        except Exception as e:
            # Log error but don't fail the request
            print(f"Error sending email: {e}")
        
        return Response(
            {
                'message': 'Your message has been sent successfully. We\'ll get back to you soon!',
                'data': ContactMessageSerializer(message).data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
URL configuration for ifla_backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from courses.views import dashboard, enrollment_form, payment_portal, languages_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('accounts.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/contact/', include('contact.urls')),
    
    # Serve HTML pages
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('languages/', languages_page, name='languages'),
    path('languages.html', languages_page, name='languages_html'),
    path('auth/', TemplateView.as_view(template_name='auth.html'), name='auth'),
    path('auth.html', TemplateView.as_view(template_name='auth.html'), name='auth_html'),
    path('dashboard/', dashboard, name='dashboard'),
    path('enrollment/', enrollment_form, name='enrollment-form'),
    path('payment/', payment_portal, name='payment-portal'),
    
    # Admin UI routes (accessible at /api/courses/admin/*)
    # Django admin is at /admin/
]

# Serve static and media files in development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Serve static files from STATICFILES_DIRS
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()


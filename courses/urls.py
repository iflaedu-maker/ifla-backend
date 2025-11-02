from django.urls import path
from . import views
from . import admin_views

urlpatterns = [
    path('', views.language_list, name='language-list'),
    path('<int:pk>/', views.language_detail, name='language-detail'),
    path('<int:language_id>/levels/', views.course_levels_by_language, name='course-levels'),
    path('enroll/', views.enroll, name='enroll'),
    path('my-enrollments/', views.my_enrollments, name='my-enrollments'),
    path('enrollment-form/', views.enrollment_form, name='enrollment-form'),
    path('payment/', views.payment_portal, name='payment-portal'),
    path('payment/create-order/', views.create_payment_order, name='create-payment-order'),
    path('payment/webhook/', views.payment_webhook, name='payment-webhook'),
    path('payment/success/', views.payment_success, name='payment-success'),
    path('certificate/<int:certificate_id>/download/', views.download_certificate, name='download-certificate'),
    
    # Admin routes
    path('admin/dashboard/', admin_views.admin_dashboard, name='admin-dashboard'),
    path('admin/applications/', admin_views.admin_applications, name='admin-applications'),
    path('admin/applications/<int:application_id>/', admin_views.admin_application_detail, name='admin-application-detail'),
    path('admin/applications/<int:application_id>/update-status/', admin_views.admin_update_application_status, name='admin-update-application-status'),
    path('admin/enrollments/', admin_views.admin_enrollments, name='admin-enrollments'),
    path('admin/enrollments/<int:enrollment_id>/update/', admin_views.admin_update_enrollment, name='admin-update-enrollment'),
    path('admin/courses/', admin_views.admin_courses, name='admin-courses'),
    path('admin/certificates/', admin_views.admin_certificates, name='admin-certificates'),
    path('admin/certificates/<int:enrollment_id>/approve/', admin_views.admin_approve_certificate, name='admin-approve-certificate'),
    path('admin/analytics/', admin_views.admin_analytics, name='admin-analytics'),
    path('admin/users/', admin_views.admin_users, name='admin-users'),
    path('admin/users/<int:user_id>/', admin_views.admin_user_detail, name='admin-user-detail'),
    path('admin/users/add/', admin_views.admin_add_user, name='admin-add-user'),
    path('admin/users/<int:user_id>/delete/', admin_views.admin_delete_user, name='admin-delete-user'),
    path('admin/users/<int:user_id>/toggle-status/', admin_views.admin_toggle_user_status, name='admin-toggle-user-status'),
    
    # Course Management routes
    path('admin/languages/add/', admin_views.admin_add_language, name='admin-add-language'),
    path('admin/languages/<int:language_id>/update/', admin_views.admin_update_language, name='admin-update-language'),
    path('admin/languages/<int:language_id>/delete/', admin_views.admin_delete_language, name='admin-delete-language'),
    path('admin/levels/add/', admin_views.admin_add_level, name='admin-add-level'),
    path('admin/levels/<int:level_id>/update/', admin_views.admin_update_level, name='admin-update-level'),
    path('admin/levels/<int:level_id>/delete/', admin_views.admin_delete_level, name='admin-delete-level'),
    
    # API endpoints for fetching data
    path('admin/api/languages/<int:language_id>/', admin_views.admin_get_language, name='admin-get-language'),
    path('admin/api/levels/<int:level_id>/', admin_views.admin_get_level, name='admin-get-level'),
]


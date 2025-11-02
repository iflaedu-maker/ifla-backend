"""
Management command to delete all users and their data except admin users.

Usage:
    python manage.py delete_non_admin_users
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from accounts.models import User, EmailOTP
from courses.models import Certificate


class Command(BaseCommand):
    help = 'Delete all users and their data except admin users (users with is_superuser=True)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Actually perform the deletion (without this flag, it will only show what would be deleted)',
        )

    def handle(self, *args, **options):
        # Find all admin users (users with is_superuser=True)
        admin_users = User.objects.filter(is_superuser=True)
        admin_count = admin_users.count()
        
        # Find all non-admin users
        non_admin_users = User.objects.exclude(is_superuser=True)
        non_admin_count = non_admin_users.count()
        
        if admin_count == 0:
            self.stdout.write(
                self.style.WARNING('No admin users found! Please ensure you have at least one superuser.')
            )
            return
        
        self.stdout.write(self.style.SUCCESS(f'\nFound {admin_count} admin user(s):'))
        for admin in admin_users:
            self.stdout.write(f'  - {admin.username} ({admin.email})')
        
        self.stdout.write(self.style.WARNING(f'\nFound {non_admin_count} non-admin user(s) to delete:'))
        
        if non_admin_count == 0:
            self.stdout.write(self.style.SUCCESS('No non-admin users to delete.'))
            return
        
        # Show what will be deleted
        for user in non_admin_users[:10]:  # Show first 10
            self.stdout.write(f'  - {user.username} ({user.email})')
        if non_admin_count > 10:
            self.stdout.write(f'  ... and {non_admin_count - 10} more users')
        
        # Count related data
        total_enrollments = sum(user.enrollments.count() for user in non_admin_users)
        total_applications = sum(user.enrollment_applications.count() for user in non_admin_users)
        
        # Count EmailOTP records for non-admin users
        non_admin_emails = [user.email for user in non_admin_users]
        email_otp_count = EmailOTP.objects.filter(email__in=non_admin_emails).count()
        
        # Count certificates that reference non-admin users as approver
        certificate_count = Certificate.objects.filter(approved_by__in=non_admin_users).count()
        
        self.stdout.write(self.style.WARNING('\nRelated data to be deleted:'))
        self.stdout.write(f'  - {total_enrollments} enrollment(s)')
        self.stdout.write(f'  - {total_applications} enrollment application(s)')
        self.stdout.write(f'  - {email_otp_count} EmailOTP record(s)')
        self.stdout.write(f'  - Certificates and invoices (cascaded from enrollments)')
        self.stdout.write(f'  - {certificate_count} certificate(s) with non-admin approvers')
        
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    '\nThis is a DRY RUN. No data was deleted.\n'
                    'Run with --confirm to actually delete the data.'
                )
            )
            return
        
        # Confirm deletion
        self.stdout.write(self.style.ERROR('\n=== DELETION CONFIRMED ==='))
        
        with transaction.atomic():
            # Delete EmailOTP records for non-admin users
            deleted_otps = EmailOTP.objects.filter(email__in=non_admin_emails).delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_otps[0]} EmailOTP record(s)'))
            
            # Set approved_by to NULL for certificates approved by non-admin users
            updated_certificates = Certificate.objects.filter(
                approved_by__in=non_admin_users
            ).update(approved_by=None)
            if updated_certificates > 0:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Set approved_by to NULL for {updated_certificates} certificate(s)'
                    )
                )
            
            # Delete non-admin users (this will cascade delete enrollments, applications, invoices, etc.)
            deleted_users = non_admin_users.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted {deleted_users[0]} user(s) and all related data'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Deletion completed successfully!'))
        self.stdout.write(f'Remaining users: {User.objects.count()} (all admin users)')


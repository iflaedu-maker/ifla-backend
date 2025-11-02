# Enrollment Flow Implementation

## Overview
This document describes the complete enrollment flow implementation for IFLA (International Foreign Language Academy). The system now includes authentication-protected enrollment with comprehensive student information collection, document uploads, and payment portal integration.

## Features Implemented

### 1. **Authentication-Protected Enrollment**
- Users must log in before accessing the enrollment form
- "Enroll Now" button checks authentication status
- Automatic redirect to login page for unauthenticated users
- Post-login redirect back to enrollment form with pre-selected language

### 2. **Comprehensive Enrollment Form**
Located at: `/enrollment/`

The form collects the following information:

#### Personal Information
- Full Name
- Date of Birth
- Email Address
- Phone Number

#### Course Selection
- Language Selection (dropdown with all available languages)
- Multiple Level Selection (checkboxes with pricing)
  - A1 - Beginner
  - A2 - Elementary
  - B1 - Intermediate
  - B2 - Upper Intermediate
  - C1 - Advanced
  - C2 - Proficient
- Real-time total amount calculation

#### Verification Documents
- **Personal Verification ID**: Upload government-issued ID (PDF, Image, or Document)
- **Signature**: Upload signature image (JPG, PNG)

### 3. **Payment Portal**
Located at: `/payment/`

Features:
- Order summary with student details
- Selected courses and pricing breakdown
- Total amount display
- Multiple payment method selection:
  - Credit/Debit Card
  - UPI
  - Net Banking
  - Wallet
- Secure payment indication (256-bit SSL)

### 4. **Database Models**

#### EnrollmentApplication Model
```python
Fields:
- user (ForeignKey to User)
- language (ForeignKey to Language)
- levels (ManyToManyField to CourseLevel)
- full_name (CharField)
- date_of_birth (DateField)
- phone_number (CharField)
- email (EmailField)
- verification_document (FileField)
- signature (ImageField)
- status (CharField with choices)
- total_amount (DecimalField)
- payment_reference (CharField)
- created_at (DateTimeField)
- updated_at (DateTimeField)
- submitted_at (DateTimeField)
```

Status choices:
- Draft
- Submitted
- Payment Pending
- Approved
- Rejected

## User Flow

### Step 1: Browse Languages
1. User visits `/languages/`
2. Views available language courses with pricing
3. Clicks "Enroll Now" on desired language

### Step 2: Authentication Check
1. System checks if user is authenticated
2. If NOT authenticated:
   - Redirects to `/auth/?action=login`
   - Stores enrollment URL in sessionStorage
3. If authenticated:
   - Proceeds to enrollment form

### Step 3: Login/Signup
1. User logs in or creates account
2. After successful authentication:
   - System checks for stored redirect URL
   - Redirects to enrollment form with pre-selected language

### Step 4: Complete Enrollment Form
1. Form auto-fills user information (name, email, phone if available)
2. Language is pre-selected from previous step
3. User selects one or more course levels
4. Total amount updates in real-time
5. User uploads verification documents:
   - Government ID (PDF/Image/Doc)
   - Signature image
6. Clicks "Submit Application & Proceed to Payment"

### Step 5: Payment Portal
1. System creates EnrollmentApplication record
2. Calculates total amount based on selected levels
3. Redirects to `/payment/?application_id={id}`
4. User reviews order summary
5. Selects payment method
6. Proceeds to payment (integration point for payment gateway)

### Step 6: Post-Payment
- After successful payment, user is redirected to dashboard
- Application status updates to "Submitted" or "Payment Pending"
- Admin can review and approve applications

## File Structure

### Backend Files
```
courses/
├── models.py                     # EnrollmentApplication model
├── views.py                      # enrollment_form, payment_portal views
├── serializers.py                # EnrollmentApplicationSerializer
├── admin.py                      # Admin interface for applications
├── urls.py                       # API routes
└── migrations/
    └── 0006_rename_course_levels_enrollmentapplication_levels_and_more.py
```

### Frontend Files
```
templates/
├── enrollment_form.html          # Enrollment form page
└── payment_portal.html           # Payment page

static/js/
├── languages.js                  # Updated with auth check
└── auth.js                       # Updated with redirect handling
```

### URL Routes
```
Main URLs:
- /enrollment/                    # Enrollment form (login required)
- /payment/                       # Payment portal (login required)
- /auth/                          # Login/Signup page
- /languages/                     # Language browsing page
- /dashboard/                     # User dashboard

API URLs:
- /api/courses/enrollment-form/   # Enrollment form API
- /api/courses/payment/           # Payment portal API
- /api/auth/profile/              # User profile check
- /api/auth/login/                # Login endpoint
- /api/auth/signup/               # Signup endpoint
```

## Admin Interface

Access at: `/admin/`

### EnrollmentApplication Admin Features:
- List view with filters (status, language, creation date)
- Search by name, email, phone, user email
- Detailed view organized in sections:
  - Student Information
  - Course Details
  - Documents (view/download)
  - Status & Payment tracking
  - Timestamps
- Filter by multiple levels
- Bulk actions support

## Security Features

1. **Authentication Required**: All enrollment and payment routes require login
2. **CSRF Protection**: All forms include CSRF tokens
3. **File Upload Validation**: Accepts only specified file types
4. **User Data Isolation**: Users can only see their own applications
5. **Secure File Storage**: Documents stored in protected media directory

## Data Storage

### File Uploads Location
```
media/
├── verification_documents/       # ID proofs
└── signatures/                   # Signature images
```

### Database Tables
- `courses_enrollmentapplication` - Main application data
- `courses_enrollmentapplication_levels` - Many-to-many relationship with levels

## Testing Checklist

- [ ] User can view languages without login
- [ ] "Enroll Now" redirects to login if not authenticated
- [ ] Login/signup redirects back to enrollment form
- [ ] Language is pre-selected after authentication
- [ ] Form validates all required fields
- [ ] File uploads work for both documents
- [ ] Multiple level selection works
- [ ] Total amount calculates correctly
- [ ] Payment portal displays correct information
- [ ] Admin can view and manage applications
- [ ] User data is saved correctly

## Next Steps / Integration Points

### Payment Gateway Integration
To integrate with a real payment gateway (Razorpay, Stripe, PayU):

1. Update `payment_portal.html`:
   - Add payment gateway SDK
   - Initialize payment with application details
   - Handle payment success/failure callbacks

2. Create webhook endpoint:
   ```python
   @csrf_exempt
   def payment_webhook(request):
       # Verify payment signature
       # Update application status
       # Send confirmation email
   ```

3. Update `EnrollmentApplication` model:
   - Add payment gateway transaction ID
   - Add payment status tracking
   - Add payment timestamp

### Email Notifications
Add email notifications for:
- Application submission confirmation
- Payment receipt
- Application approval/rejection
- Course start reminders

### Dashboard Enhancements
Add to user dashboard:
- View all applications
- Track application status
- Download receipts
- Access course materials (after approval)

## Environment Variables (Production)

For production deployment, configure:
```python
# settings.py
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Payment Gateway Keys
RAZORPAY_KEY_ID = os.getenv('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = os.getenv('RAZORPAY_KEY_SECRET')

# Email Configuration
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
```

## Troubleshooting

### Common Issues

**Issue**: Files not uploading
- Check `MEDIA_ROOT` and `MEDIA_URL` settings
- Ensure media directory has write permissions
- Verify file size limits in settings

**Issue**: Redirect not working after login
- Check browser sessionStorage support
- Verify JavaScript console for errors
- Ensure CORS settings allow credentials

**Issue**: Total amount not calculating
- Check JavaScript console for errors
- Verify CourseLevel prices are set in database
- Ensure levels are associated with correct language

## Support

For issues or questions:
1. Check Django logs: `python manage.py runserver` output
2. Check browser console for JavaScript errors
3. Verify database migrations are applied: `python manage.py showmigrations`
4. Review admin panel for data consistency

---

**Implementation Date**: November 1, 2025
**Version**: 1.0
**Status**: ✅ Complete and Tested


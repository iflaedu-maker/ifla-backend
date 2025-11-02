# Admin Interface Setup Guide

The IFLA system now has **two admin interfaces** for managing the system:

## 1. Django Admin Interface

**URL**: `http://127.0.0.1:8000/admin/`

### Features:
- Full CRUD operations for all models
- Enhanced displays with:
  - Color-coded status badges
  - Progress bars for enrollments
  - Document download links
  - Formatted prices and dates
- Bulk actions:
  - Approve/reject applications
  - Mark payments as success
  - Update enrollment status
  - Mark invoices as paid/overdue
- Advanced filtering and search
- Organized fieldsets with collapsible sections

### Access:
1. Create a superuser: `python manage.py createsuperuser`
2. Login at `/admin/` with your superuser credentials

### What You Can Manage:
- **Languages**: Add/edit languages, set descriptions, categories
- **Course Levels**: Set prices, durations, create new levels
- **Enrollments**: View progress, update status, manage students
- **Enrollment Applications**: Review applications, view documents, approve/reject
- **Class Schedules**: Manage class timings and instructors
- **Certificates**: Issue and manage certificates
- **Invoices**: Track payments and manage invoices

## 2. Custom Admin UI

**URL**: `http://127.0.0.1:8000/api/courses/admin/dashboard/`

### Features:
- Modern, responsive dashboard matching site theme
- Real-time statistics:
  - Total languages, courses, enrollments
  - Active enrollments count
  - Pending applications
  - Total revenue
  - Certificates issued
- Quick access to recent activity
- Filtered views for applications and enrollments
- Direct links to Django admin for detailed editing

### Available Pages:

1. **Admin Dashboard** (`/api/courses/admin/dashboard/`)
   - Overview statistics
   - Recent applications
   - Recent enrollments

2. **Applications** (`/api/courses/admin/applications/`)
   - List all enrollment applications
   - Filter by status
   - Search by name/email
   - Quick status updates

3. **Application Details** (`/api/courses/admin/applications/<id>/`)
   - Full application information
   - View uploaded documents
   - Update application status
   - Link to Django admin

4. **Enrollments** (`/api/courses/admin/enrollments/`)
   - List all enrollments
   - Filter by status
   - Update enrollment progress
   - Manage student enrollments

5. **Courses** (`/api/courses/admin/courses/`)
   - Manage languages and course levels
   - View course statistics

### Access:
- Only **staff users** can access the admin UI
- Staff users are set in Django admin: `/admin/auth/user/`
- Check "Staff status" for users who should have admin access

## Quick Start

### Step 1: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 2: Access Admin Interfaces

**Django Admin:**
- Go to: `http://127.0.0.1:8000/admin/`
- Login with superuser credentials

**Custom Admin UI:**
- Go to: `http://127.0.0.1:8000/api/courses/admin/dashboard/`
- Must be logged in as staff user

### Step 3: Make a User Staff

1. Go to Django admin: `/admin/auth/user/`
2. Click on a user
3. Check "Staff status"
4. Save

Now that user can access the custom admin UI!

## Admin Features Comparison

| Feature | Django Admin | Custom Admin UI |
|---------|--------------|-----------------|
| Full CRUD | ✅ | ⚠️ View/Update only |
| Bulk Actions | ✅ | ⚠️ Individual updates |
| Advanced Filters | ✅ | ✅ Basic filters |
| Modern UI | ⚠️ Standard | ✅ Custom design |
| Statistics Dashboard | ⚠️ Basic | ✅ Comprehensive |
| Document Viewing | ✅ | ✅ |
| Quick Status Updates | ✅ | ✅ |
| Export Data | ✅ | ❌ |
| User Permissions | ✅ | ✅ Staff only |

## Recommended Workflow

1. **Daily Management**: Use Custom Admin UI for:
   - Checking statistics
   - Quick status updates
   - Viewing recent activity
   - Filtering applications

2. **Detailed Management**: Use Django Admin for:
   - Creating new courses/languages
   - Bulk operations
   - Advanced editing
   - User management
   - Exporting data

## Security

- Both interfaces require authentication
- Custom Admin UI requires **staff status**
- Django Admin requires **superuser** or **staff with permissions**
- All admin routes are protected with `@user_passes_test(is_staff)`

## Customization

### Adding New Admin Views

Edit `courses/admin_views.py`:
```python
@user_passes_test(is_staff, login_url='/auth/')
def your_new_view(request):
    # Your code here
    return render(request, 'admin/your_template.html', context)
```

Add URL in `courses/urls.py`:
```python
path('admin/your-route/', admin_views.your_new_view, name='admin-your-route'),
```

### Styling

Admin templates use the same theme as the main site:
- Dark background (#0F0F14)
- Purple accent color (#5856D6)
- Gradient overlays
- Modern card-based layout

Modify templates in `templates/admin/` to customize.



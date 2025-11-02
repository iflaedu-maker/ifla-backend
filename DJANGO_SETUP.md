# Django IFLA Backend Setup Guide

## Prerequisites

1. Python 3.8 or higher installed
2. pip (Python package manager)

## Installation Steps

### 1. Create Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 5. Collect Static Files

```bash
python manage.py collectstatic
```

### 6. Populate Initial Data (Optional)

```bash
python manage.py populate_languages
```

This will create sample language and course data.

### 7. Run Development Server

```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication
- `POST /api/auth/signup/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout
- `GET /api/auth/profile/` - Get user profile

### Courses
- `GET /api/courses/` - List all languages
- `GET /api/courses/<id>/` - Get language details
- `GET /api/courses/<id>/levels/` - Get course levels for a language
- `POST /api/courses/enroll/` - Enroll in a course
- `GET /api/courses/my-enrollments/` - Get user enrollments

### Contact
- `POST /api/contact/submit/` - Submit contact form

## Frontend Integration

The frontend JavaScript files have been updated to use these API endpoints. Make sure to:
1. Update API base URL in JavaScript files if needed
2. Ensure CORS is properly configured for your domain

## Admin Panel

Access the Django admin panel at: `http://127.0.0.1:8000/admin/`

Login with your superuser credentials to manage:
- Users
- Languages
- Course Levels
- Enrollments
- Contact Messages

## Production Deployment

For production:
1. Set `DEBUG = False` in settings.py
2. Update `SECRET_KEY` with a secure random key
3. Configure proper database (PostgreSQL recommended)
4. Set up proper email backend
5. Configure static files serving (use WhiteNoise or CDN)
6. Use environment variables for sensitive settings


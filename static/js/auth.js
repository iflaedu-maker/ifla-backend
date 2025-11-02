// Switch between Login and Signup forms
function switchToSignup() {
    document.getElementById('loginCard').style.display = 'none';
    document.getElementById('signupCard').style.display = 'block';
    
    // Animate the card
    const signupCard = document.getElementById('signupCard');
    signupCard.style.opacity = '0';
    signupCard.style.transform = 'translateY(20px)';
    setTimeout(() => {
        signupCard.style.transition = 'all 0.4s ease';
        signupCard.style.opacity = '1';
        signupCard.style.transform = 'translateY(0)';
    }, 10);
}

function switchToLogin() {
    document.getElementById('signupCard').style.display = 'none';
    document.getElementById('loginCard').style.display = 'block';
    
    // Animate the card
    const loginCard = document.getElementById('loginCard');
    loginCard.style.opacity = '0';
    loginCard.style.transform = 'translateY(20px)';
    setTimeout(() => {
        loginCard.style.transition = 'all 0.4s ease';
        loginCard.style.opacity = '1';
        loginCard.style.transform = 'translateY(0)';
    }, 10);
}

// Toggle password visibility
function togglePassword(inputId) {
    const input = document.getElementById(inputId);
    const button = input.nextElementSibling;
    
    if (input.type === 'password') {
        input.type = 'text';
        button.innerHTML = `
            <svg class="eye-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M14.12 14.12A7.5 7.5 0 0 1 5.88 5.88M1 10s3-6 9-6c1.5 0 2.87.35 4.12.94M19 10s-1.5 3-4.12 4.12M9 9l6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <line x1="1" y1="1" x2="19" y2="19" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
    } else {
        input.type = 'password';
        button.innerHTML = `
            <svg class="eye-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M1 10s3-6 9-6 9 6 9 6-3 6-9 6-9-6-9-6z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <circle cx="10" cy="10" r="3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
        `;
    }
}

// API Configuration
const API_BASE_URL = window.location.origin;

// Handle Login Form Submission
document.getElementById('loginForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const username_or_email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.querySelector('span').textContent;
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.querySelector('span').textContent = 'Logging in...';
    
    try {
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            showNotification('CSRF token missing. Please refresh the page.', 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
            return;
        }

         const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            credentials: 'include',
            body: JSON.stringify({ username_or_email, password })
        });
        
        let data;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const text = await response.text();
            console.error('Non-JSON response:', text);
            showNotification('Server error. Please try again later.', 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
            return;
        }
        
        if (response.ok) {
            showNotification('Login successful! Redirecting...', 'success');
            setTimeout(() => {
                // Check if there's a redirect URL stored
                const redirectUrl = sessionStorage.getItem('redirectAfterLogin');
                if (redirectUrl) {
                    sessionStorage.removeItem('redirectAfterLogin');
                    window.location.href = redirectUrl;
                } else {
                    // Check if user is staff/admin - redirect to admin dashboard
                    if (data.user && (data.user.is_staff || data.user.is_superuser)) {
                        window.location.href = '/api/courses/admin/dashboard/';
                    } else {
                        window.location.href = '/dashboard/';
                    }
                }
            }, 1500);
        } else {
            // Handle different error response formats
            let errorMessage = 'Login failed. Please check your credentials.';
            if (data.error) {
                errorMessage = data.error;
            } else if (data.email) {
                errorMessage = data.email[0] || errorMessage;
            } else if (data.password) {
                errorMessage = data.password[0] || errorMessage;
            } else if (data.non_field_errors) {
                errorMessage = data.non_field_errors[0] || errorMessage;
            }
            showNotification(errorMessage, 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
        }
    } catch (error) {
        console.error('Login error:', error);
        let errorMessage = 'An error occurred. Please try again.';
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMessage = 'Network error. Please check your internet connection.';
        } else if (error.message.includes('JSON')) {
            errorMessage = 'Server response error. Please try again.';
        }
        showNotification(errorMessage, 'error');
        submitBtn.disabled = false;
        submitBtn.querySelector('span').textContent = originalText;
    }
});

// Store signup email for OTP verification
let pendingSignupEmail = '';

// Handle Signup Form Submission
document.getElementById('signupForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('signupEmail').value;
    const username = document.getElementById('signupUsername')?.value || '';
    const password = document.getElementById('signupPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.querySelector('span').textContent;
    
    // Validate password match
    if (password !== confirmPassword) {
        showNotification('Passwords do not match!', 'error');
        return;
    }
    
    // Validate password strength (basic)
    if (password.length < 8) {
        showNotification('Password must be at least 8 characters long', 'error');
        return;
    }
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.querySelector('span').textContent = 'Sending verification code...';
    
    try {
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            showNotification('CSRF token missing. Please refresh the page.', 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
            return;
        }

        const signupData = { 
            email, 
            password, 
            first_name: firstName, 
            last_name: lastName 
        };
        
        // Only include username if it's provided
        if (username.trim()) {
            signupData.username = username.trim();
        }

        // Send OTP instead of creating account directly
        const response = await fetch(`${API_BASE_URL}/api/auth/send-otp/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            credentials: 'include',
            body: JSON.stringify(signupData)
        });
        
        let data;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const text = await response.text();
            console.error('Non-JSON response:', text);
            showNotification('Server error. Please try again later.', 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
            return;
        }
        
        if (response.ok) {
            // Store email for OTP verification
            pendingSignupEmail = email;
            
            // Show OTP verification form
            document.getElementById('signupCard').style.display = 'none';
            document.getElementById('otpCard').style.display = 'block';
            document.getElementById('otpEmailDisplay').textContent = email;
            document.getElementById('otpInput').focus();
            
            showNotification('Verification code sent to your email!', 'success');
        } else {
            // Handle different error response formats
            let errorMessage = 'Failed to send verification code. Please try again.';
            if (data.error) {
                errorMessage = data.error;
            } else if (data.email) {
                errorMessage = Array.isArray(data.email) ? data.email[0] : data.email;
            } else if (data.password) {
                errorMessage = Array.isArray(data.password) ? data.password[0] : data.password;
            } else if (data.first_name) {
                errorMessage = Array.isArray(data.first_name) ? data.first_name[0] : data.first_name;
            } else if (data.last_name) {
                errorMessage = Array.isArray(data.last_name) ? data.last_name[0] : data.last_name;
            } else if (data.non_field_errors) {
                errorMessage = Array.isArray(data.non_field_errors) ? data.non_field_errors[0] : data.non_field_errors;
            } else if (typeof data === 'object') {
                // Try to find first error message
                const firstError = Object.values(data).find(val => val);
                if (firstError) {
                    errorMessage = Array.isArray(firstError) ? firstError[0] : firstError;
                }
            }
            showNotification(errorMessage, 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
        }
    } catch (error) {
        console.error('Signup error:', error);
        let errorMessage = 'An error occurred. Please try again.';
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMessage = 'Network error. Please check your internet connection.';
        } else if (error.message.includes('JSON')) {
            errorMessage = 'Server response error. Please try again.';
        }
        showNotification(errorMessage, 'error');
        submitBtn.disabled = false;
        submitBtn.querySelector('span').textContent = originalText;
    }
});

// Handle OTP Form Submission
document.getElementById('otpForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const otp = document.getElementById('otpInput').value.trim();
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.querySelector('span').textContent;
    
    // Validate OTP format
    if (!otp || otp.length !== 6 || !/^\d{6}$/.test(otp)) {
        showNotification('Please enter a valid 6-digit code', 'error');
        return;
    }
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.querySelector('span').textContent = 'Verifying...';
    
    try {
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            showNotification('CSRF token missing. Please refresh the page.', 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
            return;
        }

        const response = await fetch(`${API_BASE_URL}/api/auth/verify-otp/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            credentials: 'include',
            body: JSON.stringify({
                email: pendingSignupEmail,
                otp: otp
            })
        });
        
        let data;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const text = await response.text();
            console.error('Non-JSON response:', text);
            showNotification('Server error. Please try again later.', 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
            return;
        }
        
        if (response.ok) {
            showNotification('Account created successfully! Redirecting...', 'success');
            setTimeout(() => {
                // Check if there's a redirect URL stored
                const redirectUrl = sessionStorage.getItem('redirectAfterLogin');
                if (redirectUrl) {
                    sessionStorage.removeItem('redirectAfterLogin');
                    window.location.href = redirectUrl;
                } else {
                    // Check if user is staff/admin - redirect to admin dashboard
                    if (data.user && (data.user.is_staff || data.user.is_superuser)) {
                        window.location.href = '/api/courses/admin/dashboard/';
                    } else {
                        window.location.href = '/dashboard/';
                    }
                }
            }, 1500);
        } else {
            let errorMessage = 'Verification failed. Please try again.';
            if (data.error) {
                errorMessage = data.error;
            }
            showNotification(errorMessage, 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
            // Clear OTP input on error
            document.getElementById('otpInput').value = '';
        }
    } catch (error) {
        console.error('OTP verification error:', error);
        let errorMessage = 'An error occurred. Please try again.';
        if (error.message.includes('Failed to fetch') || error.message.includes('NetworkError')) {
            errorMessage = 'Network error. Please check your internet connection.';
        } else if (error.message.includes('JSON')) {
            errorMessage = 'Server response error. Please try again.';
        }
        showNotification(errorMessage, 'error');
        submitBtn.disabled = false;
        submitBtn.querySelector('span').textContent = originalText;
    }
});

// Handle Resend OTP
document.getElementById('resendOtpBtn')?.addEventListener('click', async function(e) {
    e.preventDefault();
    
    if (!pendingSignupEmail) {
        showNotification('No email found. Please start registration again.', 'error');
        return;
    }
    
    const btn = this;
    const originalText = btn.textContent;
    
    btn.disabled = true;
    btn.textContent = 'Sending...';
    
    try {
        const csrfToken = getCsrfToken();
        if (!csrfToken) {
            showNotification('CSRF token missing. Please refresh the page.', 'error');
            btn.disabled = false;
            btn.textContent = originalText;
            return;
        }

        const response = await fetch(`${API_BASE_URL}/api/auth/resend-otp/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            credentials: 'include',
            body: JSON.stringify({
                email: pendingSignupEmail
            })
        });
        
        let data;
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
        } else {
            const text = await response.text();
            console.error('Non-JSON response:', text);
            showNotification('Server error. Please try again later.', 'error');
            btn.disabled = false;
            btn.textContent = originalText;
            return;
        }
        
        if (response.ok) {
            showNotification('Verification code resent! Please check your email.', 'success');
            // Clear OTP input
            document.getElementById('otpInput').value = '';
            document.getElementById('otpInput').focus();
        } else {
            let errorMessage = 'Failed to resend code. Please try again.';
            if (data && data.error) {
                errorMessage = data.error;
            }
            showNotification(errorMessage, 'error');
        }
        
        btn.disabled = false;
        btn.textContent = originalText;
    } catch (error) {
        console.error('Resend OTP error:', error);
        showNotification('An error occurred. Please try again.', 'error');
        btn.disabled = false;
        btn.textContent = originalText;
    }
});

// Allow only numeric input for OTP field
document.getElementById('otpInput')?.addEventListener('input', function(e) {
    this.value = this.value.replace(/[^0-9]/g, '');
});

// Helper function to reset signup form
function resetSignupForm() {
    document.getElementById('signupForm').reset();
    document.getElementById('otpForm').reset();
    pendingSignupEmail = '';
    document.getElementById('otpCard').style.display = 'none';
    document.getElementById('signupCard').style.display = 'block';
}

// Show notification
function showNotification(message, type) {
    // Remove any existing notifications
    const existingNotification = document.querySelector('.auth-notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = 'auth-notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 16px 24px;
        background: ${type === 'success' 
            ? 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)' 
            : 'linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%)'};
        color: white;
        border-radius: 12px;
        font-family: 'Montserrat', sans-serif;
        font-size: 14px;
        font-weight: 500;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
        z-index: 10000;
        opacity: 0;
        transform: translateX(400px);
        transition: all 0.3s ease-out;
        max-width: 350px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    `;
    
    document.body.appendChild(notification);
    
    // Trigger animation
    setTimeout(() => {
        notification.style.opacity = '1';
        notification.style.transform = 'translateX(0)';
    }, 10);
    
    // Remove notification after 5 seconds
    setTimeout(() => {
        notification.style.opacity = '0';
        notification.style.transform = 'translateX(400px)';
        setTimeout(() => notification.remove(), 300);
    }, 5000);
}

// Navbar scroll effect
const navbar = document.querySelector('.navbar');

function handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (navbar) {
        if (scrollTop > 50) {
            navbar.style.background = 'rgba(15, 15, 20, 0.8)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
        } else {
            navbar.style.background = 'transparent';
            navbar.style.backdropFilter = 'none';
            navbar.style.borderBottom = 'none';
        }
    }
}

window.addEventListener('scroll', handleScroll, { passive: true });

// Get CSRF Token helper function
function getCsrfToken() {
    // First try global variable (set by Django template)
    if (window.csrfToken) {
        return window.csrfToken;
    }
    
    // Try to get from hidden input field (most reliable in Django templates)
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    if (csrfInput && csrfInput.value) {
        return csrfInput.value;
    }
    
    // Try to get from meta tag if available
    const csrfMeta = document.querySelector('meta[name=csrf-token]');
    if (csrfMeta && csrfMeta.content) {
        return csrfMeta.content;
    }
    
    // Try to get from cookie
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const parts = cookie.trim().split('=');
        if (parts.length === 2) {
            const [name, value] = parts;
            if (name === 'csrftoken' && value) {
                return decodeURIComponent(value);
            }
            if (name === 'csrfmiddlewaretoken' && value) {
                return decodeURIComponent(value);
            }
        }
    }
    
    console.error('CSRF token not found. Available cookies:', document.cookie);
    console.error('Available inputs:', document.querySelectorAll('[name*=csrf]'));
    return '';
}

// Handle Google OAuth Login - Make it globally accessible
window.handleGoogleLogin = async function() {
    console.log('Google login button clicked');
    
    try {
        console.log('Fetching Google OAuth URL from:', `${API_BASE_URL}/api/auth/google/`);
        
        const response = await fetch(`${API_BASE_URL}/api/auth/google/`, {
            method: 'GET',
            credentials: 'include',
            headers: {
                'Accept': 'application/json',
            }
        });
        
        console.log('Response status:', response.status);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('Response data:', data);
        
        if (data.auth_url) {
            console.log('Redirecting to Google OAuth:', data.auth_url);
            // Redirect to Google OAuth immediately
            window.location.href = data.auth_url;
        } else {
            console.error('No auth_url in response:', data);
            showNotification(data.error || 'Failed to get Google OAuth URL', 'error');
        }
    } catch (error) {
        console.error('Google login error:', error);
        showNotification('An error occurred. Please try again. ' + error.message, 'error');
    }
};

// Function to attach Google login handlers
function attachGoogleHandlers() {
    const googleButtons = document.querySelectorAll('.google-btn');
    console.log('Found Google buttons:', googleButtons.length);
    
    googleButtons.forEach((button, index) => {
        // Remove existing listeners to avoid duplicates
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
        
        // Add click handler
        newButton.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            console.log('Google button clicked (button', index + 1, ')');
            handleGoogleLogin();
        });
        
        console.log('Attached handler to Google button', index + 1);
    });
}

// Attach Google login handlers when page loads
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('action') === 'signup') {
        switchToSignup();
    }
    
    // Check for OAuth errors in URL
    const error = urlParams.get('error');
    const message = urlParams.get('message');
    if (error) {
        showNotification(message || 'Authentication failed. Please try again.', 'error');
        // Clean up URL
        window.history.replaceState({}, document.title, window.location.pathname);
    }
    
    // Attach Google login handlers
    attachGoogleHandlers();
    
    // Also attach handlers after form switches (in case buttons are dynamically shown)
    const originalSwitchToSignup = window.switchToSignup;
    window.switchToSignup = function() {
        if (originalSwitchToSignup) originalSwitchToSignup();
        setTimeout(attachGoogleHandlers, 100);
    };
    
    const originalSwitchToLogin = window.switchToLogin;
    window.switchToLogin = function() {
        if (originalSwitchToLogin) originalSwitchToLogin();
        setTimeout(attachGoogleHandlers, 100);
    };
});

console.log('✨ Auth page loaded successfully!');


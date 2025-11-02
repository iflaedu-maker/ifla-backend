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
    
    const email = document.getElementById('loginEmail').value;
    const password = document.getElementById('loginPassword').value;
    const submitBtn = this.querySelector('button[type="submit"]');
    const originalText = submitBtn.querySelector('span').textContent;
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.querySelector('span').textContent = 'Logging in...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/login/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            credentials: 'include',
            body: JSON.stringify({ email, password })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Login successful! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        } else {
            showNotification(data.error || 'Login failed. Please check your credentials.', 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
        }
    } catch (error) {
        console.error('Login error:', error);
        showNotification('An error occurred. Please try again.', 'error');
        submitBtn.disabled = false;
        submitBtn.querySelector('span').textContent = originalText;
    }
});

// Handle Signup Form Submission
document.getElementById('signupForm')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const firstName = document.getElementById('firstName').value;
    const lastName = document.getElementById('lastName').value;
    const email = document.getElementById('signupEmail').value;
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
    submitBtn.querySelector('span').textContent = 'Creating account...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/signup/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            credentials: 'include',
            body: JSON.stringify({ 
                email, 
                password, 
                first_name: firstName, 
                last_name: lastName 
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('Account created successfully! Redirecting...', 'success');
            setTimeout(() => {
                window.location.href = '/';
            }, 1500);
        } else {
            showNotification(data.error || 'Signup failed. Please try again.', 'error');
            submitBtn.disabled = false;
            submitBtn.querySelector('span').textContent = originalText;
        }
    } catch (error) {
        console.error('Signup error:', error);
        showNotification('An error occurred. Please try again.', 'error');
        submitBtn.disabled = false;
        submitBtn.querySelector('span').textContent = originalText;
    }
});

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
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// Check URL for signup parameter
document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('action') === 'signup') {
        switchToSignup();
    }
});

console.log('✨ Auth page loaded successfully!');


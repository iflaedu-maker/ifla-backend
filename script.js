// Performance optimized animations

// Throttle function for better performance
function throttle(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        if (!timeout) {
            timeout = setTimeout(() => {
                func(...args);
                timeout = null;
            }, wait);
        }
    };
}

// Intersection Observer for fade-in animations (most efficient)
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            fadeObserver.unobserve(entry.target); // Stop observing once visible
        }
    });
}, observerOptions);

// Subtle parallax effect on scroll (optimized with throttle)
const handleParallax = throttle(() => {
    const scrolled = window.pageYOffset;
    
    // Only apply parallax in hero section for better performance
    if (scrolled < window.innerHeight) {
        // Hero background parallax (subtle)
        const heroBackground = document.querySelector('.hero-background-gradient');
        if (heroBackground) {
            heroBackground.style.transform = `translateY(${scrolled * 0.3}px)`;
        }
        
        // Hero content parallax (very subtle)
        const heroContent = document.querySelector('.hero-content-section');
        if (heroContent) {
            heroContent.style.transform = `translateY(${scrolled * 0.1}px)`;
        }
        
        // Hero visual parallax (opposite direction, subtle)
        const heroVisual = document.querySelector('.hero-visual-section');
        if (heroVisual) {
            heroVisual.style.transform = `translateY(${scrolled * -0.05}px)`;
        }
    }
}, 50); // Throttle to 50ms for smooth but performant parallax

window.addEventListener('scroll', handleParallax, { passive: true });

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
    // Fade in stat cards
    const cards = document.querySelectorAll('.stat-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = `opacity 0.6s ease ${index * 0.1}s, transform 0.6s ease ${index * 0.1}s`;
        fadeObserver.observe(card);
    });
    
    // Fade in stats header
    const statsTitle = document.querySelector('.stats-title');
    const statsSubtitle = document.querySelector('.stats-subtitle');
    
    if (statsTitle) {
        statsTitle.style.opacity = '0';
        statsTitle.style.transform = 'translateY(20px)';
        statsTitle.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeObserver.observe(statsTitle);
    }
    
    if (statsSubtitle) {
        statsSubtitle.style.opacity = '0';
        statsSubtitle.style.transform = 'translateY(20px)';
        statsSubtitle.style.transition = 'opacity 0.6s ease 0.1s, transform 0.6s ease 0.1s';
        fadeObserver.observe(statsSubtitle);
    }
    
    // Fade in languages section
    const languagesHeader = document.querySelector('.languages-header');
    const languagesScroller = document.querySelector('.languages-scroller');
    
    if (languagesHeader) {
        languagesHeader.style.opacity = '0';
        languagesHeader.style.transform = 'translateY(20px)';
        languagesHeader.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        fadeObserver.observe(languagesHeader);
    }
    
    if (languagesScroller) {
        languagesScroller.style.opacity = '0';
        languagesScroller.style.transform = 'translateY(20px)';
        languagesScroller.style.transition = 'opacity 0.6s ease 0.1s, transform 0.6s ease 0.1s';
        fadeObserver.observe(languagesScroller);
    }
});

// Navbar background on scroll (throttled)
const navbar = document.querySelector('.navbar');
let lastScrollTop = 0;

const handleScroll = throttle(() => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (navbar) {
        if (scrollTop > 100) {
            navbar.style.background = 'rgba(15, 15, 20, 0.8)';
            navbar.style.backdropFilter = 'blur(20px)';
            navbar.style.borderBottom = '1px solid rgba(255, 255, 255, 0.1)';
        } else {
            navbar.style.background = 'transparent';
            navbar.style.backdropFilter = 'none';
            navbar.style.borderBottom = 'none';
        }
    }
    
    lastScrollTop = scrollTop;
}, 100); // Throttle to 100ms

window.addEventListener('scroll', handleScroll, { passive: true });

// Video autoplay when visible
const videoCard = document.querySelector('.card-video');
if (videoCard) {
    const videoObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const video = entry.target.querySelector('.card-video-element');
                if (video && video.paused) {
                    video.play().catch(() => {
                        // Autoplay might be blocked, that's okay
                    });
                }
                videoObserver.unobserve(entry.target); // Only play once
            }
        });
    }, { threshold: 0.3 });
    
    videoObserver.observe(videoCard);
}

// Simple counter animation (optimized)
const animateCounter = (element, target) => {
    const duration = 1500; // 1.5 seconds
    const start = 0;
    const startTime = performance.now();
    const suffix = element.textContent.includes('+') ? '+' : (element.textContent.includes('%') ? '%' : '');
    
    function update(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function for smooth animation
        const easeOutQuad = progress * (2 - progress);
        const current = Math.floor(start + (target - start) * easeOutQuad);
        
        element.textContent = current + suffix;
        
        if (progress < 1) {
            requestAnimationFrame(update);
        }
    }
    
    requestAnimationFrame(update);
};

// Observe metrics for counter animation
const metricsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const value = entry.target.textContent;
            const num = parseInt(value);
            if (!isNaN(num) && num > 0) {
                animateCounter(entry.target, num);
                metricsObserver.unobserve(entry.target); // Only animate once
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('.metric-value, .card-number').forEach(metric => {
    metricsObserver.observe(metric);
});

// Google Reviews Integration
const GOOGLE_CONFIG = {
    apiKey: 'YOUR_GOOGLE_API_KEY', // Replace with your Google API key
    placeId: 'YOUR_PLACE_ID' // Replace with your Google Business Place ID
};

// EmailJS Configuration
const EMAILJS_CONFIG = {
    serviceID: 'service_uttf6t9',      // EmailJS Service ID
    templateID: 'template_6uaqvba',    // EmailJS Template ID
    publicKey: 'm57DbJAg_P8Un7r-D'     // EmailJS Public Key
};

// Fetch Google Reviews
async function fetchGoogleReviews() {
    const reviewsGrid = document.getElementById('reviewsGrid');
    
    if (!GOOGLE_CONFIG.apiKey || GOOGLE_CONFIG.apiKey === 'YOUR_GOOGLE_API_KEY') {
        // Show demo reviews if API not configured
        displayDemoReviews();
        return;
    }
    
    try {
        const response = await fetch(
            `https://maps.googleapis.com/maps/api/place/details/json?place_id=${GOOGLE_CONFIG.placeId}&fields=reviews,rating,user_ratings_total&key=${GOOGLE_CONFIG.apiKey}`
        );
        
        if (!response.ok) {
            throw new Error('Failed to fetch reviews');
        }
        
        const data = await response.json();
        
        if (data.result && data.result.reviews) {
            // Filter for 5-star reviews only
            const fiveStarReviews = data.result.reviews.filter(review => review.rating === 5);
            displayReviews(fiveStarReviews);
        } else {
            displayDemoReviews();
        }
    } catch (error) {
        console.error('Error fetching Google reviews:', error);
        displayDemoReviews();
    }
}

// Display reviews in the grid
function displayReviews(reviews) {
    const reviewsGrid = document.getElementById('reviewsGrid');
    reviewsGrid.innerHTML = '';
    
    // Limit to 6 most recent reviews
    const limitedReviews = reviews.slice(0, 6);
    
    limitedReviews.forEach((review, index) => {
        const reviewCard = createReviewCard(review, index);
        reviewsGrid.appendChild(reviewCard);
    });
}

// Create a review card element
function createReviewCard(review, index) {
    const card = document.createElement('div');
    card.className = 'review-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    // Get initials from name
    const initials = review.author_name
        .split(' ')
        .map(word => word[0])
        .join('')
        .substring(0, 2)
        .toUpperCase();
    
    // Format date
    const date = new Date(review.time * 1000);
    const formattedDate = date.toLocaleDateString('en-US', { 
        month: 'short', 
        year: 'numeric' 
    });
    
    // Create stars HTML
    const starsHTML = '⭐'.repeat(5);
    
    card.innerHTML = `
        <div class="review-header">
            <div class="review-avatar">${initials}</div>
            <div class="review-info">
                <div class="review-name">${review.author_name}</div>
                <div class="review-date">${formattedDate}</div>
            </div>
        </div>
        <div class="review-stars">${starsHTML}</div>
        <p class="review-text">${review.text}</p>
        <div class="review-google-badge">
            <span>Posted on Google</span>
        </div>
    `;
    
    return card;
}

// Display demo reviews (fallback)
function displayDemoReviews() {
    const demoReviews = [
        {
            author_name: 'Sarah Johnson',
            text: 'IFLA has completely transformed my language learning experience! The interactive lessons and personalized approach made learning Japanese enjoyable and effective. Highly recommend!',
            time: Date.now() / 1000 - 86400 * 30
        },
        {
            author_name: 'Michael Chen',
            text: 'Best language learning platform I\'ve used! The teachers are amazing and the curriculum is well-structured. I went from beginner to conversational in just 6 months.',
            time: Date.now() / 1000 - 86400 * 45
        },
        {
            author_name: 'Emma Rodriguez',
            text: 'Excellent program! The cultural immersion aspects really set IFLA apart. I not only learned the language but also gained deep insights into the culture.',
            time: Date.now() / 1000 - 86400 * 60
        },
        {
            author_name: 'David Kim',
            text: 'Outstanding quality and value. The flexibility to learn at my own pace while having expert guidance made all the difference. Worth every penny!',
            time: Date.now() / 1000 - 86400 * 15
        },
        {
            author_name: 'Lisa Thompson',
            text: 'IFLA exceeded all my expectations! The interactive platform, supportive community, and knowledgeable instructors created the perfect learning environment.',
            time: Date.now() / 1000 - 86400 * 20
        },
        {
            author_name: 'James Wilson',
            text: 'Incredible experience! The personalized learning path and real-time feedback helped me achieve fluency faster than I ever thought possible.',
            time: Date.now() / 1000 - 86400 * 10
        }
    ];
    
    displayReviews(demoReviews);
}

// Initialize EmailJS
(function() {
    // Initialize EmailJS with your public key
    if (typeof emailjs !== 'undefined' && EMAILJS_CONFIG.publicKey !== 'YOUR_PUBLIC_KEY') {
        emailjs.init(EMAILJS_CONFIG.publicKey);
    }
})();

// Initialize reviews when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Wait a bit for other content to load first
    setTimeout(() => {
        fetchGoogleReviews();
    }, 1000);
    
    // Contact form submission handler
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleFormSubmit);
        
        // Add fade-in animation for contact section
        const contactSection = document.querySelector('.contact-section');
        if (contactSection) {
            contactSection.style.opacity = '0';
            contactSection.style.transform = 'translateY(30px)';
            contactSection.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            fadeObserver.observe(contactSection);
        }
        
        // Add fade-in animation for footer
        const footer = document.querySelector('.footer');
        if (footer) {
            footer.style.opacity = '0';
            footer.style.transform = 'translateY(30px)';
            footer.style.transition = 'opacity 0.8s ease 0.2s, transform 0.8s ease 0.2s';
            fadeObserver.observe(footer);
        }
    }
});

// API Configuration
const API_BASE_URL = window.location.origin;

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

// Handle contact form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('.form-submit-btn');
    const originalText = submitBtn.querySelector('span').textContent;
    
    // Get form data
    const formData = new FormData(form);
    const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        language: formData.get('language'),
        message: formData.get('message')
    };
    
    // Validate form data
    if (!data.name || !data.email || !data.language || !data.message) {
        showNotification('Please fill in all fields', 'error');
        return;
    }
    
    // Validate email format
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(data.email)) {
        showNotification('Please enter a valid email address', 'error');
        return;
    }
    
    // Disable submit button and show loading state
    submitBtn.disabled = true;
    submitBtn.querySelector('span').textContent = 'Sending...';
    submitBtn.style.opacity = '0.7';
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/contact/submit/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            credentials: 'include',
            body: JSON.stringify(data)
        });
        
        const responseData = await response.json();
        
        if (response.ok) {
            submitBtn.querySelector('span').textContent = 'Message Sent!';
            submitBtn.style.background = 'linear-gradient(135deg, #4CAF50 0%, #45a049 100%)';
            form.reset();
            showNotification('Thank you! Your message has been sent successfully. We\'ll get back to you soon!', 'success');
            setTimeout(() => resetButton(submitBtn, originalText), 3000);
        } else {
            submitBtn.querySelector('span').textContent = 'Failed to Send';
            submitBtn.style.background = 'linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%)';
            showNotification(responseData.error || 'Failed to send message. Please try again.', 'error');
            setTimeout(() => resetButton(submitBtn, originalText), 3000);
        }
    } catch (error) {
        console.error('Contact form error:', error);
        submitBtn.querySelector('span').textContent = 'Failed to Send';
        submitBtn.style.background = 'linear-gradient(135deg, #FF6B6B 0%, #EE5A52 100%)';
        showNotification('An error occurred. Please try again.', 'error');
        setTimeout(() => resetButton(submitBtn, originalText), 3000);
    }
}

// Note: EmailJS functionality removed - now using Django backend API

// Reset submit button to original state
function resetButton(submitBtn, originalText) {
    submitBtn.disabled = false;
    submitBtn.querySelector('span').textContent = originalText;
    submitBtn.style.opacity = '1';
    submitBtn.style.background = 'linear-gradient(135deg, #5856D6 0%, #7B68EE 100%)';
}

// Show notification to user
function showNotification(message, type) {
    // Remove any existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }
    
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 100px;
        right: 20px;
        padding: 20px 30px;
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

console.log('✨ Optimized animations loaded!');

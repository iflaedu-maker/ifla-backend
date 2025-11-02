// Language data with pricing information
const languageData = {
    japanese: {
        flag: '🇯🇵',
        name: 'Japanese',
        category: 1,
        description: 'Master the elegant Japanese language and immerse yourself in one of the world\'s most fascinating cultures. Learn hiragana, katakana, and kanji while exploring Japanese customs, traditions, and modern society.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹16,000' },
            { level: 'A2 - Elementary', price: '₹18,000' },
            { level: 'B1 - Intermediate', price: '₹20,000' },
            { level: 'B2 - Upper Intermediate', price: '₹22,000' },
            { level: 'C1 - Advanced', price: '₹24,000' },
            { level: 'C2 - Proficiency', price: '₹26,000' }
        ]
    },
    chinese: {
        flag: '🇨🇳',
        name: 'Chinese',
        category: 1,
        description: 'Learn Mandarin Chinese and unlock opportunities in the world\'s most spoken language. Master the tones, characters, and cultural nuances that make Chinese unique and fascinating.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹16,000' },
            { level: 'A2 - Elementary', price: '₹18,000' },
            { level: 'B1 - Intermediate', price: '₹20,000' },
            { level: 'B2 - Upper Intermediate', price: '₹22,000' },
            { level: 'C1 - Advanced', price: '₹24,000' },
            { level: 'C2 - Proficiency', price: '₹26,000' }
        ]
    },
    hebrew: {
        flag: '🇮🇱',
        name: 'Hebrew',
        category: 1,
        description: 'Discover the ancient Hebrew language and connect with its rich historical and cultural heritage. Learn to read, write, and speak modern Hebrew while exploring its biblical roots.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹16,000' },
            { level: 'A2 - Elementary', price: '₹18,000' },
            { level: 'B1 - Intermediate', price: '₹20,000' },
            { level: 'B2 - Upper Intermediate', price: '₹22,000' },
            { level: 'C1 - Advanced', price: '₹24,000' },
            { level: 'C2 - Proficiency', price: '₹26,000' }
        ]
    },
    korean: {
        flag: '🇰🇷',
        name: 'Korean',
        category: 1,
        description: 'Explore Korean language and dive into K-culture, K-pop, and modern Korean society. Learn Hangul and master the unique grammar structure while discovering Korean traditions.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹16,000' },
            { level: 'A2 - Elementary', price: '₹18,000' },
            { level: 'B1 - Intermediate', price: '₹20,000' },
            { level: 'B2 - Upper Intermediate', price: '₹22,000' },
            { level: 'C1 - Advanced', price: '₹24,000' },
            { level: 'C2 - Proficiency', price: '₹26,000' }
        ]
    },
    russian: {
        flag: '🇷🇺',
        name: 'Russian',
        category: 1,
        description: 'Master Russian and access the language of Tolstoy, Dostoyevsky, and rich Slavic culture. Learn the Cyrillic alphabet and complex grammar while exploring Russian literature and arts.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹16,000' },
            { level: 'A2 - Elementary', price: '₹18,000' },
            { level: 'B1 - Intermediate', price: '₹20,000' },
            { level: 'B2 - Upper Intermediate', price: '₹22,000' },
            { level: 'C1 - Advanced', price: '₹24,000' },
            { level: 'C2 - Proficiency', price: '₹26,000' }
        ]
    },
    dutch: {
        flag: '🇳🇱',
        name: 'Dutch',
        category: 1,
        description: 'Learn Dutch and open doors to opportunities in the Netherlands and Belgium. Master this Germanic language and discover the rich culture of the Low Countries.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹16,000' },
            { level: 'A2 - Elementary', price: '₹18,000' },
            { level: 'B1 - Intermediate', price: '₹20,000' },
            { level: 'B2 - Upper Intermediate', price: '₹22,000' },
            { level: 'C1 - Advanced', price: '₹24,000' },
            { level: 'C2 - Proficiency', price: '₹26,000' }
        ]
    },
    swedish: {
        flag: '🇸🇪',
        name: 'Swedish',
        category: 1,
        description: 'Embrace Swedish and connect with Scandinavian culture, design, and innovation. Learn one of the North Germanic languages and explore Swedish traditions and modern lifestyle.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹16,000' },
            { level: 'A2 - Elementary', price: '₹18,000' },
            { level: 'B1 - Intermediate', price: '₹20,000' },
            { level: 'B2 - Upper Intermediate', price: '₹22,000' },
            { level: 'C1 - Advanced', price: '₹24,000' },
            { level: 'C2 - Proficiency', price: '₹26,000' }
        ]
    },
    arabic: {
        flag: '🇸🇦',
        name: 'Arabic',
        category: 2,
        description: 'Learn Modern Standard Arabic and explore the rich cultural heritage of the Arab world. Master the Arabic script and discover one of the world\'s most influential languages.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹14,000' },
            { level: 'A2 - Elementary', price: '₹16,000' },
            { level: 'B1 - Intermediate', price: '₹18,000' },
            { level: 'B2 - Upper Intermediate', price: '₹20,000' },
            { level: 'C1 - Advanced', price: '₹22,000' },
            { level: 'C2 - Proficiency', price: '₹24,000' }
        ]
    },
    french: {
        flag: '🇫🇷',
        name: 'French',
        category: 2,
        description: 'Master the language of love, diplomacy, and one of the world\'s most beautiful cultures. Learn French and access a world of art, cuisine, fashion, and international relations.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹14,000' },
            { level: 'A2 - Elementary', price: '₹16,000' },
            { level: 'B1 - Intermediate', price: '₹18,000' },
            { level: 'B2 - Upper Intermediate', price: '₹20,000' },
            { level: 'C1 - Advanced', price: '₹22,000' },
            { level: 'C2 - Proficiency', price: '₹24,000' }
        ]
    },
    spanish: {
        flag: '🇪🇸',
        name: 'Spanish',
        category: 2,
        description: 'Learn Spanish and connect with over 500 million speakers across the globe. Discover the vibrant cultures of Spain and Latin America while mastering one of the world\'s most useful languages.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹14,000' },
            { level: 'A2 - Elementary', price: '₹16,000' },
            { level: 'B1 - Intermediate', price: '₹18,000' },
            { level: 'B2 - Upper Intermediate', price: '₹20,000' },
            { level: 'C1 - Advanced', price: '₹22,000' },
            { level: 'C2 - Proficiency', price: '₹24,000' }
        ]
    },
    italian: {
        flag: '🇮🇹',
        name: 'Italian',
        category: 2,
        description: 'Discover Italian, the language of art, music, cuisine, and la dolce vita. Learn to speak like a native while exploring Italy\'s incredible cultural contributions to the world.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹14,000' },
            { level: 'A2 - Elementary', price: '₹16,000' },
            { level: 'B1 - Intermediate', price: '₹18,000' },
            { level: 'B2 - Upper Intermediate', price: '₹20,000' },
            { level: 'C1 - Advanced', price: '₹22,000' },
            { level: 'C2 - Proficiency', price: '₹24,000' }
        ]
    },
    german: {
        flag: '🇩🇪',
        name: 'German',
        category: 2,
        description: 'Master German and access opportunities in Europe\'s largest economy and beyond. Learn the language of Goethe, Einstein, and modern engineering excellence.',
        pricing: [
            { level: 'A1 - Beginner', price: '₹14,000' },
            { level: 'A2 - Elementary', price: '₹16,000' },
            { level: 'B1 - Intermediate', price: '₹18,000' },
            { level: 'B2 - Upper Intermediate', price: '₹20,000' },
            { level: 'C1 - Advanced', price: '₹22,000' },
            { level: 'C2 - Proficiency', price: '₹24,000' }
        ]
    }
};

// Modal functionality
const modal = document.getElementById('pricingModal');
const modalOverlay = modal.querySelector('.pricing-modal-overlay');
const closeBtn = modal.querySelector('.modal-close');

// Open modal with language details
function openModal(language) {
    const data = languageData[language];
    if (!data) return;

    // Populate modal content
    document.getElementById('modalFlag').textContent = data.flag;
    document.getElementById('modalTitle').textContent = data.name;
    document.getElementById('modalDescription').textContent = data.description;

    // Populate pricing levels
    const pricingLevelsContainer = document.getElementById('pricingLevels');
    pricingLevelsContainer.innerHTML = '';
    
    data.pricing.forEach(level => {
        const levelDiv = document.createElement('div');
        levelDiv.className = 'pricing-level';
        levelDiv.innerHTML = `
            <span class="level-name">${level.level}</span>
            <span class="level-price">${level.price} + taxes</span>
        `;
        pricingLevelsContainer.appendChild(levelDiv);
    });

    // Update enroll button to check authentication
    const enrollBtn = modal.querySelector('.modal-cta-btn') || modal.querySelector('#enrollNowBtn');
    if (enrollBtn) {
        // Store language name for later use
        enrollBtn.dataset.language = data.name;
        
        // Remove old click handler if exists (by cloning)
        const newEnrollBtn = enrollBtn.cloneNode(true);
        enrollBtn.parentNode.replaceChild(newEnrollBtn, enrollBtn);
        
        // Add new click handler
        newEnrollBtn.addEventListener('click', handleEnrollClick);
    }

    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden';
}

// Handle enroll button click
function handleEnrollClick(e) {
    e.preventDefault();
    e.stopPropagation(); // Prevent event from bubbling to modal overlay
    const languageName = this.dataset.language || this.getAttribute('data-language');
    
    if (!languageName) {
        console.error('Language name not found');
        return;
    }
    
    console.log('Enroll button clicked for language:', languageName);
    
    // Check if user is authenticated by making an API call
    fetch('/api/auth/profile/', {
        method: 'GET',
        credentials: 'include',
        headers: {
            'Content-Type': 'application/json',
        }
    })
    .then(response => {
        console.log('Auth check response status:', response.status);
        if (response.ok) {
            // User is authenticated - redirect to enrollment page with language
            const enrollmentUrl = `/enrollment/?language=${encodeURIComponent(languageName)}`;
            console.log('User authenticated, redirecting to:', enrollmentUrl);
            // Redirect immediately - don't wait for modal to close
            window.location.href = enrollmentUrl;
        } else {
            // User is not authenticated, redirect to signup page
            console.log('User not authenticated, redirecting to signup');
            sessionStorage.setItem('redirectAfterLogin', `/enrollment/?language=${encodeURIComponent(languageName)}`);
            window.location.href = '/auth/?action=signup';
        }
    })
    .catch(error => {
        console.error('Error checking authentication:', error);
        // On error, redirect to signup page
        sessionStorage.setItem('redirectAfterLogin', `/enrollment/?language=${encodeURIComponent(languageName)}`);
        window.location.href = '/auth/?action=signup';
    });
}

// Close modal
function closeModal() {
    modal.classList.remove('active');
    document.body.style.overflow = '';
}

// Event listeners for language cards
document.querySelectorAll('.language-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
        const card = e.target.closest('.language-card');
        const language = card.getAttribute('data-language');
        openModal(language);
    });
});

// Close modal events
closeBtn.addEventListener('click', closeModal);
modalOverlay.addEventListener('click', closeModal);

// Close modal on ESC key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
    }
});

// Navbar scroll effect
const navbar = document.querySelector('.navbar');
let lastScrollTop = 0;

function handleScroll() {
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
}

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

const throttledScroll = throttle(handleScroll, 100);
window.addEventListener('scroll', throttledScroll, { passive: true });

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const fadeObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Search functionality
const searchInput = document.getElementById('languageSearch');
const clearBtn = document.getElementById('clearSearch');
const searchResultsCount = document.getElementById('searchResultsCount');
const languageCards = document.querySelectorAll('.language-card');

function filterLanguages() {
    const searchTerm = searchInput.value.toLowerCase().trim();
    let visibleCount = 0;

    languageCards.forEach(card => {
        const languageName = card.getAttribute('data-language');
        const languageData = window.languageData ? window.languageData[languageName] : null;
        const displayName = languageData ? languageData.name.toLowerCase() : languageName;

        if (displayName.includes(searchTerm)) {
            card.classList.remove('hidden');
            visibleCount++;
        } else {
            card.classList.add('hidden');
        }
    });

    // Show/hide clear button
    if (searchTerm) {
        clearBtn.style.display = 'flex';
        if (visibleCount === 0) {
            searchResultsCount.textContent = 'No languages found';
            searchResultsCount.style.color = 'rgba(255, 107, 107, 0.8)';
        } else if (visibleCount === languageCards.length) {
            searchResultsCount.textContent = `Showing all ${visibleCount} languages`;
            searchResultsCount.style.color = 'rgba(255, 255, 255, 0.6)';
        } else {
            searchResultsCount.textContent = `Found ${visibleCount} language${visibleCount !== 1 ? 's' : ''}`;
            searchResultsCount.style.color = 'rgba(88, 86, 214, 0.9)';
        }
    } else {
        clearBtn.style.display = 'none';
        searchResultsCount.textContent = '';
    }
}

function clearSearch() {
    searchInput.value = '';
    filterLanguages();
    searchInput.focus();
}

// Search event listeners
if (searchInput) {
    searchInput.addEventListener('input', filterLanguages);
    searchInput.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            clearSearch();
        }
    });
}

if (clearBtn) {
    clearBtn.addEventListener('click', clearSearch);
}

// Make languageData globally accessible for search
window.languageData = languageData;

// Observe elements for fade-in animation
document.addEventListener('DOMContentLoaded', () => {
    // Animate search bar
    const searchBar = document.querySelector('.search-bar-container');
    if (searchBar) {
        searchBar.style.opacity = '0';
        searchBar.style.transform = 'translateY(20px)';
        searchBar.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        setTimeout(() => {
            searchBar.style.opacity = '1';
            searchBar.style.transform = 'translateY(0)';
        }, 300);
    }
});

console.log('✨ Languages page loaded successfully!');


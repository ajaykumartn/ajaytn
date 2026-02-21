// Enhanced Portfolio JavaScript with Advanced Animations
console.log('🚀 Loading enhanced portfolio JavaScript...');

// Global animation state
let animationObserver;
let mousePosition = { x: 0, y: 0 };

// Wait for DOM to be ready
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, initializing enhanced features...');
    
    // Initialize core libraries
    initLibraries();
    
    // Initialize enhanced features
    setTimeout(initParticles, 500);
    setTimeout(initTypingAnimation, 1000);
    
    // Initialize interactive features
    initMobileMenu();
    initScrollToTop();
    initContactForm();
    initProjectCards();
    initScrollAnimations();
    initMouseEffects();
    initHeaderEffects();
    initMagneticButtons();
    initParallaxEffects();
    initTextAnimations();
    
    console.log('✨ All enhanced features initialized!');
});

// Initialize core libraries
function initLibraries() {
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
        console.log('✓ Lucide icons initialized');
    } else {
        console.warn('✗ Lucide icons not found');
    }
    
    // Initialize AOS animations with enhanced settings
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: false,
            offset: 50,
            easing: 'ease-out-cubic',
            mirror: true
        });
        console.log('✓ Enhanced AOS animations initialized');
    } else {
        console.warn('✗ AOS not found');
    }
}

// Enhanced Particles.js initialization
function initParticles() {
    // Particles removed as per user request
    console.log('✓ Particles disabled');
}

// Typing animation
function initTypingAnimation() {
    const typingElement = document.getElementById('typing-text');
    
    if (typingElement) {
        console.log('Starting typing animation...');
        
        const words = [
            'AI/ML DEVELOPER',
            'DATA SCIENTIST',
            'PROBLEM SOLVER',
            'TECH ENTHUSIAST'
        ];
        
        let wordIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        
        function type() {
            const currentWord = words[wordIndex];
            
            if (isDeleting) {
                typingElement.textContent = currentWord.substring(0, charIndex - 1);
                charIndex--;
            } else {
                typingElement.textContent = currentWord.substring(0, charIndex + 1);
                charIndex++;
            }
            
            if (!isDeleting && charIndex === currentWord.length) {
                setTimeout(() => isDeleting = true, 2000);
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                wordIndex = (wordIndex + 1) % words.length;
            }
            
            setTimeout(type, isDeleting ? 50 : 100);
        }
        
        type();
        console.log('✓ Typing animation started');
    }
}

// Mobile menu
function initMobileMenu() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const navLinks = document.querySelector('.nav-links');
    
    if (mobileMenuBtn && navLinks) {
        mobileMenuBtn.addEventListener('click', function() {
            navLinks.style.display = navLinks.style.display === 'flex' ? 'none' : 'flex';
        });
        
        console.log('✓ Mobile menu initialized');
    }
}

// Scroll to top button
function initScrollToTop() {
    const scrollTopBtn = document.getElementById('scroll-top');
    
    if (scrollTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 300) {
                scrollTopBtn.style.display = 'block';
            } else {
                scrollTopBtn.style.display = 'none';
            }
        });
        
        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        
        console.log('✓ Scroll to top initialized');
    }
}

// Contact form
function initContactForm() {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        const submitButton = document.getElementById('submit-button');
        const formStatus = document.getElementById('form-status');
        
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Sending...';
            submitButton.disabled = true;
            formStatus.textContent = '';
            
            const formData = {
                name: contactForm.name.value,
                email: contactForm.email.value,
                message: contactForm.message.value
            };
            
            try {
                const response = await fetch('/send-email', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(formData)
                });
                
                const result = await response.json();
                
                if (response.ok) {
                    formStatus.textContent = 'Message sent successfully!';
                    formStatus.style.color = '#10b981';
                    contactForm.reset();
                } else {
                    formStatus.textContent = result.error || 'An error occurred. Please try again.';
                    formStatus.style.color = '#ef4444';
                }
            } catch (error) {
                console.error('Form submission error:', error);
                formStatus.textContent = 'Network error. Please try again.';
                formStatus.style.color = '#ef4444';
            } finally {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            }
        });
        
        console.log('✓ Contact form initialized');
    }
}

// Project cards 3D tilt effect
function initProjectCards() {
    if (typeof VanillaTilt !== 'undefined') {
        VanillaTilt.init(document.querySelectorAll('.project-card'), {
            max: 15,
            speed: 400,
            glare: true,
            'max-glare': 0.5
        });
        
        console.log('✓ Project card tilt effects initialized');
    }
}

// Smooth scrolling for navigation links
document.addEventListener('click', function(e) {
    if (e.target.matches('a[href^="#"]')) {
        e.preventDefault();
        const targetId = e.target.getAttribute('href');
        const targetElement = document.querySelector(targetId);
        
        if (targetElement) {
            targetElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
});

// Initialize scroll-triggered animations
function initScrollAnimations() {
    animationObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
                
                // Change aurora background based on section
                changeAuroraColor(entry.target.id);
                
                // Add stagger effect for grouped elements
                if (entry.target.classList.contains('skill-card')) {
                    const index = Array.from(entry.target.parentNode.children).indexOf(entry.target);
                    entry.target.style.animationDelay = `${index * 0.1}s`;
                }
                
                if (entry.target.classList.contains('project-card')) {
                    const index = Array.from(entry.target.parentNode.children).indexOf(entry.target);
                    entry.target.style.animationDelay = `${index * 0.2}s`;
                }
            }
        });
    }, { threshold: 0.3, rootMargin: '0px 0px -50px 0px' });
    
    // Observe elements for animation
    const elementsToAnimate = document.querySelectorAll(
        '.section-heading, .about-image, .about-text, .project-card, .skill-card, .timeline-item, .achievement-item, .contact-form'
    );
    
    elementsToAnimate.forEach(el => animationObserver.observe(el));
    
    // Observe sections for aurora color change
    const sections = document.querySelectorAll('section');
    sections.forEach(section => animationObserver.observe(section));
    
    console.log('✓ Scroll animations initialized');
}

// Change aurora background color based on section
function changeAuroraColor(sectionId) {
    const auroraBg = document.querySelector('.aurora-bg');
    if (!auroraBg) return;
    
    const colorSchemes = {
        'home': 'linear-gradient(125deg, #0c0a18, #1a1a3d, #3c1e5a, #5e2f75)',
        'about': 'linear-gradient(125deg, #1a1a3d, #2d1b4e, #4a1e6b, #5e2f75)',
        'projects': 'linear-gradient(125deg, #0c0a18, #1a1a3d, #2d1b4e, #3c1e5a)',
        'skills': 'linear-gradient(125deg, #2d1b4e, #3c1e5a, #5e2f75, #7c3aed)',
        'experience': 'linear-gradient(125deg, #1a1a3d, #2d1b4e, #3c1e5a, #4a1e6b)',
        'achievements': 'linear-gradient(125deg, #0c0a18, #1a1a3d, #3c1e5a, #5e2f75)',
        'contact': 'linear-gradient(125deg, #2d1b4e, #3c1e5a, #5e2f75, #1a1a3d)'
    };
    
    if (colorSchemes[sectionId]) {
        auroraBg.style.background = colorSchemes[sectionId];
        auroraBg.style.backgroundSize = '400% 400%';
    }
}

// Initialize mouse tracking
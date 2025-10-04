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
    const particlesContainer = document.getElementById('particles-js');
    
    if (particlesContainer && typeof particlesJS !== 'undefined') {
        console.log('🌟 Initializing enhanced particles...');
        
        particlesJS('particles-js', {
            particles: {
                number: {
                    value: 120,
                    density: { enable: true, value_area: 800 }
                },
                color: { 
                    value: ['#c084fc', '#ec4899', '#8b5cf6', '#a855f7'] 
                },
                shape: { 
                    type: ['circle', 'triangle'],
                    stroke: { width: 0, color: '#000000' }
                },
                opacity: {
                    value: 0.6,
                    random: true,
                    anim: { enable: true, speed: 1, opacity_min: 0.1, sync: false }
                },
                size: {
                    value: 4,
                    random: true,
                    anim: { enable: true, speed: 2, size_min: 0.1, sync: false }
                },
                line_linked: {
                    enable: true,
                    distance: 150,
                    color: '#c084fc',
                    opacity: 0.3,
                    width: 1
                },
                move: {
                    enable: true,
                    speed: 3,
                    direction: 'none',
                    random: true,
                    straight: false,
                    out_mode: 'out',
                    bounce: false,
                    attract: { enable: true, rotateX: 600, rotateY: 1200 }
                }
            },
            interactivity: {
                detect_on: 'canvas',
                events: {
                    onhover: { enable: true, mode: 'bubble' },
                    onclick: { enable: true, mode: 'push' },
                    resize: true
                },
                modes: {
                    grab: { distance: 400, line_linked: { opacity: 1 } },
                    bubble: { distance: 250, size: 8, duration: 2, opacity: 0.8, speed: 3 },
                    repulse: { distance: 200, duration: 0.4 },
                    push: { particles_nb: 6 },
                    remove: { particles_nb: 2 }
                }
            },
            retina_detect: true
        });
        
        console.log('✓ Enhanced particles initialized');
    } else {
        console.warn('✗ Particles.js or container not found');
    }
}

// Typing animation
function initTypingAnimation() {
    const typingElement = document.getElementById('typing-text');
    
    if (typingElement) {
        console.log('Starting typing animation...');
        
        const words = [
            'AI & Machine Learning Enthusiast',
            'B.Tech CSE Student', 
            'A Creative Problem Solver',
            'A Lifelong Learner'
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
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
    
    // Observe elements for animation
    const elementsToAnimate = document.querySelectorAll(
        '.section-heading, .about-image, .project-card, .skill-card, .timeline-item, .achievement-item, .contact-form'
    );
    
    elementsToAnimate.forEach(el => animationObserver.observe(el));
    console.log('✓ Scroll animations initialized');
}

// Initialize mous
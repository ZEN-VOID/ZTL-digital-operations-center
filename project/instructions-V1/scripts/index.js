/* ==========================================
   ZTL数智化作战中心 - 主页脚本
   Homepage Specific JavaScript
   ========================================== */

// ==========================================
// Initialize on DOM load
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    initStatsCounter();
    initOrbitalSystem();
    initFeatureCards();
});

// ==========================================
// Stats Counter Animation
// ==========================================
function initStatsCounter() {
    const statCards = document.querySelectorAll('.stat-card');
    let hasAnimated = false;

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                animateAllStats();
            }
        });
    }, observerOptions);

    statCards.forEach(card => observer.observe(card));
}

function animateAllStats() {
    const statNumbers = document.querySelectorAll('.stat-number');

    statNumbers.forEach(stat => {
        const targetValue = parseInt(stat.getAttribute('data-count'));
        const duration = 2000; // 2 seconds
        const start = 0;

        animateValue(stat, start, targetValue, duration);
    });
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16); // 60fps
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current);
    }, 16);
}

// ==========================================
// Orbital System Interactions
// ==========================================
function initOrbitalSystem() {
    const planets = document.querySelectorAll('.planet');

    planets.forEach(planet => {
        // Add hover glow effect
        planet.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.2)';
            this.style.zIndex = '10';
        });

        planet.addEventListener('mouseleave', function() {
            const originalTransform = getOriginalTransform(this);
            this.style.transform = originalTransform;
            this.style.zIndex = '1';
        });

        // Add click navigation
        planet.addEventListener('click', function() {
            const category = this.classList[1].replace('planet-', '');
            navigateToPage(category);
        });
    });

    // Animate orbits on scroll
    const orbitalSystem = document.querySelector('.orbital-system');
    if (orbitalSystem) {
        window.addEventListener('scroll', throttleScroll(function() {
            const scrolled = window.pageYOffset;
            const orbits = orbitalSystem.querySelectorAll('.orbit');

            orbits.forEach((orbit, index) => {
                const speed = (index + 1) * 0.05;
                orbit.style.transform = `translate(-50%, -50%) rotate(${scrolled * speed}deg)`;
            });
        }, 16));
    }
}

function getOriginalTransform(element) {
    if (element.style.top === '0px') return 'translateX(-50%)';
    if (element.style.bottom === '0px') return 'translateX(-50%)';
    if (element.style.right === '0px') return 'translateY(-50%)';
    if (element.style.left === '0px') return 'translateY(-50%)';
    return 'translate(-50%, -50%)';
}

function navigateToPage(category) {
    const pageMap = {
        'agents': 'agents.html',
        'skills': 'skills.html',
        'commands': 'commands.html',
        'mcp': 'mcp-servers.html'
    };

    if (pageMap[category]) {
        // Add transition effect
        document.body.style.opacity = '0';
        document.body.style.transition = 'opacity 0.3s ease';

        setTimeout(() => {
            window.location.href = pageMap[category];
        }, 300);
    }
}

function throttleScroll(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ==========================================
// Feature Cards Stagger Animation
// ==========================================
function initFeatureCards() {
    const featureCards = document.querySelectorAll('.feature-card');

    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger animation delay
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, index * 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    featureCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(50px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });
}

// ==========================================
// Architecture Layer Interactions
// ==========================================
function initArchitectureLayers() {
    const layers = document.querySelectorAll('.layer-block');

    layers.forEach((layer, index) => {
        layer.addEventListener('mouseenter', function() {
            // Highlight related layers
            layers.forEach((l, i) => {
                if (i <= index) {
                    l.style.opacity = '1';
                } else {
                    l.style.opacity = '0.5';
                }
            });
        });

        layer.addEventListener('mouseleave', function() {
            layers.forEach(l => {
                l.style.opacity = '1';
            });
        });
    });
}

// Initialize architecture layers if they exist
if (document.querySelector('.layer-block')) {
    initArchitectureLayers();
}

// ==========================================
// Performance Metrics Animation
// ==========================================
function initPerformanceMetrics() {
    const performanceCards = document.querySelectorAll('.performance-card');

    const observerOptions = {
        threshold: 0.3
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('metric-visible');
                animatePerformanceValue(entry.target);
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    performanceCards.forEach(card => {
        observer.observe(card);
    });
}

function animatePerformanceValue(card) {
    const valueElement = card.querySelector('.performance-value');
    if (!valueElement) return;

    const text = valueElement.textContent;
    const match = text.match(/(\d+)/);

    if (match) {
        const targetValue = parseInt(match[1]);
        const duration = 1500;
        let current = 0;
        const increment = targetValue / (duration / 16);

        const timer = setInterval(() => {
            current += increment;
            if (current >= targetValue) {
                current = targetValue;
                clearInterval(timer);
            }

            // Keep the % sign if it exists
            valueElement.textContent = Math.round(current) + (text.includes('%') ? '%' : '');
        }, 16);
    }
}

// Initialize performance metrics
if (document.querySelector('.performance-card')) {
    initPerformanceMetrics();
}

// ==========================================
// Use Cases Preview Interactions
// ==========================================
function initUseCasesPreview() {
    const useCaseCards = document.querySelectorAll('.use-case-card');

    useCaseCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            // Scale up the card
            this.style.transform = 'translateY(-10px) scale(1.05)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(-5px) scale(1)';
        });
    });
}

// Initialize use cases
if (document.querySelector('.use-case-card')) {
    initUseCasesPreview();
}

// ==========================================
// Parallax Effect for Hero Section
// ==========================================
function initParallaxEffect() {
    const heroContent = document.querySelector('.hero-content');
    const heroVisual = document.querySelector('.hero-visual');

    if (heroContent && heroVisual) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;

            if (scrolled < window.innerHeight) {
                heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
                heroContent.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;

                heroVisual.style.transform = `translateY(${scrolled * 0.2}px)`;
                heroVisual.style.opacity = 1 - (scrolled / window.innerHeight) * 0.3;
            }
        });
    }
}

// Initialize parallax effect
initParallaxEffect();

// ==========================================
// Keyboard Navigation
// ==========================================
document.addEventListener('keydown', function(e) {
    // Press 'h' to go home
    if (e.key === 'h' && !isInputFocused()) {
        window.location.href = 'index.html';
    }

    // Press numbers 1-6 for quick navigation
    const keyMap = {
        '1': 'agents.html',
        '2': 'skills.html',
        '3': 'commands.html',
        '4': 'mcp-servers.html',
        '5': 'architecture.html',
        '6': 'use-cases.html'
    };

    if (keyMap[e.key] && !isInputFocused()) {
        window.location.href = keyMap[e.key];
    }
});

function isInputFocused() {
    const activeElement = document.activeElement;
    return activeElement.tagName === 'INPUT' ||
           activeElement.tagName === 'TEXTAREA' ||
           activeElement.isContentEditable;
}

// ==========================================
// Easter Egg: Konami Code
// ==========================================
(function() {
    const konamiCode = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];
    let konamiIndex = 0;

    document.addEventListener('keydown', function(e) {
        if (e.key === konamiCode[konamiIndex]) {
            konamiIndex++;

            if (konamiIndex === konamiCode.length) {
                activateEasterEgg();
                konamiIndex = 0;
            }
        } else {
            konamiIndex = 0;
        }
    });

    function activateEasterEgg() {
        // Add rainbow effect to the title
        const title = document.querySelector('.hero-title');
        if (title) {
            title.style.animation = 'rainbow 2s linear infinite';

            // Add rainbow animation keyframes
            const style = document.createElement('style');
            style.textContent = `
                @keyframes rainbow {
                    0% { filter: hue-rotate(0deg); }
                    100% { filter: hue-rotate(360deg); }
                }
            `;
            document.head.appendChild(style);

            // Show a message
            setTimeout(() => {
                alert('🎉 You found the secret! Welcome to the ZTL Command Center! 🚀');
            }, 500);
        }
    }
})();

// ==========================================
// Console Art
// ==========================================
console.log('%c' +
    '╔═══════════════════════════════════════╗\n' +
    '║  ZTL数智化作战中心                     ║\n' +
    '║  Digital Intelligence Command Center  ║\n' +
    '║  Powered by Claude Sonnet 4.5         ║\n' +
    '╚═══════════════════════════════════════╝',
    'color: #00f5ff; font-family: monospace; font-size: 14px; font-weight: bold;'
);

console.log('%c60 AI Agents | 34 Skills | 25 Commands | 8 MCP Servers',
    'color: #ff006e; font-family: monospace; font-size: 12px;'
);

console.log('%cKeyboard Shortcuts: h=Home | 1-6=Navigate Pages',
    'color: #8b5cf6; font-family: monospace; font-size: 11px;'
);

/* ==========================================
   ZTL数智化作战中心 - Use Cases页面脚本
   Use Cases Page Specific JavaScript
   ========================================== */

// ==========================================
// Initialize on DOM load
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    initUseCaseWheelAnimations();
    initWorkflowAnimations();
    initOutcomesCounter();
    initScrollAnimations();
    initParallaxEffect();
    initKeyboardShortcuts();
    initScrollProgress();
    initCardHoverEffects();
    initSmoothScroll();
    initUseCaseNavigation();
});

// ==========================================
// Use Case Wheel Animations
// ==========================================
function initUseCaseWheelAnimations() {
    const wheelItems = document.querySelectorAll('.wheel-item');
    const wheelCenter = document.querySelector('.wheel-center');

    // Animate wheel items on load
    wheelItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'scale(0.5)';

        setTimeout(() => {
            item.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            item.style.opacity = '1';
            item.style.transform = 'scale(1)';
        }, 500 + index * 100);
    });

    // Center pulse animation
    if (wheelCenter) {
        wheelCenter.style.opacity = '0';
        wheelCenter.style.transform = 'translate(-50%, -50%) scale(0.8)';

        setTimeout(() => {
            wheelCenter.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            wheelCenter.style.opacity = '1';
            wheelCenter.style.transform = 'translate(-50%, -50%) scale(1)';
        }, 200);
    }

    // Add rotation animation on hover
    wheelItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.15) rotate(5deg)';
        });

        item.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1) rotate(0deg)';
        });
    });
}

// ==========================================
// Use Case Navigation from Wheel
// ==========================================
function initUseCaseNavigation() {
    const wheelItems = document.querySelectorAll('.wheel-item');

    const useCaseSections = [
        '.strategic-case',
        '.creative-case',
        '.intelligence-case',
        '.admin-case',
        '.operations-case',
        '.construction-case'
    ];

    wheelItems.forEach((item, index) => {
        item.addEventListener('click', function() {
            const targetSection = document.querySelector(useCaseSections[index]);

            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// ==========================================
// Workflow Animations
// ==========================================
function initWorkflowAnimations() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const workflowPhases = entry.target.querySelectorAll('.workflow-phase');

                workflowPhases.forEach((phase, index) => {
                    phase.style.opacity = '0';
                    phase.style.transform = 'translateY(30px)';

                    setTimeout(() => {
                        phase.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
                        phase.style.opacity = '1';
                        phase.style.transform = 'translateY(0)';
                    }, index * 150);
                });

                // Animate arrows
                const arrows = entry.target.querySelectorAll('.workflow-arrow');
                arrows.forEach((arrow, index) => {
                    arrow.style.opacity = '0';

                    setTimeout(() => {
                        arrow.style.transition = 'opacity 0.5s ease';
                        arrow.style.opacity = '1';
                    }, (index + 1) * 150 + 75);
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all workflow timelines
    const workflowTimelines = document.querySelectorAll('.workflow-timeline');
    workflowTimelines.forEach(timeline => {
        observer.observe(timeline);
    });
}

// ==========================================
// Outcomes Counter Animation
// ==========================================
function initOutcomesCounter() {
    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const outcomeMetrics = entry.target.querySelectorAll('.outcome-metric');

                outcomeMetrics.forEach(metric => {
                    const text = metric.textContent;
                    const numberMatch = text.match(/(\d+)/);

                    if (numberMatch) {
                        const targetValue = parseInt(numberMatch[1]);
                        const suffix = text.replace(numberMatch[1], '');
                        const duration = 2000;

                        animateValue(metric, 0, targetValue, duration, suffix);
                    }
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all outcomes sections
    const outcomesSections = document.querySelectorAll('.outcomes-section');
    outcomesSections.forEach(section => {
        observer.observe(section);
    });
}

function animateValue(element, start, end, duration, suffix = '') {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            current = end;
            clearInterval(timer);
        }
        element.textContent = Math.round(current) + suffix;
    }, 16);
}

// ==========================================
// Scroll Animations for All Sections
// ==========================================
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe use case sections
    const useCaseSections = document.querySelectorAll('.use-case-section');
    useCaseSections.forEach(section => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(50px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(section);
    });

    // Observe scenario cards
    const scenarioCards = document.querySelectorAll('.scenario-card');
    scenarioCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });

    // Observe benefit cards
    const benefitCards = document.querySelectorAll('.benefit-card');
    benefitCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

        setTimeout(() => {
            observer.observe(card);
        }, index * 50);
    });
}

// ==========================================
// Card Hover Effects Enhancement
// ==========================================
function initCardHoverEffects() {
    const cards = document.querySelectorAll('.scenario-card, .outcome-card, .benefit-card');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Agent tag hover effects
    const agentTags = document.querySelectorAll('.agent-tag');

    agentTags.forEach(tag => {
        tag.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
        });

        tag.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
}

// ==========================================
// Parallax Effect for Hero Section
// ==========================================
function initParallaxEffect() {
    const heroContent = document.querySelector('.hero-content');
    const useCaseWheel = document.querySelector('.use-case-wheel');

    if (heroContent && useCaseWheel) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;

            if (scrolled < window.innerHeight) {
                heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
                heroContent.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;

                useCaseWheel.style.transform = `translateY(${scrolled * 0.2}px)`;
                useCaseWheel.style.opacity = 1 - (scrolled / window.innerHeight) * 0.3;
            }
        });
    }
}

// ==========================================
// Keyboard Shortcuts
// ==========================================
function initKeyboardShortcuts() {
    document.addEventListener('keydown', function(e) {
        // Don't trigger if user is typing in an input
        if (isInputFocused()) return;

        // Press 'h' to go home
        if (e.key === 'h') {
            window.location.href = 'index.html';
        }

        // Number keys 1-6 to navigate to different use cases
        const useCaseMap = {
            '1': '.strategic-case',
            '2': '.creative-case',
            '3': '.intelligence-case',
            '4': '.admin-case',
            '5': '.operations-case',
            '6': '.construction-case'
        };

        if (useCaseMap[e.key]) {
            const section = document.querySelector(useCaseMap[e.key]);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        // Press 's' to navigate to summary section
        if (e.key === 's') {
            const summarySection = document.querySelector('.summary-section');
            if (summarySection) {
                summarySection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
}

function isInputFocused() {
    const activeElement = document.activeElement;
    return activeElement.tagName === 'INPUT' ||
           activeElement.tagName === 'TEXTAREA' ||
           activeElement.isContentEditable;
}

// ==========================================
// Scroll Progress Indicator
// ==========================================
function initScrollProgress() {
    let scrollProgressBar = document.createElement('div');
    scrollProgressBar.className = 'scroll-progress';
    scrollProgressBar.innerHTML = '<div class="scroll-progress-bar"></div>';
    document.body.appendChild(scrollProgressBar);

    window.addEventListener('scroll', function() {
        const windowHeight = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (window.pageYOffset / windowHeight) * 100;

        const progressBar = document.querySelector('.scroll-progress-bar');
        if (progressBar) {
            progressBar.style.width = scrolled + '%';
        }
    });
}

// ==========================================
// Smooth Scroll for Internal Links
// ==========================================
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            const targetId = this.getAttribute('href');
            if (targetId === '#') return;

            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// ==========================================
// Challenge Items Animation
// ==========================================
function initChallengeAnimations() {
    const observerOptions = {
        threshold: 0.3
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const challengeItems = entry.target.querySelectorAll('.challenge-item');

                challengeItems.forEach((item, index) => {
                    item.style.opacity = '0';
                    item.style.transform = 'translateX(-20px)';

                    setTimeout(() => {
                        item.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
                        item.style.opacity = '1';
                        item.style.transform = 'translateX(0)';
                    }, index * 100);
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all scenario challenges
    const scenarioChallenges = document.querySelectorAll('.scenario-challenges');
    scenarioChallenges.forEach(challenges => {
        observer.observe(challenges);
    });
}

// Initialize challenge animations
initChallengeAnimations();

// ==========================================
// Action Items Sequential Reveal
// ==========================================
function initActionItemsAnimation() {
    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const actionItems = entry.target.querySelectorAll('.action-item');

                actionItems.forEach((item, index) => {
                    item.style.opacity = '0';
                    item.style.transform = 'translateY(10px)';

                    setTimeout(() => {
                        item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                        item.style.opacity = '1';
                        item.style.transform = 'translateY(0)';
                    }, index * 80);
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all phase actions
    const phaseActions = document.querySelectorAll('.phase-actions');
    phaseActions.forEach(actions => {
        observer.observe(actions);
    });
}

// Initialize action items animation
initActionItemsAnimation();

// ==========================================
// Hero Stats Counter
// ==========================================
function initHeroStatsCounter() {
    const heroStats = document.querySelectorAll('.hero-stat-number');
    let hasAnimated = false;

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;

                heroStats.forEach(stat => {
                    const text = stat.textContent;
                    const match = text.match(/(\d+)/);

                    if (match) {
                        const targetValue = parseInt(match[1]);
                        const suffix = text.replace(match[1], '');
                        const duration = 2000;

                        animateValue(stat, 0, targetValue, duration, suffix);
                    }
                });
            }
        });
    }, observerOptions);

    const heroSection = document.querySelector('.use-cases-hero');
    if (heroSection) {
        observer.observe(heroSection);
    }
}

// Initialize hero stats counter
initHeroStatsCounter();

// ==========================================
// Console Art
// ==========================================
console.log('%c' +
    '╔═══════════════════════════════════════╗\n' +
    '║  ZTL数智化作战中心 - Use Cases       ║\n' +
    '║  6 Real-World Scenarios | 60 Agents  ║\n' +
    '╚═══════════════════════════════════════╝',
    'color: #00f5ff; font-family: monospace; font-size: 14px; font-weight: bold;'
);

console.log('%cKeyboard Shortcuts: h=Home | 1-6=Navigate Cases | s=Summary',
    'color: #8b5cf6; font-family: monospace; font-size: 11px;'
);

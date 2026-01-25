/* ==========================================
   ZTL数智化作战中心 - Skills页面脚本
   Skills Page Specific JavaScript
   ========================================== */

// ==========================================
// Initialize on DOM load
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    initExpandableCategoryLists();
    initSkillCardAnimations();
    initStatsCounter();
    initKeyboardShortcuts();
});

// ==========================================
// Expandable Category Lists
// ==========================================
function initExpandableCategoryLists() {
    const expandButtons = document.querySelectorAll('.expand-btn');

    expandButtons.forEach(button => {
        button.addEventListener('click', function() {
            const category = this.getAttribute('data-category');
            const categoryBlock = this.closest('.category-block');
            const skillsGrid = categoryBlock.querySelector('.skills-grid');
            const arrow = this.querySelector('.arrow');
            const buttonText = this.querySelector('span:first-child');

            // Toggle expanded state
            const isExpanded = skillsGrid.classList.contains('expanded');

            if (isExpanded) {
                // Collapse
                skillsGrid.classList.remove('expanded');
                arrow.textContent = '▼';
                buttonText.textContent = '展开查看';
                this.classList.remove('active');
            } else {
                // Expand
                skillsGrid.classList.add('expanded');
                arrow.textContent = '▲';
                buttonText.textContent = '收起列表';
                this.classList.add('active');

                // Animate skill cards
                animateSkillCards(skillsGrid);
            }
        });
    });
}

function animateSkillCards(skillsGrid) {
    const skillCards = skillsGrid.querySelectorAll('.skill-card');

    skillCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';

        setTimeout(() => {
            card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 50);
    });
}

// ==========================================
// Skill Card Scroll Animations
// ==========================================
function initSkillCardAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const categoryBlocks = document.querySelectorAll('.category-block');
                const blockIndex = Array.from(categoryBlocks).indexOf(entry.target);

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, blockIndex * 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all category blocks
    const categoryBlocks = document.querySelectorAll('.category-block');
    categoryBlocks.forEach(block => {
        block.style.opacity = '0';
        block.style.transform = 'translateY(50px)';
        block.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(block);
    });

    // Observe benefit cards
    const benefitCards = document.querySelectorAll('.benefit-card');
    benefitCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });

    // Observe integration cards
    const integrationCards = document.querySelectorAll('.integration-card');
    integrationCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });

    // Observe disclosure layer cards
    const layerCards = document.querySelectorAll('.layer-card');
    layerCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateX(-30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';

        setTimeout(() => {
            card.style.opacity = '1';
            card.style.transform = 'translateX(0)';
        }, index * 200);
    });
}

// ==========================================
// Stats Counter Animation
// ==========================================
function initStatsCounter() {
    const overviewCards = document.querySelectorAll('.overview-card');
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

    overviewCards.forEach(card => observer.observe(card));
}

function animateAllStats() {
    const statNumbers = document.querySelectorAll('.overview-number');

    statNumbers.forEach(stat => {
        const text = stat.textContent;
        const match = text.match(/(\d+)/);

        if (match) {
            const targetValue = parseInt(match[1]);
            const duration = 2000;

            animateValue(stat, 0, targetValue, duration);
        }
    });
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
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
    const categoryNodes = document.querySelectorAll('.skill-category-node');

    categoryNodes.forEach(node => {
        node.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.3)';
            this.style.zIndex = '20';
        });

        node.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.zIndex = '1';
        });

        node.addEventListener('click', function() {
            const category = this.classList.contains('node-meta') ? 'meta' :
                           this.classList.contains('node-workflow') ? 'workflow' :
                           this.classList.contains('node-knowledge') ? 'knowledge' :
                           'execution';

            // Scroll to category section
            const categoryBlock = document.querySelector(`.${category}-category`);
            if (categoryBlock) {
                categoryBlock.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Auto-expand the category
                setTimeout(() => {
                    const expandBtn = categoryBlock.querySelector('.expand-btn');
                    if (expandBtn && !expandBtn.classList.contains('active')) {
                        expandBtn.click();
                    }
                }, 600);
            }
        });
    });
}

// Initialize orbital system
initOrbitalSystem();

// ==========================================
// Category Hover Effects
// ==========================================
function initCategoryHoverEffects() {
    const categoryBlocks = document.querySelectorAll('.category-block');

    categoryBlocks.forEach(block => {
        block.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.category-icon');
            if (icon) {
                icon.style.transform = 'scale(1.2) rotate(10deg)';
            }
        });

        block.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.category-icon');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
}

// Initialize hover effects
initCategoryHoverEffects();

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

        // Press 'e' to expand all categories
        if (e.key === 'e') {
            expandAllCategories();
        }

        // Press 'c' to collapse all categories
        if (e.key === 'c') {
            collapseAllCategories();
        }

        // Number keys 1-6 to navigate to different sections
        const sectionMap = {
            '1': 'overview',
            '2': 'disclosure',
            '3': 'categories',
            '4': 'benefits',
            '5': 'integration'
        };

        if (sectionMap[e.key]) {
            const section = document.querySelector(`.${sectionMap[e.key]}-section`);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
}

function expandAllCategories() {
    const expandButtons = document.querySelectorAll('.expand-btn:not(.active)');
    expandButtons.forEach(button => button.click());
}

function collapseAllCategories() {
    const expandButtons = document.querySelectorAll('.expand-btn.active');
    expandButtons.forEach(button => button.click());
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

// Initialize scroll progress
initScrollProgress();

// ==========================================
// Layer Cards Animation on Scroll
// ==========================================
function initLayerCardsAnimation() {
    const layerCards = document.querySelectorAll('.layer-card');
    const observerOptions = {
        threshold: 0.3
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const cards = document.querySelectorAll('.layer-card');
                const cardIndex = Array.from(cards).indexOf(entry.target);

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                }, cardIndex * 150);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    layerCards.forEach(card => {
        observer.observe(card);
    });
}

// Initialize layer cards animation
initLayerCardsAnimation();

// ==========================================
// Skill Card Badge Hover Effects
// ==========================================
function initBadgeHoverEffects() {
    const skillCards = document.querySelectorAll('.skill-card');

    skillCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const badge = this.querySelector('.skill-badge');
            if (badge) {
                badge.style.transform = 'scale(1.1)';
            }
        });

        card.addEventListener('mouseleave', function() {
            const badge = this.querySelector('.skill-badge');
            if (badge) {
                badge.style.transform = 'scale(1)';
            }
        });
    });
}

// Initialize after a delay to ensure cards are loaded
setTimeout(initBadgeHoverEffects, 1000);

// ==========================================
// Overview Cards Stagger Animation
// ==========================================
function initOverviewCardsAnimation() {
    const overviewCards = document.querySelectorAll('.overview-card');
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const cards = document.querySelectorAll('.overview-card');
                const cardIndex = Array.from(cards).indexOf(entry.target);

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, cardIndex * 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    overviewCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}

// Initialize overview cards animation
initOverviewCardsAnimation();

// ==========================================
// Parallax Effect for Hero Section
// ==========================================
function initParallaxEffect() {
    const heroContent = document.querySelector('.hero-content');
    const orbitalSystem = document.querySelector('.skills-orbital-system');

    if (heroContent && orbitalSystem) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;

            if (scrolled < window.innerHeight) {
                heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
                heroContent.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;

                orbitalSystem.style.transform = `translateY(${scrolled * 0.2}px)`;
                orbitalSystem.style.opacity = 1 - (scrolled / window.innerHeight) * 0.3;
            }
        });
    }
}

// Initialize parallax effect
initParallaxEffect();

// ==========================================
// Console Art
// ==========================================
console.log('%c' +
    '╔═══════════════════════════════════════╗\n' +
    '║  ZTL数智化作战中心 - Skills System   ║\n' +
    '║  33 Skill Packages | 4 Categories    ║\n' +
    '╚═══════════════════════════════════════╝',
    'color: #00f5ff; font-family: monospace; font-size: 14px; font-weight: bold;'
);

console.log('%cKeyboard Shortcuts: h=Home | e=Expand All | c=Collapse All | 1-5=Navigate',
    'color: #8b5cf6; font-family: monospace; font-size: 11px;'
);

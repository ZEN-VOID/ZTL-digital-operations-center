/* ==========================================
   ZTL数智化作战中心 - Agents页面脚本
   Agents Page Specific JavaScript
   ========================================== */

// ==========================================
// Initialize on DOM load
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    initExpandableAgentLists();
    initAgentCardAnimations();
    initFlowCardAnimations();
    initKeyboardShortcuts();
});

// ==========================================
// Expandable Agent Lists
// ==========================================
function initExpandableAgentLists() {
    const expandButtons = document.querySelectorAll('.expand-btn');

    expandButtons.forEach(button => {
        button.addEventListener('click', function() {
            const groupName = this.getAttribute('data-group');
            const agentGroup = this.closest('.agent-group');
            const agentList = agentGroup.querySelector('.agent-list');
            const arrow = this.querySelector('.arrow');
            const buttonText = this.querySelector('span:first-child');

            // Toggle expanded state
            const isExpanded = agentList.classList.contains('expanded');

            if (isExpanded) {
                // Collapse
                agentList.classList.remove('expanded');
                arrow.textContent = '▼';
                buttonText.textContent = '展开查看';
                this.classList.remove('active');
            } else {
                // Expand
                agentList.classList.add('expanded');
                arrow.textContent = '▲';
                buttonText.textContent = '收起列表';
                this.classList.add('active');

                // Animate agent items
                animateAgentItems(agentList);
            }
        });
    });
}

function animateAgentItems(agentList) {
    const agentItems = agentList.querySelectorAll('.agent-item');

    agentItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateX(-20px)';

        setTimeout(() => {
            item.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            item.style.opacity = '1';
            item.style.transform = 'translateX(0)';
        }, index * 50);
    });
}

// ==========================================
// Agent Card Scroll Animations
// ==========================================
function initAgentCardAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Stagger animation delay based on position
                const agentGroups = document.querySelectorAll('.agent-group');
                const groupIndex = Array.from(agentGroups).indexOf(entry.target);

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, groupIndex * 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all agent groups
    const agentGroups = document.querySelectorAll('.agent-group');
    agentGroups.forEach(group => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(50px)';
        group.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(group);
    });
}

// ==========================================
// Flow Card Animations
// ==========================================
function initFlowCardAnimations() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('flow-visible');

                // Animate flow steps
                const flowSteps = entry.target.querySelectorAll('.flow-step');
                flowSteps.forEach((step, index) => {
                    setTimeout(() => {
                        step.style.opacity = '1';
                        step.style.transform = 'translateX(0)';
                    }, index * 200);
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all flow cards
    const flowCards = document.querySelectorAll('.flow-card');
    flowCards.forEach(card => {
        observer.observe(card);

        // Set initial state for flow steps
        const flowSteps = card.querySelectorAll('.flow-step');
        flowSteps.forEach(step => {
            step.style.opacity = '0';
            step.style.transform = 'translateX(-30px)';
            step.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });
    });
}

// ==========================================
// Overview Stats Counter Animation
// ==========================================
function initStatsCounter() {
    const statCards = document.querySelectorAll('.overview-card');
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

// Initialize stats counter
if (document.querySelector('.overview-card')) {
    initStatsCounter();
}

// ==========================================
// Agent Group Hover Effects
// ==========================================
function initAgentGroupHoverEffects() {
    const agentGroups = document.querySelectorAll('.agent-group');

    agentGroups.forEach(group => {
        group.addEventListener('mouseenter', function() {
            // Enhance glow effect on hover
            const icon = this.querySelector('.group-icon');
            if (icon) {
                icon.style.transform = 'scale(1.1) rotate(5deg)';
            }
        });

        group.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.group-icon');
            if (icon) {
                icon.style.transform = 'scale(1) rotate(0deg)';
            }
        });
    });
}

// Initialize hover effects
initAgentGroupHoverEffects();

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

        // Press 'e' to expand all agent lists
        if (e.key === 'e') {
            expandAllAgentLists();
        }

        // Press 'c' to collapse all agent lists
        if (e.key === 'c') {
            collapseAllAgentLists();
        }

        // Number keys 1-7 to navigate to different sections
        const sectionMap = {
            '1': 'overview',
            '2': 'network',
            '3': 'flows',
            '4': 'benefits'
        };

        if (sectionMap[e.key]) {
            const section = document.querySelector(`.${sectionMap[e.key]}-section`);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }
    });
}

function expandAllAgentLists() {
    const expandButtons = document.querySelectorAll('.expand-btn:not(.active)');
    expandButtons.forEach(button => button.click());
}

function collapseAllAgentLists() {
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
// Benefit Cards Animation
// ==========================================
function initBenefitCards() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const benefitCards = document.querySelectorAll('.benefit-card');
                const cardIndex = Array.from(benefitCards).indexOf(entry.target);

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, cardIndex * 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const benefitCards = document.querySelectorAll('.benefit-card');
    benefitCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}

// Initialize benefit cards
if (document.querySelector('.benefit-card')) {
    initBenefitCards();
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
// Agent Search Functionality (Future Enhancement)
// ==========================================
function initAgentSearch() {
    // This is a placeholder for future search functionality
    // Could allow users to search for specific agents by name or role
}

// ==========================================
// Console Art
// ==========================================
console.log('%c' +
    '╔═══════════════════════════════════════╗\n' +
    '║  ZTL数智化作战中心 - Agents Network  ║\n' +
    '║  60 AI Agents | 7 Business Groups    ║\n' +
    '╚═══════════════════════════════════════╝',
    'color: #00f5ff; font-family: monospace; font-size: 14px; font-weight: bold;'
);

console.log('%cKeyboard Shortcuts: h=Home | e=Expand All | c=Collapse All | 1-4=Navigate',
    'color: #8b5cf6; font-family: monospace; font-size: 11px;'
);

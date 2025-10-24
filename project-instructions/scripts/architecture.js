/* ==========================================
   ZTL数智化作战中心 - Architecture页面脚本
   Architecture Page Specific JavaScript
   ========================================== */

// ==========================================
// Initialize on DOM load
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    initPyramidInteractions();
    initLayerAnimations();
    initFlowAnimations();
    initKnowledgeAnimations();
    initCompleteFlowAnimations();
    initStatsCounter();
    initCardAnimations();
    initKeyboardShortcuts();
});

// ==========================================
// Pyramid Layer Interactions
// ==========================================
function initPyramidInteractions() {
    const pyramidLayers = document.querySelectorAll('.pyramid-layer');

    pyramidLayers.forEach((layer, index) => {
        layer.addEventListener('click', function() {
            const layerNumber = index + 1;
            const targetSection = document.querySelector(`.layer-${layerNumber}-detail`);

            if (targetSection) {
                targetSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });

        layer.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });

        layer.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

// ==========================================
// Layer Detail Section Animations
// ==========================================
function initLayerAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const layerContent = entry.target.querySelector('.layer-content');

                if (layerContent) {
                    const leftColumn = layerContent.querySelector('.layer-content > div:first-child');
                    const rightColumn = layerContent.querySelector('.layer-content > div:last-child');

                    if (leftColumn) {
                        setTimeout(() => {
                            leftColumn.style.opacity = '1';
                            leftColumn.style.transform = 'translateX(0)';
                        }, 100);
                    }

                    if (rightColumn) {
                        setTimeout(() => {
                            rightColumn.style.opacity = '1';
                            rightColumn.style.transform = 'translateX(0)';
                        }, 300);
                    }
                }

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const layerSections = document.querySelectorAll('.layer-detail-section');
    layerSections.forEach(section => {
        const layerContent = section.querySelector('.layer-content');
        if (layerContent) {
            const leftColumn = layerContent.querySelector('.layer-content > div:first-child');
            const rightColumn = layerContent.querySelector('.layer-content > div:last-child');

            if (leftColumn) {
                leftColumn.style.opacity = '0';
                leftColumn.style.transform = 'translateX(-50px)';
                leftColumn.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            }

            if (rightColumn) {
                rightColumn.style.opacity = '0';
                rightColumn.style.transform = 'translateX(50px)';
                rightColumn.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            }
        }
        observer.observe(section);
    });
}

// ==========================================
// Flow Step Animations
// ==========================================
function initFlowAnimations() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const flowSteps = entry.target.querySelectorAll('.flow-step');

                flowSteps.forEach((step, index) => {
                    setTimeout(() => {
                        step.style.opacity = '1';
                        step.style.transform = 'translateX(0)';
                    }, index * 150);
                });

                // Animate connectors
                const connectors = entry.target.querySelectorAll('.flow-connector');
                connectors.forEach((connector, index) => {
                    setTimeout(() => {
                        connector.style.opacity = '1';
                    }, (index + 1) * 150 + 75);
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const flowContainers = document.querySelectorAll('.flow-steps');
    flowContainers.forEach(container => {
        const flowSteps = container.querySelectorAll('.flow-step');
        flowSteps.forEach(step => {
            step.style.opacity = '0';
            step.style.transform = 'translateX(-30px)';
            step.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });

        const connectors = container.querySelectorAll('.flow-connector');
        connectors.forEach(connector => {
            connector.style.opacity = '0';
            connector.style.transition = 'opacity 0.3s ease';
        });

        observer.observe(container);
    });
}

// ==========================================
// Knowledge Structure Animations
// ==========================================
function initKnowledgeAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -80px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const knowledgeItems = entry.target.querySelectorAll('.knowledge-item');

                knowledgeItems.forEach((item, index) => {
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'translateX(0)';
                    }, index * 50);
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const knowledgeBranches = document.querySelectorAll('.knowledge-branch');
    knowledgeBranches.forEach(branch => {
        const knowledgeItems = branch.querySelectorAll('.knowledge-item');
        knowledgeItems.forEach(item => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-20px)';
            item.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        });

        observer.observe(branch);
    });
}

// ==========================================
// Complete Flow Animations
// ==========================================
function initCompleteFlowAnimations() {
    const observerOptions = {
        threshold: 0.15,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const flowStages = entry.target.querySelectorAll('.flow-stage');

                flowStages.forEach((stage, index) => {
                    setTimeout(() => {
                        stage.style.opacity = '1';
                        stage.style.transform = 'translateY(0)';
                    }, index * 200);
                });

                // Animate arrows between stages
                const arrows = entry.target.querySelectorAll('.flow-arrow');
                arrows.forEach((arrow, index) => {
                    setTimeout(() => {
                        arrow.style.opacity = '1';
                        arrow.style.transform = 'scale(1)';
                    }, (index + 1) * 200 + 100);
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const flowDiagram = document.querySelector('.complete-flow-diagram');
    if (flowDiagram) {
        const flowStages = flowDiagram.querySelectorAll('.flow-stage');
        flowStages.forEach(stage => {
            stage.style.opacity = '0';
            stage.style.transform = 'translateY(30px)';
            stage.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        });

        const arrows = flowDiagram.querySelectorAll('.flow-arrow');
        arrows.forEach(arrow => {
            arrow.style.opacity = '0';
            arrow.style.transform = 'scale(0.5)';
            arrow.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        });

        observer.observe(flowDiagram);
    }
}

// ==========================================
// Stats Counter Animation
// ==========================================
function initStatsCounter() {
    const statCards = document.querySelectorAll('.hero-stat');
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
    const statNumbers = document.querySelectorAll('.hero-stat-number');

    statNumbers.forEach(stat => {
        const text = stat.textContent;
        const match = text.match(/(\d+)/);

        if (match) {
            const targetValue = parseInt(match[1]);
            const duration = 2000;

            animateValue(stat, 0, targetValue, duration, text.replace(match[1], ''));
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

// ==========================================
// Card Animations (Overview, Principles, Benefits)
// ==========================================
function initCardAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const cards = entry.target.querySelectorAll('.overview-card, .principle-card, .benefit-card');

                cards.forEach((card, index) => {
                    setTimeout(() => {
                        card.style.opacity = '1';
                        card.style.transform = 'translateY(0)';
                    }, index * 100);
                });

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Overview cards
    const overviewGrid = document.querySelector('.overview-grid');
    if (overviewGrid) {
        const cards = overviewGrid.querySelectorAll('.overview-card');
        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });
        observer.observe(overviewGrid);
    }

    // Principle cards
    const principlesGrid = document.querySelector('.principles-grid');
    if (principlesGrid) {
        const cards = principlesGrid.querySelectorAll('.principle-card');
        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });
        observer.observe(principlesGrid);
    }

    // Benefit cards
    const benefitsGrid = document.querySelector('.benefits-grid');
    if (benefitsGrid) {
        const cards = benefitsGrid.querySelectorAll('.benefit-card');
        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });
        observer.observe(benefitsGrid);
    }

    // Tech stack items
    const techStackGrid = document.querySelector('.tech-stack-grid');
    if (techStackGrid) {
        const observerTech = new IntersectionObserver(function(entries) {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const techCategories = entry.target.querySelectorAll('.tech-category');

                    techCategories.forEach((category, index) => {
                        setTimeout(() => {
                            category.style.opacity = '1';
                            category.style.transform = 'translateY(0)';
                        }, index * 150);
                    });

                    observerTech.unobserve(entry.target);
                }
            });
        }, observerOptions);

        const techCategories = techStackGrid.querySelectorAll('.tech-category');
        techCategories.forEach(category => {
            category.style.opacity = '0';
            category.style.transform = 'translateY(30px)';
            category.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        });

        observerTech.observe(techStackGrid);
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

        // Number keys 1-6 to navigate to different sections
        const sectionMap = {
            '1': 'overview',
            '2': 'layer-1',
            '3': 'layer-2',
            '4': 'layer-3',
            '5': 'principles',
            '6': 'benefits'
        };

        if (sectionMap[e.key]) {
            const section = document.querySelector(`.${sectionMap[e.key]}-section, .layer-${sectionMap[e.key].replace('layer-', '')}-detail`);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
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

// Initialize scroll progress
initScrollProgress();

// ==========================================
// Parallax Effect for Hero Section
// ==========================================
function initParallaxEffect() {
    const heroContent = document.querySelector('.hero-content');
    const heroPyramid = document.querySelector('.hero-pyramid');

    if (heroContent && heroPyramid) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;

            if (scrolled < window.innerHeight) {
                heroContent.style.transform = `translateY(${scrolled * 0.3}px)`;
                heroContent.style.opacity = 1 - (scrolled / window.innerHeight) * 0.5;

                heroPyramid.style.transform = `translateY(${scrolled * 0.2}px)`;
                heroPyramid.style.opacity = 1 - (scrolled / window.innerHeight) * 0.3;
            }
        });
    }
}

// Initialize parallax effect
initParallaxEffect();

// ==========================================
// Tools Matrix Hover Enhancement
// ==========================================
function initToolsMatrixEnhancements() {
    const toolCategories = document.querySelectorAll('.tool-category');

    toolCategories.forEach(category => {
        category.addEventListener('mouseenter', function() {
            const categoryTitle = this.querySelector('.category-title');
            if (categoryTitle) {
                categoryTitle.style.color = '#a78bfa';
            }
        });

        category.addEventListener('mouseleave', function() {
            const categoryTitle = this.querySelector('.category-title');
            if (categoryTitle) {
                categoryTitle.style.color = '#ffffff';
            }
        });
    });
}

// Initialize tools matrix enhancements
if (document.querySelector('.tools-matrix')) {
    initToolsMatrixEnhancements();
}

// ==========================================
// Execution Paths Hover Effects
// ==========================================
function initExecutionPathsEffects() {
    const executionPaths = document.querySelectorAll('.execution-path');

    executionPaths.forEach(path => {
        path.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(138, 92, 246, 0.15)';
            this.style.borderColor = 'rgba(138, 92, 246, 0.5)';
        });

        path.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(255, 255, 255, 0.05)';
            this.style.borderColor = 'rgba(255, 255, 255, 0.1)';
        });
    });
}

// Initialize execution paths effects
if (document.querySelector('.execution-paths')) {
    initExecutionPathsEffects();
}

// ==========================================
// Smooth Scroll for All Internal Links
// ==========================================
function initSmoothScroll() {
    const internalLinks = document.querySelectorAll('a[href^="#"]');

    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
}

// Initialize smooth scroll
initSmoothScroll();

// ==========================================
// Console Art
// ==========================================
console.log('%c' +
    '╔═══════════════════════════════════════╗\n' +
    '║  ZTL数智化作战中心 - Architecture    ║\n' +
    '║  3 Layers | 60 Agents | 33 Skills    ║\n' +
    '╚═══════════════════════════════════════╝',
    'color: #00f5ff; font-family: monospace; font-size: 14px; font-weight: bold;'
);

console.log('%cKeyboard Shortcuts: h=Home | 1-6=Navigate Sections',
    'color: #8b5cf6; font-family: monospace; font-size: 11px;'
);

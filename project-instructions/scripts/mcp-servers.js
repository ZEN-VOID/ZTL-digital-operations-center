/* ==========================================
   ZTL数智化作战中心 - MCP Servers页面脚本
   MCP Servers Page Specific JavaScript
   ========================================== */

// ==========================================
// Initialize on DOM load
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    initNetworkVisualization();
    initStatsCounter();
    initNetworkNodeInteractions();
    initServerBlockAnimations();
    initOverviewCardAnimations();
    initBenefitsCardAnimations();
    initKeyboardShortcuts();
});

// ==========================================
// Network Visualization with SVG Lines
// ==========================================
function initNetworkVisualization() {
    const networkVisual = document.querySelector('.mcp-network-visual');
    const networkCore = document.querySelector('.network-core');
    const networkNodes = document.querySelectorAll('.network-node');

    if (!networkVisual || !networkCore || networkNodes.length === 0) return;

    // Create SVG container for connection lines
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.style.position = 'absolute';
    svg.style.top = '0';
    svg.style.left = '0';
    svg.style.width = '100%';
    svg.style.height = '100%';
    svg.style.pointerEvents = 'none';
    svg.style.zIndex = '1';
    networkVisual.insertBefore(svg, networkCore);

    // Function to draw connection lines
    function drawConnections() {
        // Clear existing lines
        svg.innerHTML = '';

        // Get core center position
        const coreRect = networkCore.getBoundingClientRect();
        const visualRect = networkVisual.getBoundingClientRect();
        const coreX = coreRect.left + coreRect.width / 2 - visualRect.left;
        const coreY = coreRect.top + coreRect.height / 2 - visualRect.top;

        // Draw line to each node
        networkNodes.forEach(node => {
            const nodeRect = node.getBoundingClientRect();
            const nodeX = nodeRect.left + nodeRect.width / 2 - visualRect.left;
            const nodeY = nodeRect.top + nodeRect.height / 2 - visualRect.top;

            // Create gradient for line
            const gradientId = `gradient-${node.classList[1]}`;
            const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
            gradient.setAttribute('id', gradientId);
            gradient.setAttribute('x1', '0%');
            gradient.setAttribute('y1', '0%');
            gradient.setAttribute('x2', '100%');
            gradient.setAttribute('y2', '0%');

            const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
            stop1.setAttribute('offset', '0%');
            stop1.setAttribute('style', 'stop-color:rgb(139, 92, 246);stop-opacity:0.6');

            const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
            stop2.setAttribute('offset', '100%');
            stop2.setAttribute('style', 'stop-color:' + window.getComputedStyle(node).color + ';stop-opacity:0.6');

            gradient.appendChild(stop1);
            gradient.appendChild(stop2);
            svg.appendChild(gradient);

            // Create line
            const line = document.createElementNS('http://www.w3.org/2000/svg', 'line');
            line.setAttribute('x1', coreX);
            line.setAttribute('y1', coreY);
            line.setAttribute('x2', nodeX);
            line.setAttribute('y2', nodeY);
            line.setAttribute('stroke', `url(#${gradientId})`);
            line.setAttribute('stroke-width', '2');
            line.setAttribute('stroke-dasharray', '5,5');
            line.style.opacity = '0.4';
            line.style.transition = 'opacity 0.3s ease';

            // Store reference to line in node
            node.connectionLine = line;

            svg.appendChild(line);
        });
    }

    // Initial draw
    drawConnections();

    // Redraw on window resize
    let resizeTimeout;
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(drawConnections, 100);
    });

    // Enhance connection on node hover
    networkNodes.forEach(node => {
        node.addEventListener('mouseenter', function() {
            if (this.connectionLine) {
                this.connectionLine.style.opacity = '1';
                this.connectionLine.setAttribute('stroke-width', '3');
            }
        });

        node.addEventListener('mouseleave', function() {
            if (this.connectionLine) {
                this.connectionLine.style.opacity = '0.4';
                this.connectionLine.setAttribute('stroke-width', '2');
            }
        });
    });
}

// ==========================================
// Stats Counter Animation
// ==========================================
function initStatsCounter() {
    const heroStats = document.querySelectorAll('.hero-stat-number');
    let hasAnimated = false;

    const observerOptions = {
        threshold: 0.5
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !hasAnimated) {
                hasAnimated = true;
                animateHeroStats();
            }
        });
    }, observerOptions);

    if (heroStats.length > 0) {
        observer.observe(heroStats[0].closest('.hero-stats'));
    }

    // Also animate overview stats
    const overviewCards = document.querySelectorAll('.overview-card');
    let overviewAnimated = false;

    const overviewObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting && !overviewAnimated) {
                overviewAnimated = true;
                animateOverviewStats();
            }
        });
    }, observerOptions);

    overviewCards.forEach(card => overviewObserver.observe(card));
}

function animateHeroStats() {
    const heroStats = document.querySelectorAll('.hero-stat-number');

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

function animateOverviewStats() {
    const overviewNumbers = document.querySelectorAll('.overview-number');

    overviewNumbers.forEach(stat => {
        const text = stat.textContent;
        const match = text.match(/(\d+)/);

        if (match) {
            const targetValue = parseInt(match[1]);
            const suffix = text.replace(match[1], '');
            const duration = 1500;

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

// ==========================================
// Network Node Interactions
// ==========================================
function initNetworkNodeInteractions() {
    const networkNodes = document.querySelectorAll('.network-node');

    networkNodes.forEach(node => {
        node.addEventListener('click', function() {
            const nodeClass = this.classList[1]; // e.g., 'node-chrome'
            const serverId = nodeClass.replace('node-', ''); // e.g., 'chrome'

            // Find corresponding server block
            const serverBlock = document.querySelector(`.${serverId}-server`);

            if (serverBlock) {
                // Scroll to server block
                serverBlock.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Highlight server block temporarily
                serverBlock.style.transform = 'translateY(-10px)';
                serverBlock.style.boxShadow = '0 20px 60px rgba(139, 92, 246, 0.4)';

                setTimeout(() => {
                    serverBlock.style.transform = '';
                    serverBlock.style.boxShadow = '';
                }, 1000);
            }
        });
    });
}

// ==========================================
// Server Block Scroll Animations
// ==========================================
function initServerBlockAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const serverBlocks = document.querySelectorAll('.server-block');
                const blockIndex = Array.from(serverBlocks).indexOf(entry.target);

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, blockIndex * 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe all server blocks
    const serverBlocks = document.querySelectorAll('.server-block');
    serverBlocks.forEach(block => {
        block.style.opacity = '0';
        block.style.transform = 'translateY(50px)';
        block.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(block);
    });
}

// ==========================================
// Overview Card Animations
// ==========================================
function initOverviewCardAnimations() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const overviewCards = document.querySelectorAll('.overview-card');
                const cardIndex = Array.from(overviewCards).indexOf(entry.target);

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }, cardIndex * 100);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const overviewCards = document.querySelectorAll('.overview-card');
    overviewCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(card);
    });
}

// ==========================================
// Benefits Card Animations
// ==========================================
function initBenefitsCardAnimations() {
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
                }, cardIndex * 150);

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

        // Number keys 1-4 to navigate to different sections
        const sectionMap = {
            '1': 'overview',
            '2': 'servers',
            '3': 'integration',
            '4': 'benefits'
        };

        if (sectionMap[e.key]) {
            const section = document.querySelector(`.${sectionMap[e.key]}-section`);
            if (section) {
                section.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        }

        // Press 's' to scroll to specific server
        if (e.key === 's') {
            const serverIds = ['chrome', 'playwright', 'context7', 'lark', 'github', 'cos', 'supabase', 'shadcn'];
            const currentScrollY = window.pageYOffset;

            // Find next server block below current position
            let nextServer = null;
            for (const serverId of serverIds) {
                const serverBlock = document.querySelector(`.${serverId}-server`);
                if (serverBlock) {
                    const serverTop = serverBlock.getBoundingClientRect().top + window.pageYOffset;
                    if (serverTop > currentScrollY + 100) {
                        nextServer = serverBlock;
                        break;
                    }
                }
            }

            // If no server below, go to first server
            if (!nextServer) {
                nextServer = document.querySelector(`.${serverIds[0]}-server`);
            }

            if (nextServer) {
                nextServer.scrollIntoView({ behavior: 'smooth', block: 'start' });
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
// Architecture Layer Animations
// ==========================================
function initArchitectureLayerAnimations() {
    const observerOptions = {
        threshold: 0.2,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                const layers = document.querySelectorAll('.architecture-layer');
                const layerIndex = Array.from(layers).indexOf(entry.target);

                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                }, layerIndex * 200);

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const architectureLayers = document.querySelectorAll('.architecture-layer');
    architectureLayers.forEach(layer => {
        layer.style.opacity = '0';
        layer.style.transform = 'translateX(-30px)';
        layer.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(layer);
    });
}

// Initialize architecture layer animations
initArchitectureLayerAnimations();

// ==========================================
// Server Badge Hover Effects
// ==========================================
function initBadgeHoverEffects() {
    const serverBlocks = document.querySelectorAll('.server-block');

    serverBlocks.forEach(block => {
        block.addEventListener('mouseenter', function() {
            const badge = this.querySelector('.server-badge');
            if (badge) {
                badge.style.transform = 'scale(1.1) translateY(-2px)';
            }
        });

        block.addEventListener('mouseleave', function() {
            const badge = this.querySelector('.server-badge');
            if (badge) {
                badge.style.transform = 'scale(1) translateY(0)';
            }
        });
    });
}

// Initialize after a delay to ensure elements are loaded
setTimeout(initBadgeHoverEffects, 1000);

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
// Network Core Rotation on Scroll
// ==========================================
function initCoreRotation() {
    const networkCore = document.querySelector('.network-core');

    if (networkCore) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rotation = scrolled * 0.1; // Slow rotation

            networkCore.style.transform = `translate(-50%, -50%) rotate(${rotation}deg)`;
        });
    }
}

// Initialize core rotation
initCoreRotation();

// ==========================================
// Console Art
// ==========================================
console.log('%c' +
    '╔═══════════════════════════════════════╗\n' +
    '║  ZTL数智化作战中心 - MCP Servers     ║\n' +
    '║  8 MCP Servers | 150+ Tools          ║\n' +
    '╚═══════════════════════════════════════╝',
    'color: #00f5ff; font-family: monospace; font-size: 14px; font-weight: bold;'
);

console.log('%cMCP服务器: chrome-mcp | playwright-mcp | context7 | lark-mcp | github-mcp | cos-mcp | supabase-mcp | shadcn-ui',
    'color: #8b5cf6; font-family: monospace; font-size: 11px;'
);

console.log('%cKeyboard Shortcuts: h=Home | s=Next Server | 1-4=Navigate Sections',
    'color: #ff006e; font-family: monospace; font-size: 11px;'
);

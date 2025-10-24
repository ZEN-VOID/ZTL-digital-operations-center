// Examples Page JavaScript
// Case Studies Navigation and Interactions

// Scroll to category section
function scrollToCategory(categoryId) {
    const section = document.getElementById(categoryId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Open case detail page
function openCaseDetail(caseId) {
    // For now, show an alert with case ID
    // In production, this would navigate to a dedicated case detail page
    console.log('Opening case detail:', caseId);

    // Future implementation: navigate to detail page
    // window.location.href = `case-detail.html?id=${caseId}`;

    // Temporary: show info
    alert(`案例详情页正在建设中\n\nCase ID: ${caseId}\n\n功能规划：\n- 完整的案例执行过程\n- 智能体协作时间线\n- 输入输出可视化\n- 关键决策点说明\n- 可下载的交付物`);
}

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scroll behavior to category cards
    const categoryCards = document.querySelectorAll('.category-card');
    categoryCards.forEach(card => {
        card.addEventListener('click', function() {
            const category = this.getAttribute('onclick').match(/'([^']+)'/)[1];
            scrollToCategory(category);
        });
    });

    // Highlight active category on scroll
    window.addEventListener('scroll', highlightActiveCategory);

    // Add hover effects to case nodes
    const caseNodes = document.querySelectorAll('.case-node');
    caseNodes.forEach((node, index) => {
        node.addEventListener('mouseenter', function() {
            this.style.animationPlayState = 'paused';
        });

        node.addEventListener('mouseleave', function() {
            this.style.animationPlayState = 'running';
        });
    });

    // Add parallax effect to orbit rings
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        const rings = document.querySelectorAll('.orbit-ring');

        rings.forEach((ring, index) => {
            const speed = 0.1 * (index + 1);
            ring.style.transform = `rotate(${scrolled * speed}deg)`;
        });
    });
});

// Highlight active category card based on scroll position
function highlightActiveCategory() {
    const sections = document.querySelectorAll('.cases-section');
    const categoryCards = document.querySelectorAll('.category-card');

    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 150;
        if (window.pageYOffset >= sectionTop) {
            currentSection = section.getAttribute('id');
        }
    });

    categoryCards.forEach(card => {
        const category = card.getAttribute('onclick')?.match(/'([^']+)'/)?.[1];
        if (category === currentSection) {
            card.style.borderColor = 'currentColor';
            card.style.transform = 'translateY(-8px)';
        } else {
            card.style.borderColor = 'rgba(0,245,255,0.2)';
            card.style.transform = 'translateY(0)';
        }
    });
}

// Filter cases by category
function filterCases(category) {
    const caseCards = document.querySelectorAll('.case-card');

    caseCards.forEach(card => {
        if (category === 'all') {
            card.style.display = 'block';
        } else {
            const tags = card.querySelectorAll('.case-tag');
            let hasCategory = false;

            tags.forEach(tag => {
                if (tag.textContent.toLowerCase().includes(category.toLowerCase())) {
                    hasCategory = true;
                }
            });

            card.style.display = hasCategory ? 'block' : 'none';
        }
    });
}

// Search cases by keyword
function searchCases(keyword) {
    const caseCards = document.querySelectorAll('.case-card');
    keyword = keyword.toLowerCase();

    caseCards.forEach(card => {
        const title = card.querySelector('.case-title').textContent.toLowerCase();
        const desc = card.querySelector('.case-desc').textContent.toLowerCase();

        if (title.includes(keyword) || desc.includes(keyword)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

// Sort cases by metric
function sortCases(metric) {
    const casesGrid = document.querySelector('.cases-grid');
    const caseCards = Array.from(document.querySelectorAll('.case-card'));

    // Sort logic based on metric
    caseCards.sort((a, b) => {
        // Featured cases first
        const aFeatured = a.classList.contains('featured');
        const bFeatured = b.classList.contains('featured');

        if (aFeatured && !bFeatured) return -1;
        if (!aFeatured && bFeatured) return 1;

        // Then by other metrics (could be enhanced)
        return 0;
    });

    // Re-append in sorted order
    caseCards.forEach(card => {
        casesGrid.appendChild(card);
    });
}

// Add CSS for active category card
const style = document.createElement('style');
style.textContent = `
    .category-card.active {
        border-color: currentColor !important;
        box-shadow: 0 12px 40px rgba(0,0,0,0.5), 0 0 40px currentColor !important;
        transform: translateY(-8px) !important;
    }
`;
document.head.appendChild(style);

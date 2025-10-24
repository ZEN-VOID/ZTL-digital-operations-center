// Output Page JavaScript
// File Management Center Interactions

console.log('✅ output.js script loading...');

// Scroll to department section
function scrollToDept(deptId) {
    const section = document.getElementById(deptId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Toggle folder expansion
function toggleFolder(element) {
    const folderItem = element.closest('.folder-item');
    if (folderItem) {
        folderItem.classList.toggle('collapsed');
    }
}

// Initialize collapsed state for some folders
document.addEventListener('DOMContentLoaded', function() {
    // Collapse all folders by default except the first few
    const folderItems = document.querySelectorAll('.folder-item');
    folderItems.forEach((item, index) => {
        if (index > 2) {
            item.classList.add('collapsed');
        }
    });

    // Add smooth scroll behavior to department cards
    const deptCards = document.querySelectorAll('.dept-card');
    deptCards.forEach(card => {
        card.addEventListener('click', function() {
            const dept = this.getAttribute('data-dept');
            scrollToDept(dept);
        });
    });

    // Highlight active department on scroll
    window.addEventListener('scroll', highlightActiveDept);
});

// Highlight active department card based on scroll position
function highlightActiveDept() {
    const sections = document.querySelectorAll('.department-section');
    const deptCards = document.querySelectorAll('.dept-card');

    let currentSection = '';

    sections.forEach(section => {
        const sectionTop = section.offsetTop - 150;
        if (window.pageYOffset >= sectionTop) {
            currentSection = section.getAttribute('id');
        }
    });

    deptCards.forEach(card => {
        card.classList.remove('active');
        if (card.getAttribute('data-dept') === currentSection) {
            card.classList.add('active');
        }
    });
}

// Add CSS for active department card
const style = document.createElement('style');
style.textContent = `
    .dept-card.active {
        border-color: rgba(0,245,255,0.8) !important;
        box-shadow: 0 8px 32px rgba(0,245,255,0.3) !important;
        transform: translateY(-4px) scale(1.02);
    }
`;
document.head.appendChild(style);

// ============================================
// Resource Filter and Search Functions
// ============================================

// Filter resources by type
function filterResources(type) {
    // Update active tab
    const filterTabs = document.querySelectorAll('.filter-tab');
    filterTabs.forEach(tab => {
        tab.classList.remove('active');
        if (tab.getAttribute('data-filter') === type) {
            tab.classList.add('active');
        }
    });

    // Filter resource items
    const resourceItems = document.querySelectorAll('.resource-item');
    resourceItems.forEach(item => {
        const resourceType = item.getAttribute('data-resource-type');

        if (type === 'all') {
            item.style.display = 'block';
        } else if (resourceType === type) {
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });

    // Also filter individual gallery items and doc items
    if (type !== 'all') {
        const galleryItems = document.querySelectorAll('.gallery-item');
        const docItems = document.querySelectorAll('.doc-item');

        galleryItems.forEach(item => {
            const itemType = item.getAttribute('data-resource-type');
            item.style.display = (itemType === type || type === 'all') ? 'block' : 'none';
        });

        docItems.forEach(item => {
            const itemType = item.getAttribute('data-resource-type');
            item.style.display = (itemType === type || type === 'all') ? 'flex' : 'none';
        });
    } else {
        // Show all individual items when 'all' is selected
        document.querySelectorAll('.gallery-item, .doc-item').forEach(item => {
            item.style.display = '';
        });
    }
}

// Search resources by filename
function searchResources(keyword) {
    const lowerKeyword = keyword.toLowerCase();

    // Search in folder names
    const folderItems = document.querySelectorAll('.folder-item');
    folderItems.forEach(item => {
        const folderName = item.querySelector('.folder-name').textContent.toLowerCase();
        item.style.display = folderName.includes(lowerKeyword) ? 'block' : 'none';
    });

    // Search in document names
    const docItems = document.querySelectorAll('.doc-item');
    docItems.forEach(item => {
        const docName = item.querySelector('.doc-name').textContent.toLowerCase();
        const parentFolder = item.closest('.folder-item');

        if (docName.includes(lowerKeyword)) {
            item.style.display = 'flex';
            // Show parent folder if child matches
            if (parentFolder) {
                parentFolder.style.display = 'block';
            }
        } else if (!keyword) {
            // Show all when search is empty
            item.style.display = 'flex';
        } else {
            item.style.display = 'none';
        }
    });

    // Search in gallery items (images)
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach(item => {
        const galleryName = item.querySelector('.gallery-name').textContent.toLowerCase();
        const parentFolder = item.closest('.folder-item');

        if (galleryName.includes(lowerKeyword)) {
            item.style.display = 'block';
            // Show parent folder if child matches
            if (parentFolder) {
                parentFolder.style.display = 'block';
            }
        } else if (!keyword) {
            // Show all when search is empty
            item.style.display = 'block';
        } else {
            item.style.display = 'none';
        }
    });

    // If search is empty, show all items
    if (!keyword) {
        folderItems.forEach(item => item.style.display = 'block');
    }
}

// ============================================
// Image Preview Modal Functions
// ============================================

// Preview image in full screen modal
function previewImage(src, title) {
    console.log('🖼️ previewImage called:', { src, title });

    // Create modal if doesn't exist
    let modal = document.getElementById('imagePreviewModal');

    if (!modal) {
        modal = document.createElement('div');
        modal.id = 'imagePreviewModal';
        modal.className = 'image-preview-modal';
        modal.innerHTML = `
            <div class="preview-close" onclick="closeImagePreview()">✕</div>
            <div class="preview-content">
                <img src="" alt="" class="preview-image" id="previewImage">
                <div class="preview-title" id="previewTitle"></div>
            </div>
        `;
        document.body.appendChild(modal);

        // Close modal on click outside image
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                closeImagePreview();
            }
        });

        // Close modal on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape' && modal.classList.contains('active')) {
                closeImagePreview();
            }
        });
    }

    // Update modal content
    document.getElementById('previewImage').src = src;
    document.getElementById('previewTitle').textContent = title;

    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

// Close image preview modal
function closeImagePreview() {
    const modal = document.getElementById('imagePreviewModal');
    if (modal) {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
    }
}

// ============================================
// Document Action Functions
// ============================================

// View document (open in new tab)
function viewDocument(path) {
    console.log('📄 viewDocument called:', path);
    // For markdown files, open in new tab
    window.open(path, '_blank');
}

// Download file
function downloadFile(path) {
    console.log('💾 downloadFile called:', path);
    // Create temporary link and trigger download
    const link = document.createElement('a');
    link.href = path;
    link.download = path.split('/').pop(); // Get filename from path
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// Verify all functions are loaded
console.log("✅ output.js fully loaded");
console.log("🔧 Available functions:", {
    scrollToDept: typeof scrollToDept,
    toggleFolder: typeof toggleFolder,
    highlightActiveDept: typeof highlightActiveDept,
    filterResources: typeof filterResources,
    searchResources: typeof searchResources,
    previewImage: typeof previewImage,
    closeImagePreview: typeof closeImagePreview,
    viewDocument: typeof viewDocument,
    downloadFile: typeof downloadFile
});


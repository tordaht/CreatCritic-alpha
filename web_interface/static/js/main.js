// CreaCritic Web Arayüzü JavaScript
// Seri No: CR-019-v1.0

document.addEventListener('DOMContentLoaded', function() {
    // DOM elementleri
    const uploadArea = document.getElementById('uploadArea');
    const fileInput = document.getElementById('fileInput');
    const uploadPreview = document.getElementById('uploadPreview');
    const fileName = document.getElementById('fileName');
    const btnRemove = document.getElementById('btnRemove');
    const btnAnalyze = document.getElementById('btnAnalyze');
    const uploadForm = document.getElementById('uploadForm');
    const loadingModal = document.getElementById('loadingModal');
    const geminiApiKey = document.getElementById('geminiApiKey');

    // API Key kaydetme ve yükleme
    function saveApiKey() {
        const apiKey = geminiApiKey.value.trim();
        if (apiKey) {
            localStorage.setItem('creacritic_api_key', apiKey);
            showFlashMessage('API Key kaydedildi!', 'success');
        }
    }

    function loadApiKey() {
        const savedApiKey = localStorage.getItem('creacritic_api_key');
        if (savedApiKey) {
            geminiApiKey.value = savedApiKey;
            showFlashMessage('Kaydedilen API Key yüklendi!', 'success');
        }
    }

    // Sayfa yüklendiğinde API Key'i yükle
    loadApiKey();

    // API Key input event - otomatik kaydet
    geminiApiKey.addEventListener('input', function() {
        const apiKey = this.value.trim();
        if (apiKey && apiKey.length > 10) { // Minimum uzunluk kontrolü
            setTimeout(saveApiKey, 1000); // 1 saniye sonra kaydet
        }
    });

    // API Key silme fonksiyonu
    window.clearApiKey = function() {
        if (confirm('Kaydedilen API Key\'i silmek istediğinizden emin misiniz?')) {
            localStorage.removeItem('creacritic_api_key');
            geminiApiKey.value = '';
            showFlashMessage('API Key silindi!', 'success');
        }
    };

    // Upload area click event
    uploadArea.addEventListener('click', function() {
        fileInput.click();
    });

    // Drag and drop events
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#5a6fd8';
        uploadArea.style.background = 'rgba(102, 126, 234, 0.1)';
    });

    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.background = 'rgba(102, 126, 234, 0.05)';
    });

    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        uploadArea.style.borderColor = '#667eea';
        uploadArea.style.background = 'rgba(102, 126, 234, 0.05)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFileSelect(files[0]);
        }
    });

    // File input change event
    fileInput.addEventListener('change', function(e) {
        if (e.target.files.length > 0) {
            handleFileSelect(e.target.files[0]);
        }
    });

    // Remove file button
    btnRemove.addEventListener('click', function() {
        removeFile();
    });

    // Form submit event
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        if (fileInput.files.length > 0) {
            showLoadingModal();
            uploadForm.submit();
        }
    });

    // File selection handler
    function handleFileSelect(file) {
        // File type validation
        const allowedTypes = ['image/png', 'image/jpeg', 'image/gif', 'image/bmp', 'application/pdf'];
        
        if (!allowedTypes.includes(file.type)) {
            showFlashMessage('Desteklenmeyen dosya formatı!', 'error');
            return;
        }

        // File size validation (10MB limit)
        if (file.size > 10 * 1024 * 1024) {
            showFlashMessage('Dosya boyutu 10MB\'dan büyük olamaz!', 'error');
            return;
        }

        // Update UI
        fileName.textContent = file.name;
        uploadArea.style.display = 'none';
        uploadPreview.style.display = 'flex';
        btnAnalyze.disabled = false;

        // Add file to form
        const dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);
        fileInput.files = dataTransfer.files;
    }

    // Remove file handler
    function removeFile() {
        fileInput.value = '';
        uploadArea.style.display = 'block';
        uploadPreview.style.display = 'none';
        btnAnalyze.disabled = true;
    }

    // Show loading modal
    function showLoadingModal() {
        loadingModal.style.display = 'block';
    }

    // Hide loading modal
    function hideLoadingModal() {
        loadingModal.style.display = 'none';
    }

    // Show flash message
    function showFlashMessage(message, type = 'success') {
        const flashContainer = document.querySelector('.flash-messages') || createFlashContainer();
        
        const flashMessage = document.createElement('div');
        flashMessage.className = `flash-message ${type}`;
        flashMessage.innerHTML = `
            <i class="fas fa-${type === 'success' ? 'check-circle' : 'exclamation-circle'}"></i>
            <span>${message}</span>
            <button class="btn-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        flashContainer.appendChild(flashMessage);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (flashMessage.parentElement) {
                flashMessage.remove();
            }
        }, 5000);
    }

    // Create flash container
    function createFlashContainer() {
        const container = document.createElement('div');
        container.className = 'flash-messages';
        document.body.appendChild(container);
        return container;
    }

    // About modal functions
    window.showAbout = function() {
        document.getElementById('aboutModal').style.display = 'block';
    };

    window.hideAbout = function() {
        document.getElementById('aboutModal').style.display = 'none';
    };

    // Close modals when clicking outside
    window.addEventListener('click', function(e) {
        const aboutModal = document.getElementById('aboutModal');
        const loadingModal = document.getElementById('loadingModal');
        
        if (e.target === aboutModal) {
            aboutModal.style.display = 'none';
        }
        
        if (e.target === loadingModal) {
            loadingModal.style.display = 'none';
        }
    });

    // Smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add active class to current nav link
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Animate elements on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // Add typing animation to hero title
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle) {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        
        let i = 0;
        const typeWriter = () => {
            if (i < text.length) {
                heroTitle.textContent += text.charAt(i);
                i++;
                setTimeout(typeWriter, 100);
            }
        };
        
        // Start typing animation after 1 second
        setTimeout(typeWriter, 1000);
    }

    // Add particle effect to hero section
    createParticles();

    // Console log for debugging
    console.log('CreaCritic Web Arayüzü Yüklendi');
    console.log('Seri No: CR-019-v1.0');
});

// Particle effect function
function createParticles() {
    const hero = document.querySelector('.hero');
    if (!hero) return;

    for (let i = 0; i < 50; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.cssText = `
            position: absolute;
            width: 2px;
            height: 2px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 50%;
            pointer-events: none;
            animation: float ${Math.random() * 3 + 2}s linear infinite;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
        `;
        hero.appendChild(particle);
    }

    // Add CSS animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0% {
                transform: translateY(0px) rotate(0deg);
                opacity: 1;
            }
            100% {
                transform: translateY(-100px) rotate(360deg);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// API functions for future use
const CreaCriticAPI = {
    async analyzeFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('API hatası');
            }

            return await response.json();
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    async getHistory() {
        try {
            const response = await fetch('/api/history');
            return await response.json();
        } catch (error) {
            console.error('History Error:', error);
            throw error;
        }
    }
};

// Export for global use
window.CreaCriticAPI = CreaCriticAPI; 
// JavaScript de base pour l'application Flask

// Fonction utilitaire pour faire des requêtes AJAX
async function fetchAPI(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        return await response.json();
    } catch (error) {
        console.error('Erreur API:', error);
        throw error;
    }
}

// Fonction pour afficher les messages d'alerte
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.textContent = message;
    
    // Insérer au début du contenu principal
    const main = document.querySelector('.main') || document.body;
    main.insertBefore(alertDiv, main.firstChild);
    
    // Supprimer automatiquement après 5 secondes
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Fonction pour afficher/masquer le loader
function showLoading(show = true) {
    let loader = document.querySelector('.loading');
    
    if (show && !loader) {
        loader = document.createElement('div');
        loader.className = 'loading';
        loader.textContent = 'Chargement...';
        document.body.appendChild(loader);
    } else if (!show && loader) {
        loader.remove();
    }
}

// Fonction pour formater les nombres
function formatNumber(num, decimals = 2) {
    if (num === null || num === undefined) return '-';
    return Number(num).toLocaleString('fr-FR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    });
}

// Fonction pour formater les pourcentages
function formatPercentage(num, decimals = 2) {
    if (num === null || num === undefined) return '-';
    return `${Number(num * 100).toFixed(decimals)}%`;
}

// Fonction pour formater les dates
function formatDate(dateString) {
    if (!dateString) return '-';
    const date = new Date(dateString);
    return date.toLocaleDateString('fr-FR');
}

// Fonction pour vérifier si une icône Lucide est rendue
function isIconRendered(element) {
    // Vérifier si l'élément a du contenu SVG (directement ou dans un enfant)
    const svg = element.querySelector('svg') || element.querySelector('path') || element.querySelector('circle');
    if (svg) return true;
    
    // Vérifier si l'élément a des attributs SVG
    if (element.getAttribute('viewBox') || element.getAttribute('d')) return true;
    
    // Vérifier si l'élément a du contenu HTML (icône rendue)
    if (element.innerHTML && element.innerHTML.trim() !== '') return true;
    
    return false;
}

// Fonction pour initialiser les icônes Lucide avec retry
function initLucideIcons() {
    console.log('Tentative d\'initialisation des icônes Lucide...');
    
    if (window.lucide) {
        console.log('Lucide disponible, initialisation...');
        lucide.createIcons();
        
        // Vérifier si les icônes ont été rendues
        setTimeout(() => {
            const iconElements = document.querySelectorAll('[data-lucide]');
            let missingIcons = 0;
            
            iconElements.forEach(element => {
                const iconName = element.getAttribute('data-lucide');
                if (isIconRendered(element)) {
                    console.log(`✓ Icône "${iconName}" rendue avec succès`);
                } else {
                    missingIcons++;
                    console.warn(`Icône "${iconName}" non trouvée`);
                }
            });
            
            if (missingIcons > 0) {
                console.log(`${missingIcons} icône(s) manquante(s), nouvelle tentative...`);
                setTimeout(initLucideIcons, 500);
            } else {
                console.log('Toutes les icônes Lucide ont été initialisées avec succès');
            }
        }, 200);
    } else {
        console.log('Lucide non disponible, nouvelle tentative dans 100ms...');
        setTimeout(initLucideIcons, 100);
    }
}

// Fonction pour valider les formulaires
function validateForm(formElement) {
    const inputs = formElement.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            isValid = false;
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

// Fonction pour gérer les erreurs AJAX
function handleAjaxError(error) {
    console.error('Erreur AJAX:', error);
    showAlert('Une erreur est survenue. Veuillez réessayer.', 'error');
}

// Fonction pour initialiser l'application
function initApp() {
    console.log('Application Flask initialisée');
    
    // Initialiser les icônes Lucide
    initLucideIcons();
    
    // Code d'initialisation spécifique à chaque page
    const currentPage = document.body.dataset.page;
    
    switch(currentPage) {
        case 'dashboard':
            initDashboard();
            break;
        case 'options':
            initOptionsCalculator();
            break;
        case 'volatility':
            initVolatilitySurface();
            break;
        default:
            // Page par défaut
            break;
    }
}

// Fonctions spécifiques aux pages (à implémenter selon les besoins)
function initDashboard() {
    // Initialisation du dashboard
    console.log('Dashboard initialisé');
    
    // Effets spéciaux pour le rectangle de texte
    initTextRectangleEffects();
}

function initTextRectangleEffects() {
    const textRectangle = document.querySelector('.text-rectangle');
    if (!textRectangle) return;
    
    // Effet de particules flottantes
    createFloatingParticles(textRectangle);
    
    // Effet de pulsation subtile
    addPulseEffect(textRectangle);
    
    // Effet de hover avec rotation 3D
    add3DHoverEffect(textRectangle);
}

function createFloatingParticles(container) {
    const particles = ['✨', '💫', '⭐', '🌟', '💎', '🔮'];
    const numParticles = 6;
    
    for (let i = 0; i < numParticles; i++) {
        const particle = document.createElement('div');
        particle.className = 'floating-particle';
        particle.textContent = particles[i % particles.length];
        particle.style.cssText = `
            position: absolute;
            font-size: 12px;
            opacity: 0.3;
            pointer-events: none;
            z-index: 0;
            animation: float ${3 + Math.random() * 4}s ease-in-out infinite;
            animation-delay: ${Math.random() * 2}s;
            left: ${Math.random() * 100}%;
            top: ${Math.random() * 100}%;
        `;
        container.appendChild(particle);
    }
    
    // Ajouter le CSS pour l'animation
    if (!document.querySelector('#particle-styles')) {
        const style = document.createElement('style');
        style.id = 'particle-styles';
        style.textContent = `
            @keyframes float {
                0%, 100% { transform: translateY(0px) rotate(0deg); opacity: 0.3; }
                50% { transform: translateY(-20px) rotate(180deg); opacity: 0.6; }
            }
            
            .floating-particle {
                transition: all 0.3s ease;
            }
            
            .text-rectangle:hover .floating-particle {
                opacity: 0.8;
                transform: scale(1.2);
            }
        `;
        document.head.appendChild(style);
    }
}

function addPulseEffect(container) {
    container.style.animation = 'subtle-pulse 4s ease-in-out infinite';
    
    if (!document.querySelector('#pulse-styles')) {
        const style = document.createElement('style');
        style.id = 'pulse-styles';
        style.textContent = `
            @keyframes subtle-pulse {
                0%, 100% { box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.1), inset 0 1px 0 rgba(255, 255, 255, 0.1); }
                50% { box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.15), inset 0 1px 0 rgba(255, 255, 255, 0.15); }
            }
        `;
        document.head.appendChild(style);
    }
}

function add3DHoverEffect(container) {
    container.addEventListener('mousemove', (e) => {
        const rect = container.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        
        const rotateX = (y - centerY) / 10;
        const rotateY = (centerX - x) / 10;
        
        container.style.transform = `translateY(-2px) perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
    });
    
    container.addEventListener('mouseleave', () => {
        container.style.transform = 'translateY(0px) perspective(1000px) rotateX(0deg) rotateY(0deg)';
    });
}

function initOptionsCalculator() {
    // Initialisation du calculateur d'options
    console.log('Calculateur d\'options initialisé');
}

function initVolatilitySurface() {
    // Initialisation de la surface de volatilité
    console.log('Surface de volatilité initialisée');
}

// Initialiser l'application quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    // Le DOM est déjà chargé, initialiser immédiatement
    initApp();
}

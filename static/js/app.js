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

// Fonction pour afficher les messages d'alerte (désactivée)
function showAlert(message, type = 'info') {
    // Bannières en haut désactivées - ne rien faire
    console.log(`Alert (${type}): ${message}`);
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
    
    // Initialiser les volatility smiles si on est sur la page volatility
    if (currentPage === 'volatility_surface') {
        initVolatilitySmileListeners();
        initTermStructureListeners();
        // Charger automatiquement les symboles au chargement de la page
        loadPopularSymbols();
        loadTermPopularSymbols();
        console.log('Page de volatilité implicite chargée - symboles chargés automatiquement');
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


// Fonction pour gérer le menu déroulant
function toggleDropdown(event) {
    event.preventDefault();
    
    const dropdownToggle = event.currentTarget;
    const dropdown = dropdownToggle.closest('.nav-item.dropdown');
    const dropdownMenu = dropdown.querySelector('.dropdown-menu');
    
    // Fermer tous les autres menus déroulants
    const allDropdowns = document.querySelectorAll('.nav-item.dropdown');
    allDropdowns.forEach(item => {
        if (item !== dropdown) {
            const menu = item.querySelector('.dropdown-menu');
            const toggle = item.querySelector('.dropdown-toggle');
            if (menu && toggle) {
                menu.classList.remove('show');
                toggle.classList.remove('active');
            }
        }
    });
    
    // Toggle le menu actuel
    if (dropdownMenu) {
        dropdownMenu.classList.toggle('show');
        dropdownToggle.classList.toggle('active');
    }
}

// Fermer le menu déroulant quand on clique ailleurs
document.addEventListener('click', function(event) {
    const dropdown = event.target.closest('.nav-item.dropdown');
    if (!dropdown) {
        // Fermer tous les menus déroulants
        const allDropdowns = document.querySelectorAll('.nav-item.dropdown');
        allDropdowns.forEach(item => {
            const menu = item.querySelector('.dropdown-menu');
            const toggle = item.querySelector('.dropdown-toggle');
            if (menu && toggle) {
                menu.classList.remove('show');
                toggle.classList.remove('active');
            }
        });
    }
});

// ===== LOGIQUE POUR VOLATILITY SMILES (TRADIER) =====

// Variables globales pour les volatility smiles
let selectedTickers = new Set();
let tickerMaturities = new Map(); // Map<ticker, Set<maturities>>
let selectedCombinations = new Map(); // Map<`${ticker}-${maturity}`, {ticker, maturity, status}>

// Variables globales pour les term structures
let termSelectedTickers = new Set();
let termTickerMaturities = new Map(); // Map<ticker, Set<maturities>>
let termSelectedCombinations = new Map(); // Map<`${ticker}-${maturity}`, {ticker, maturity, status}>

// Fonction pour charger les symboles populaires
async function loadPopularSymbols() {
    try {
        console.log('Chargement des symboles populaires...');
        const response = await fetchAPI('/api/tradier/symbols');
        if (response.success) {
            populateSymbolSelect(response.symbols);
            console.log(`${response.symbols.length} symboles chargés`);
        } else {
            console.error('Erreur lors du chargement des symboles:', response.error);
        }
    } catch (error) {
        console.error('Erreur lors du chargement des symboles:', error);
    }
}

// Fonction pour charger les symboles populaires pour Term Structure
async function loadTermPopularSymbols() {
    try {
        console.log('Chargement des symboles populaires pour Term Structure...');
        const response = await fetchAPI('/api/tradier/symbols');
        if (response.success) {
            populateTermSymbolSelect(response.symbols);
            console.log(`${response.symbols.length} symboles chargés pour Term Structure`);
        } else {
            console.error('Erreur lors du chargement des symboles:', response.error);
        }
    } catch (error) {
        console.error('Erreur lors du chargement des symboles:', error);
    }
}

// Fonction pour peupler le select des symboles
function populateSymbolSelect(symbols) {
    const select = document.getElementById('smile-ticker-select');
    if (!select) return;
    
    // Vider le select (garder la première option)
    select.innerHTML = '<option value="">Select a ticker to add...</option>';
    
    // Ajouter les symboles (filtrer ceux déjà sélectionnés)
    symbols.forEach(symbol => {
        if (!selectedTickers.has(symbol.symbol)) {
            const option = document.createElement('option');
            option.value = symbol.symbol;
            option.textContent = `${symbol.symbol} - ${symbol.name}`;
            select.appendChild(option);
        }
    });
}

// Fonction pour peupler le select des symboles pour Term Structure
function populateTermSymbolSelect(symbols) {
    const select = document.getElementById('term-ticker-select');
    if (!select) return;
    
    // Vider le select (garder la première option)
    select.innerHTML = '<option value="">Select a ticker to add...</option>';
    
    // Ajouter les symboles (filtrer ceux déjà sélectionnés)
    symbols.forEach(symbol => {
        if (!termSelectedTickers.has(symbol.symbol)) {
            const option = document.createElement('option');
            option.value = symbol.symbol;
            option.textContent = `${symbol.symbol} - ${symbol.name}`;
            select.appendChild(option);
        }
    });
}

// Fonction pour ajouter un ticker
async function addTicker(symbol) {
    if (selectedTickers.has(symbol)) {
        showAlert('Ce ticker est déjà sélectionné', 'warning');
        return;
    }
    
    try {
        // Charger les maturités pour ce ticker
        const response = await fetchAPI(`/api/tradier/expirations/${symbol}`);
        if (response.success) {
            selectedTickers.add(symbol);
            tickerMaturities.set(symbol, response.expirations);
            
            // Mettre à jour l'affichage
            updateSelectedTickersDisplay();
            updateSelectionsTable();
            updateButtons();
            
            // Réinitialiser le select
            const select = document.getElementById('smile-ticker-select');
            if (select) {
                select.value = '';
            }
            
            showAlert(`Ticker ${symbol} ajouté avec ${response.expirations.length} maturités`, 'success');
        } else {
            showAlert(`Erreur lors du chargement des maturités pour ${symbol}: ${response.error}`, 'error');
        }
    } catch (error) {
        console.error('Erreur lors du chargement des maturités:', error);
        showAlert('Erreur lors du chargement des maturités', 'error');
    }
}

// Fonction pour ajouter un ticker pour Term Structure
async function addTermTicker(symbol) {
    if (termSelectedTickers.has(symbol)) {
        showAlert('Ce ticker est déjà sélectionné', 'warning');
        return;
    }
    
    try {
        // Charger les maturités pour ce ticker
        const response = await fetchAPI(`/api/tradier/expirations/${symbol}`);
        if (response.success) {
            termSelectedTickers.add(symbol);
            termTickerMaturities.set(symbol, response.expirations);
            
            // Mettre à jour l'affichage
            updateTermSelectedTickersDisplay();
            updateTermSelectionsTable();
            updateTermButtons();
            
            // Réinitialiser le select
            const select = document.getElementById('term-ticker-select');
            if (select) {
                select.value = '';
            }
            
            showAlert(`Ticker ${symbol} ajouté avec ${response.expirations.length} maturités`, 'success');
        } else {
            showAlert(`Erreur lors du chargement des maturités pour ${symbol}: ${response.error}`, 'error');
        }
    } catch (error) {
        console.error('Erreur lors du chargement des maturités:', error);
        showAlert('Erreur lors du chargement des maturités', 'error');
    }
}

// Fonction pour supprimer un ticker
function removeTicker(symbol) {
    selectedTickers.delete(symbol);
    tickerMaturities.delete(symbol);
    
    // Supprimer toutes les combinaisons de ce ticker
    for (const [key, combination] of selectedCombinations.entries()) {
        if (combination.ticker === symbol) {
            selectedCombinations.delete(key);
        }
    }
    
    // Mettre à jour l'affichage
    updateSelectedTickersDisplay();
    updateSelectionsTable();
    updateButtons();
    populateSymbolSelect([]); // Recharger les options disponibles
    
    showAlert(`Ticker ${symbol} supprimé`, 'info');
}

// Fonction pour supprimer un ticker pour Term Structure
function removeTermTicker(symbol) {
    termSelectedTickers.delete(symbol);
    termTickerMaturities.delete(symbol);
    
    // Supprimer toutes les combinaisons de ce ticker
    for (const [key, combination] of termSelectedCombinations.entries()) {
        if (combination.ticker === symbol) {
            termSelectedCombinations.delete(key);
        }
    }
    
    // Mettre à jour l'affichage
    updateTermSelectedTickersDisplay();
    updateTermSelectionsTable();
    updateTermButtons();
    populateTermSymbolSelect([]); // Recharger les options disponibles
    
    showAlert(`Ticker ${symbol} supprimé`, 'info');
}

// Fonction pour mettre à jour l'affichage des tickers sélectionnés
function updateSelectedTickersDisplay() {
    const container = document.getElementById('selected-tickers');
    const countBadge = document.getElementById('ticker-count');
    if (!container) return;
    
    if (selectedTickers.size === 0) {
        container.innerHTML = `
            <div class="empty-tickers">
                <i data-lucide="building-2" class="empty-icon"></i>
                <span>No tickers selected yet</span>
            </div>
        `;
        if (countBadge) countBadge.textContent = '0';
    } else {
        container.innerHTML = '';
        selectedTickers.forEach(symbol => {
            const chip = document.createElement('div');
            chip.className = 'ticker-chip';
            chip.innerHTML = `
                <span>${symbol}</span>
                <button class="remove-btn" onclick="removeTicker('${symbol}')" title="Remove ${symbol}">
                    <i data-lucide="x"></i>
                </button>
            `;
            container.appendChild(chip);
        });
        if (countBadge) countBadge.textContent = selectedTickers.size.toString();
    }
    
    // Réinitialiser les icônes Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Fonction pour mettre à jour l'affichage des tickers sélectionnés pour Term Structure
function updateTermSelectedTickersDisplay() {
    const container = document.getElementById('term-selected-tickers');
    const countBadge = document.getElementById('term-ticker-count');
    if (!container) return;
    
    if (termSelectedTickers.size === 0) {
        container.innerHTML = `
            <div class="empty-tickers">
                <i data-lucide="building-2" class="empty-icon"></i>
                <span>No tickers selected yet</span>
            </div>
        `;
        if (countBadge) countBadge.textContent = '0';
    } else {
        container.innerHTML = '';
        termSelectedTickers.forEach(symbol => {
            const chip = document.createElement('div');
            chip.className = 'ticker-chip';
            chip.innerHTML = `
                <span>${symbol}</span>
                <button class="remove-btn" onclick="removeTermTicker('${symbol}')" title="Remove ${symbol}">
                    <i data-lucide="x"></i>
                </button>
            `;
            container.appendChild(chip);
        });
        if (countBadge) countBadge.textContent = termSelectedTickers.size.toString();
    }
    
    // Réinitialiser les icônes Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Fonction pour mettre à jour le tableau des sélections
function updateSelectionsTable() {
    const table = document.getElementById('selections-table');
    const countBadge = document.getElementById('combination-count');
    if (!table) return;
    
    if (selectedTickers.size === 0) {
        table.innerHTML = `
            <div class="empty-combinations">
                <div class="empty-content">
                    <i data-lucide="layers" class="empty-icon"></i>
                    <h4>No tickers selected</h4>
                    <p>Add tickers to see available maturities and create combinations</p>
                </div>
            </div>
        `;
        if (countBadge) countBadge.textContent = '0';
    } else {
        table.innerHTML = '';
        
        // Créer les en-têtes du tableau
        const headerRow = document.createElement('div');
        headerRow.className = 'table-row';
        headerRow.style.borderBottom = '2px solid rgba(75, 85, 99, 0.5)';
        headerRow.style.fontWeight = '600';
        headerRow.style.background = 'rgba(17, 24, 39, 0.8)';
        headerRow.innerHTML = `
            <div class="table-cell">Ticker</div>
            <div class="table-cell">Available Maturities</div>
            <div class="table-cell">Selected Combinations</div>
            <div class="table-cell">Actions</div>
        `;
        table.appendChild(headerRow);
        
        // Ajouter les lignes pour chaque ticker
        selectedTickers.forEach(ticker => {
            const maturities = tickerMaturities.get(ticker) || [];
            const tickerCombinations = Array.from(selectedCombinations.values()).filter(c => c.ticker === ticker);
            
            const row = document.createElement('div');
            row.className = 'table-row';
            
            // Créer la liste déroulante des maturités disponibles
            const maturitiesList = `
                <select class="maturity-select" data-ticker="${ticker}" onchange="selectMaturity('${ticker}', this.value)">
                    <option value="">Select a maturity...</option>
                    ${maturities.map(maturity => {
                        const isSelected = tickerCombinations.some(c => c.maturity === maturity.date);
                        return `<option value="${maturity.date}" ${isSelected ? 'disabled' : ''}>
                            ${maturity.date} (${maturity.days_to_exp} days) - ${maturity.type}
                        </option>`;
                    }).join('')}
                </select>
            `;
            
            // Créer la liste des combinaisons sélectionnées
            const combinationsList = tickerCombinations.map(combination => {
                return `
                    <div class="combination-item">
                        <span class="combination-text">${combination.maturity}</span>
                        <span class="status-badge ${combination.status}">${combination.status}</span>
                        <button class="remove-combination-btn" onclick="removeCombination('${ticker}-${combination.maturity}')" title="Remove combination">
                            <i data-lucide="x"></i>
                        </button>
                    </div>
                `;
            }).join('');
            
            row.innerHTML = `
                <div class="table-cell ticker">${ticker}</div>
                <div class="table-cell maturities-cell">
                    <div class="maturities-list">
                        ${maturitiesList || '<span class="no-data">No maturities available</span>'}
                    </div>
                </div>
                <div class="table-cell combinations-cell">
                    <div class="combinations-list">
                        ${combinationsList || '<span class="no-data">No combinations selected</span>'}
                    </div>
                </div>
                <div class="table-cell">
                    <button class="remove-row-btn" onclick="removeTicker('${ticker}')" title="Remove ticker">
                        <i data-lucide="trash-2"></i>
                    </button>
                </div>
            `;
            table.appendChild(row);
        });
        
        if (countBadge) countBadge.textContent = selectedCombinations.size.toString();
    }
    
    // Réinitialiser les icônes Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Fonction pour mettre à jour le tableau des sélections pour Term Structure
function updateTermSelectionsTable() {
    const table = document.getElementById('term-selections-table');
    const countBadge = document.getElementById('term-combination-count');
    if (!table) return;
    
    if (termSelectedTickers.size === 0) {
        table.innerHTML = `
            <div class="empty-combinations">
                <div class="empty-content">
                    <i data-lucide="layers" class="empty-icon"></i>
                    <h4>No tickers selected</h4>
                    <p>Add tickers to see available maturities and create combinations</p>
                </div>
            </div>
        `;
        if (countBadge) countBadge.textContent = '0';
    } else {
        table.innerHTML = '';
        
        // Ajouter les lignes pour chaque ticker
        termSelectedTickers.forEach(ticker => {
            const maturities = termTickerMaturities.get(ticker) || [];
            const tickerCombinations = Array.from(termSelectedCombinations.values()).filter(c => c.ticker === ticker);
            
            const row = document.createElement('tr');
            
            // Créer la liste déroulante des maturités disponibles
            const maturitiesList = `
                <select class="maturity-select" data-ticker="${ticker}" onchange="selectTermMaturity('${ticker}', this.value)">
                    <option value="">Select a maturity...</option>
                    ${maturities.map(maturity => {
                        const isSelected = tickerCombinations.some(c => c.maturity === maturity.date);
                        return `<option value="${maturity.date}" ${isSelected ? 'disabled' : ''}>
                            ${maturity.date} (${maturity.days_to_exp} days) - ${maturity.type}
                        </option>`;
                    }).join('')}
                </select>
            `;
            
            // Créer la liste des combinaisons sélectionnées
            const combinationsList = tickerCombinations.map(combination => {
                return `
                    <div class="combination-item">
                        <span class="combination-text">${combination.maturity}</span>
                        <span class="status-badge ${combination.status}">${combination.status}</span>
                        <button class="remove-combination-btn" onclick="removeTermCombination('${ticker}-${combination.maturity}')" title="Remove combination">
                            <i data-lucide="x"></i>
                        </button>
                    </div>
                `;
            }).join('');
            
            row.innerHTML = `
                <td class="ticker-cell">
                    <span class="ticker-display">${ticker}</span>
                </td>
                <td class="maturity-cell">
                    <div class="maturity-dropdown-container">
                        ${maturitiesList || '<span class="no-data">No maturities available</span>'}
                    </div>
                </td>
                <td class="combinations-cell">
                    <div class="tickers-container">
                        ${combinationsList || '<div class="empty-combinations"><div class="empty-content"><i data-lucide="layers" class="empty-icon"></i><h4>No maturity selected yet</h4><p>Select a maturity to create combinations</p></div></div>'}
                    </div>
                </td>
            `;
            table.appendChild(row);
        });
        
        if (countBadge) countBadge.textContent = termSelectedCombinations.size.toString();
    }
    
    // Réinitialiser les icônes Lucide
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Fonction pour sélectionner une maturité depuis la liste déroulante
function selectMaturity(ticker, maturity) {
    if (maturity && maturity !== '') {
        addCombination(ticker, maturity);
        // Réinitialiser le select
        const select = document.querySelector(`select[data-ticker="${ticker}"]`);
        if (select) {
            select.value = '';
        }
    }
}

// Fonction pour sélectionner une maturité depuis la liste déroulante pour Term Structure
function selectTermMaturity(ticker, maturity) {
    if (maturity && maturity !== '') {
        addTermCombination(ticker, maturity);
        // Réinitialiser le select
        const select = document.querySelector(`select[data-ticker="${ticker}"]`);
        if (select) {
            select.value = '';
        }
    }
}

// Fonction pour basculer la sélection d'une maturité (gardée pour compatibilité)
function toggleMaturity(ticker, maturity) {
    const key = `${ticker}-${maturity}`;
    
    if (selectedCombinations.has(key)) {
        removeCombination(key);
    } else {
        addCombination(ticker, maturity);
    }
}

// Fonction pour ajouter une combinaison ticker-maturité
function addCombination(ticker, maturity) {
    const key = `${ticker}-${maturity}`;
    if (selectedCombinations.has(key)) {
        showAlert('Cette combinaison est déjà sélectionnée', 'warning');
        return;
    }
    
    selectedCombinations.set(key, {
        ticker: ticker,
        maturity: maturity,
        status: 'ready'
    });
    
    updateSelectionsTable();
    updateButtons();
    updateMaturitySelects();
    
    showAlert(`Combinaison ${ticker} - ${maturity} ajoutée`, 'success');
}

// Fonction pour ajouter une combinaison ticker-maturité pour Term Structure
function addTermCombination(ticker, maturity) {
    const key = `${ticker}-${maturity}`;
    if (termSelectedCombinations.has(key)) {
        showAlert('Cette combinaison est déjà sélectionnée', 'warning');
        return;
    }
    
    termSelectedCombinations.set(key, {
        ticker: ticker,
        maturity: maturity,
        status: 'ready'
    });
    
    updateTermSelectionsTable();
    updateTermButtons();
    updateTermMaturitySelects();
    
    showAlert(`Combinaison ${ticker} - ${maturity} ajoutée`, 'success');
}

// Fonction pour supprimer une combinaison
function removeCombination(key) {
    const combination = selectedCombinations.get(key);
    if (combination) {
        selectedCombinations.delete(key);
        updateSelectionsTable();
        updateButtons();
        updateMaturitySelects();
        showAlert(`Combinaison ${combination.ticker} - ${combination.maturity} supprimée`, 'info');
    }
}

// Fonction pour supprimer une combinaison pour Term Structure
function removeTermCombination(key) {
    const combination = termSelectedCombinations.get(key);
    if (combination) {
        termSelectedCombinations.delete(key);
        updateTermSelectionsTable();
        updateTermButtons();
        updateTermMaturitySelects();
        showAlert(`Combinaison ${combination.ticker} - ${combination.maturity} supprimée`, 'info');
    }
}

// Fonction pour mettre à jour les selects de maturités
function updateMaturitySelects() {
    selectedTickers.forEach(ticker => {
        const select = document.querySelector(`select[data-ticker="${ticker}"]`);
        if (select) {
            const tickerCombinations = Array.from(selectedCombinations.values()).filter(c => c.ticker === ticker);
            const options = select.querySelectorAll('option');
            
            options.forEach(option => {
                if (option.value !== '') {
                    const isSelected = tickerCombinations.some(c => c.maturity === option.value);
                    option.disabled = isSelected;
                    option.style.color = isSelected ? '#6b7280' : '#ffffff';
                }
            });
        }
    });
}

// Fonction pour mettre à jour les selects de maturités pour Term Structure
function updateTermMaturitySelects() {
    termSelectedTickers.forEach(ticker => {
        const select = document.querySelector(`select[data-ticker="${ticker}"]`);
        if (select) {
            const tickerCombinations = Array.from(termSelectedCombinations.values()).filter(c => c.ticker === ticker);
            const options = select.querySelectorAll('option');
            
            options.forEach(option => {
                if (option.value !== '') {
                    const isSelected = tickerCombinations.some(c => c.maturity === option.value);
                    option.disabled = isSelected;
                    option.style.color = isSelected ? '#6b7280' : '#ffffff';
                }
            });
        }
    });
}

// Fonction pour vider toutes les sélections
function clearAllSelections() {
    selectedTickers.clear();
    tickerMaturities.clear();
    selectedCombinations.clear();
    
    updateSelectedTickersDisplay();
    updateSelectionsTable();
    updateButtons();
    loadPopularSymbols();
    
    showAlert('Toutes les sélections ont été supprimées', 'info');
}

// Fonction pour vider toutes les sélections pour Term Structure
function clearAllTermSelections() {
    termSelectedTickers.clear();
    termTickerMaturities.clear();
    termSelectedCombinations.clear();
    
    updateTermSelectedTickersDisplay();
    updateTermSelectionsTable();
    updateTermButtons();
    loadTermPopularSymbols();
    
    showAlert('Toutes les sélections ont été supprimées', 'info');
}

// Fonction pour générer les volatility smiles
async function generateVolatilitySmiles() {
    if (selectedCombinations.size === 0) {
        showAlert('Veuillez sélectionner au moins une combinaison ticker-maturité', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        // Marquer toutes les combinaisons comme "loading"
        selectedCombinations.forEach((combination, key) => {
            combination.status = 'loading';
        });
        updateSelectionsTable();
        
        // Récupérer les données pour chaque combinaison
        const promises = [];
        const results = new Map();
        
        for (const [key, combination] of selectedCombinations.entries()) {
            const promise = fetchAPI(`/api/tradier/options/${combination.ticker}/${combination.maturity}`)
                .then(response => {
                    if (response.success) {
                        results.set(key, {
                            ticker: combination.ticker,
                            maturity: combination.maturity,
                            options: response.options,
                            status: 'ready'
                        });
                    } else {
                        results.set(key, {
                            ticker: combination.ticker,
                            maturity: combination.maturity,
                            error: response.error,
                            status: 'error'
                        });
                    }
                })
                .catch(error => {
                    results.set(key, {
                        ticker: combination.ticker,
                        maturity: combination.maturity,
                        error: error.message,
                        status: 'error'
                    });
                });
            
            promises.push(promise);
        }
        
        // Attendre que toutes les requêtes se terminent
        await Promise.all(promises);
        
        // Mettre à jour le statut des combinaisons
        results.forEach((result, key) => {
            const combination = selectedCombinations.get(key);
            if (combination) {
                combination.status = result.status;
            }
        });
        
        updateSelectionsTable();
        
        // Afficher les résultats
        displayMultipleVolatilitySmiles(results);
        
        showAlert(`${results.size} volatility smiles générés`, 'success');
        
    } catch (error) {
        console.error('Erreur lors de la génération des smiles:', error);
        showAlert('Erreur lors de la génération des volatility smiles', 'error');
    } finally {
        showLoading(false);
    }
}

// Fonction pour générer les term structures
async function generateTermStructures() {
    if (termSelectedCombinations.size === 0) {
        showAlert('Veuillez sélectionner au moins une combinaison ticker-maturité', 'warning');
        return;
    }
    
    try {
        showLoading(true);
        
        // Marquer toutes les combinaisons comme "loading"
        termSelectedCombinations.forEach((combination, key) => {
            combination.status = 'loading';
        });
        updateTermSelectionsTable();
        
        // Récupérer les données pour chaque combinaison
        const promises = [];
        const results = new Map();
        
        for (const [key, combination] of termSelectedCombinations.entries()) {
            const promise = fetchAPI(`/api/tradier/options/${combination.ticker}/${combination.maturity}`)
                .then(response => {
                    if (response.success) {
                        results.set(key, {
                            ticker: combination.ticker,
                            maturity: combination.maturity,
                            options: response.options,
                            status: 'ready'
                        });
                    } else {
                        results.set(key, {
                            ticker: combination.ticker,
                            maturity: combination.maturity,
                            error: response.error,
                            status: 'error'
                        });
                    }
                })
                .catch(error => {
                    results.set(key, {
                        ticker: combination.ticker,
                        maturity: combination.maturity,
                        error: error.message,
                        status: 'error'
                    });
                });
            
            promises.push(promise);
        }
        
        // Attendre que toutes les requêtes se terminent
        await Promise.all(promises);
        
        // Mettre à jour le statut des combinaisons
        results.forEach((result, key) => {
            const combination = termSelectedCombinations.get(key);
            if (combination) {
                combination.status = result.status;
            }
        });
        
        updateTermSelectionsTable();
        
        // Afficher les résultats
        displayMultipleTermStructures(results);
        
        showAlert(`${results.size} term structures générés`, 'success');
        
    } catch (error) {
        console.error('Erreur lors de la génération des term structures:', error);
        showAlert('Erreur lors de la génération des term structures', 'error');
    } finally {
        showLoading(false);
    }
}

// Fonction pour afficher plusieurs volatility smiles
function displayMultipleVolatilitySmiles(results) {
    const chartContainer = document.getElementById('smile-chart');
    if (!chartContainer) return;
    
    const traces = [];
    const colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16', '#f97316'];
    let colorIndex = 0;
    
    results.forEach((result, key) => {
        if (result.status === 'ready' && result.options) {
            const optionsWithIV = result.options.filter(opt => opt.implied_volatility !== null && opt.implied_volatility > 0);
            
            if (optionsWithIV.length > 0) {
                const color = colors[colorIndex % colors.length];
                colorIndex++;
                
                // Créer une trace pour ce ticker/maturité
                const trace = {
                    x: optionsWithIV.map(opt => opt.strike),
                    y: optionsWithIV.map(opt => opt.implied_volatility * 100),
                    mode: 'lines+markers',
                    name: `${result.ticker} (${result.maturity})`,
                    line: { color: color, width: 2 },
                    marker: { size: 4 },
                    text: optionsWithIV.map(opt => 
                        `${result.ticker} - ${opt.type}<br>Strike: $${opt.strike}<br>IV: ${(opt.implied_volatility * 100).toFixed(2)}%<br>Bid: $${opt.bid || 'N/A'}<br>Ask: $${opt.ask || 'N/A'}`
                    ),
                    hovertemplate: '%{text}<extra></extra>'
                };
                
                traces.push(trace);
            }
        }
    });
    
    if (traces.length === 0) {
        showAlert('Aucune donnée valide trouvée pour générer les volatility smiles', 'warning');
        return;
    }
    
    const layout = {
        title: 'Volatility Smiles Comparison',
        xaxis: { title: 'Strike Price ($)' },
        yaxis: { title: 'Implied Volatility (%)' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ffffff' },
        legend: { x: 0.02, y: 0.98 },
        showlegend: true
    };
    
    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    };
    
    // Afficher le graphique
    Plotly.newPlot(chartContainer, traces, layout, config);
    
    // Masquer le placeholder
    const placeholder = document.getElementById('smile-chart-placeholder');
    if (placeholder) {
        placeholder.style.display = 'none';
    }
}

// Fonction pour afficher plusieurs term structures
function displayMultipleTermStructures(results) {
    const chartContainer = document.getElementById('term-chart');
    if (!chartContainer) return;
    
    const traces = [];
    const colors = ['#10b981', '#3b82f6', '#8b5cf6', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16', '#f97316'];
    let colorIndex = 0;
    
    results.forEach((result, key) => {
        if (result.status === 'ready' && result.options) {
            const optionsWithIV = result.options.filter(opt => opt.implied_volatility !== null && opt.implied_volatility > 0);
            
            if (optionsWithIV.length > 0) {
                const color = colors[colorIndex % colors.length];
                colorIndex++;
                
                // Créer une trace pour ce ticker/maturité
                const trace = {
                    x: optionsWithIV.map(opt => opt.strike),
                    y: optionsWithIV.map(opt => opt.implied_volatility * 100),
                    mode: 'lines+markers',
                    name: `${result.ticker} (${result.maturity})`,
                    line: { color: color, width: 2 },
                    marker: { size: 4 },
                    text: optionsWithIV.map(opt => 
                        `${result.ticker} - ${opt.type}<br>Strike: $${opt.strike}<br>IV: ${(opt.implied_volatility * 100).toFixed(2)}%<br>Bid: $${opt.bid || 'N/A'}<br>Ask: $${opt.ask || 'N/A'}`
                    ),
                    hovertemplate: '%{text}<extra></extra>'
                };
                
                traces.push(trace);
            }
        }
    });
    
    if (traces.length === 0) {
        showAlert('Aucune donnée valide trouvée pour générer les term structures', 'warning');
        return;
    }
    
    const layout = {
        title: 'Term Structure Comparison',
        xaxis: { title: 'Strike Price ($)' },
        yaxis: { title: 'Implied Volatility (%)' },
        plot_bgcolor: 'rgba(0,0,0,0)',
        paper_bgcolor: 'rgba(0,0,0,0)',
        font: { color: '#ffffff' },
        legend: { x: 0.02, y: 0.98 },
        showlegend: true
    };
    
    const config = {
        responsive: true,
        displayModeBar: true,
        modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d'],
        displaylogo: false
    };
    
    // Afficher le graphique
    Plotly.newPlot(chartContainer, traces, layout, config);
    
    // Masquer le placeholder
    const placeholder = document.getElementById('term-chart-placeholder');
    if (placeholder) {
        placeholder.style.display = 'none';
    }
}

// Fonction pour mettre à jour l'état des boutons
function updateButtons() {
    const generateBtn = document.getElementById('smile-compare-btn');
    const clearBtn = document.getElementById('clear-all-btn');
    
    if (generateBtn) {
        generateBtn.disabled = selectedCombinations.size === 0;
    }
    
    if (clearBtn) {
        clearBtn.disabled = selectedTickers.size === 0 && selectedCombinations.size === 0;
    }
}

// Fonction pour mettre à jour l'état des boutons pour Term Structure
function updateTermButtons() {
    const generateBtn = document.getElementById('term-compare-btn');
    const clearBtn = document.getElementById('term-clear-all-btn');
    
    if (generateBtn) {
        generateBtn.disabled = termSelectedCombinations.size === 0;
    }
    
    if (clearBtn) {
        clearBtn.disabled = termSelectedTickers.size === 0 && termSelectedCombinations.size === 0;
    }
}

// Fonction pour initialiser les event listeners des volatility smiles
function initVolatilitySmileListeners() {
    // Event listener pour l'ajout de ticker
    const symbolSelect = document.getElementById('smile-ticker-select');
    if (symbolSelect) {
        // Les symboles sont maintenant chargés automatiquement au chargement de la page
        // Pas besoin de les recharger au focus
        
        symbolSelect.addEventListener('change', function() {
            const symbol = this.value;
            if (symbol) {
                addTicker(symbol);
            }
        });
    }
    
    // Event listener pour le bouton de génération
    const generateBtn = document.getElementById('smile-compare-btn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateVolatilitySmiles);
    }
    
    // Event listener pour le bouton de suppression
    const clearBtn = document.getElementById('clear-all-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearAllSelections);
    }
    
    // Event listener pour les clics sur les maturités dans le tableau
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('maturity-cell')) {
            const ticker = event.target.dataset.ticker;
            const maturity = event.target.dataset.maturity;
            if (ticker && maturity) {
                addCombination(ticker, maturity);
            }
        }
    });
}

// Fonction pour initialiser les event listeners des term structures
function initTermStructureListeners() {
    // Event listener pour l'ajout de ticker
    const symbolSelect = document.getElementById('term-ticker-select');
    if (symbolSelect) {
        // Les symboles sont maintenant chargés automatiquement au chargement de la page
        // Pas besoin de les recharger au focus
        
        symbolSelect.addEventListener('change', function() {
            const symbol = this.value;
            if (symbol) {
                addTermTicker(symbol);
            }
        });
    }
    
    // Event listener pour le bouton de génération
    const generateBtn = document.getElementById('term-compare-btn');
    if (generateBtn) {
        generateBtn.addEventListener('click', generateTermStructures);
    }
    
    // Event listener pour le bouton de suppression
    const clearBtn = document.getElementById('term-clear-all-btn');
    if (clearBtn) {
        clearBtn.addEventListener('click', clearAllTermSelections);
    }
    
    // Event listener pour les clics sur les maturités dans le tableau
    document.addEventListener('click', function(event) {
        if (event.target.classList.contains('maturity-cell')) {
            const ticker = event.target.dataset.ticker;
            const maturity = event.target.dataset.maturity;
            if (ticker && maturity) {
                addTermCombination(ticker, maturity);
            }
        }
    });
}

// Initialiser l'application quand le DOM est prêt
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
} else {
    // Le DOM est déjà chargé, initialiser immédiatement
    initApp();
}

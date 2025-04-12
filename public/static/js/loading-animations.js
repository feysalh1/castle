/**
 * Loading animations system for Children's Castle
 * This script handles the loading screens and transitions
 */

let loadingOverlay;
let transitionOverlay;
let transitionTimeouts = [];

/**
 * Initialize the loading animation system
 */
function initLoadingSystem() {
    createLoadingOverlay();
    createTransitionOverlay();
    setupLoadingEventListeners();
    console.log('Loading system initialized');
    
    // Hide loading overlay immediately to fix stuck loading animation
    setTimeout(hideLoading, 100);
}

/**
 * Create the loading overlay
 */
function createLoadingOverlay() {
    // Remove any existing overlay
    if (document.getElementById('loading-overlay')) {
        document.getElementById('loading-overlay').remove();
    }

    // Create the overlay
    loadingOverlay = document.createElement('div');
    loadingOverlay.id = 'loading-overlay';
    loadingOverlay.className = 'loading-overlay'; // Not visible by default

    // Create the loading character (randomly selected)
    const characters = ['fox', 'bear', 'pig', 'monkey'];
    const randomCharacter = characters[Math.floor(Math.random() * characters.length)];
    const loadingCharacter = document.createElement('object');
    loadingCharacter.className = 'loading-character';
    loadingCharacter.type = 'image/svg+xml';
    loadingCharacter.data = `/static/images/loading/${randomCharacter}.svg`;

    // Create the loading message
    const loadingMessage = document.createElement('div');
    loadingMessage.className = 'loading-message';
    loadingMessage.textContent = getRandomMessage();

    // Create the spinner
    const loadingSpinner = document.createElement('div');
    loadingSpinner.className = 'loading-spinner';

    // Add all elements to the overlay
    loadingOverlay.appendChild(loadingCharacter);
    loadingOverlay.appendChild(loadingMessage);
    loadingOverlay.appendChild(loadingSpinner);

    // Add the overlay to the body
    document.body.appendChild(loadingOverlay);
}

/**
 * Create the transition overlay for story and game mode transitions
 */
function createTransitionOverlay() {
    // Story Transition
    const storyTransition = document.createElement('div');
    storyTransition.id = 'story-transition';
    storyTransition.className = 'transition-overlay';
    
    const storyCharacter = document.createElement('object');
    storyCharacter.className = 'transition-character';
    storyCharacter.type = 'image/svg+xml';
    storyCharacter.data = '/static/images/icons/book.svg';
    
    storyTransition.appendChild(storyCharacter);
    document.body.appendChild(storyTransition);
    
    // Game Transition
    const gameTransition = document.createElement('div');
    gameTransition.id = 'game-transition';
    gameTransition.className = 'transition-overlay';
    
    const gameCharacter = document.createElement('object');
    gameCharacter.className = 'transition-character';
    gameCharacter.type = 'image/svg+xml';
    gameCharacter.data = '/static/images/icons/game.svg';
    
    gameTransition.appendChild(gameCharacter);
    document.body.appendChild(gameTransition);
}

/**
 * Set up event listeners for the loading system
 */
function setupLoadingEventListeners() {
    // Page load
    window.addEventListener('load', function() {
        hideLoading();
    });
    
    // Link clicks (optional - if you want to show loading on navigation)
    document.addEventListener('click', function(e) {
        if (e.target.tagName === 'A' && !e.target.getAttribute('target') && e.target.getAttribute('href') !== '#') {
            showQuickLoading();
        }
    });
}

/**
 * Show the loading overlay
 */
function showLoading(duration = 2000) {
    createLoadingOverlay(); // Recreate to get a new random character
    loadingOverlay.classList.add('visible');
    
    // Automatically hide after the duration (unless manually hidden)
    setTimeout(() => {
        hideLoading();
    }, duration);
}

/**
 * Show a quick loading screen (shorter duration)
 */
function showQuickLoading() {
    showLoading(1000);
}

/**
 * Hide the loading overlay
 */
function hideLoading() {
    if (loadingOverlay) {
        loadingOverlay.classList.remove('visible');
    }
}

/**
 * Show a transition animation
 */
function showTransition(modeType) {
    // Clear any existing timeouts
    transitionTimeouts.forEach(timeout => clearTimeout(timeout));
    transitionTimeouts = [];
    
    // Hide any existing overlay
    document.querySelectorAll('.transition-overlay').forEach(overlay => {
        overlay.classList.remove('visible');
    });
    
    // Show the appropriate transition
    const transitionOverlay = document.getElementById(`${modeType}-transition`);
    if (transitionOverlay) {
        transitionOverlay.classList.add('visible');
        
        // Hide after a delay
        const timeout = setTimeout(() => {
            transitionOverlay.classList.remove('visible');
        }, 2000);
        transitionTimeouts.push(timeout);
    }
}

/**
 * Get a random loading message
 */
function getRandomMessage() {
    const messages = [
        'Loading magic...',
        'Getting things ready...',
        'Gathering stars...',
        'Preparing your adventure...',
        'Almost there...',
        'Warming up...',
        'Just a moment...',
        'Loading fun times...'
    ];
    return messages[Math.floor(Math.random() * messages.length)];
}

// Initialize on page load if document is already loaded
if (document.readyState === 'complete') {
    initLoadingSystem();
} else {
    window.addEventListener('DOMContentLoaded', initLoadingSystem);
}

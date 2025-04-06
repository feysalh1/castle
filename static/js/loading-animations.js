/**
 * Loading and transition animations for Children's Castle app
 * Provides playful character transitions between different app states
 */

// Characters for animations
const characters = [
    { id: 'fox', animation: 'bounce', loadingText: "The little fox is preparing your stories..." },
    { id: 'bear', animation: 'wiggle', loadingText: "Brown bear is gathering your stories..." },
    { id: 'pig', animation: 'spin', loadingText: "The little pig is building your stories..." },
    { id: 'monkey', animation: 'jump', loadingText: "Five little monkeys are jumping for your stories..." }
];

// Placeholder messages for loading screen
const loadingMessages = [
    "Getting your stories ready...",
    "Preparing fun adventures...",
    "Finding the perfect tale...",
    "Gathering magical characters...",
    "Building a castle of stories...",
    "Creating a world of imagination..."
];

// Initialize the loading system
function initLoadingSystem() {
    // Create the loading overlay
    createLoadingOverlay();
    
    // Create the transition overlay
    createTransitionOverlay();
    
    // Set up event listeners
    setupLoadingEventListeners();
}

// Create the loading overlay elements
function createLoadingOverlay() {
    // If the loading overlay already exists, don't create it again
    if (document.querySelector('.loading-overlay')) {
        return;
    }

    const loadingOverlay = document.createElement('div');
    loadingOverlay.className = 'loading-overlay';
    
    const loadingContainer = document.createElement('div');
    loadingContainer.className = 'loading-container';
    
    // Add a loading text element
    const loadingText = document.createElement('div');
    loadingText.className = 'loading-text';
    loadingText.innerText = getRandomMessage();
    
    // Add progress bar
    const progressBar = document.createElement('div');
    progressBar.className = 'progress-bar';
    
    const progressFill = document.createElement('div');
    progressFill.className = 'progress-fill';
    progressBar.appendChild(progressFill);
    
    // Add elements to the overlay
    loadingOverlay.appendChild(loadingContainer);
    loadingOverlay.appendChild(loadingText);
    loadingOverlay.appendChild(progressBar);
    
    // Add the overlay to the body
    document.body.appendChild(loadingOverlay);
}

// Create the transition overlay elements
function createTransitionOverlay() {
    // If the transition overlay already exists, don't create it again
    if (document.querySelector('.transition-overlay')) {
        return;
    }

    const transitionOverlay = document.createElement('div');
    transitionOverlay.className = 'transition-overlay';
    
    // Add transition characters (will be shown/hidden as needed)
    characters.forEach(char => {
        const transitionChar = document.createElement('img');
        transitionChar.className = 'transition-character';
        transitionChar.src = `static/images/loading/${char.id}.svg`;
        transitionChar.alt = char.id;
        transitionChar.dataset.character = char.id;
        transitionOverlay.appendChild(transitionChar);
    });
    
    // Add the overlay to the body
    document.body.appendChild(transitionOverlay);
}

// Set up event listeners for loading and transitions
function setupLoadingEventListeners() {
    // Listen for mode changes to trigger transitions
    document.querySelectorAll('.mode-button').forEach(button => {
        button.addEventListener('click', function() {
            const modeType = this.dataset.mode;
            showTransition(modeType);
        });
    });
    
    // Listen for story selection changes
    const storySelect = document.getElementById('story-select');
    if (storySelect) {
        storySelect.addEventListener('change', function() {
            showQuickLoading();
        });
    }
}

// Show the loading screen with a random character
function showLoading(duration = 2000) {
    const loadingOverlay = document.querySelector('.loading-overlay');
    const loadingContainer = loadingOverlay.querySelector('.loading-container');
    const loadingText = loadingOverlay.querySelector('.loading-text');
    const progressFill = loadingOverlay.querySelector('.progress-fill');
    
    // Clear any existing characters
    loadingContainer.innerHTML = '';
    
    // Pick a random character
    const character = characters[Math.floor(Math.random() * characters.length)];
    
    // Create character element
    const characterElement = document.createElement('img');
    characterElement.className = `loading-character character-${character.id}`;
    characterElement.src = `static/images/loading/${character.id}.svg`;
    characterElement.alt = character.id;
    
    // Add the character to the container
    loadingContainer.appendChild(characterElement);
    
    // Update loading text
    loadingText.innerText = character.loadingText;
    
    // Show the loading overlay
    loadingOverlay.classList.add('active');
    
    // Animate the progress bar
    progressFill.style.width = '0%';
    
    // Simulate loading progress
    let progress = 0;
    const progressInterval = setInterval(() => {
        progress += Math.random() * 10;
        if (progress > 100) progress = 100;
        progressFill.style.width = `${progress}%`;
        
        if (progress >= 100) {
            clearInterval(progressInterval);
            // Hide loading after the specified duration
            setTimeout(() => {
                hideLoading();
            }, 500);
        }
    }, duration / 10);
    
    // Hide loading after the duration anyway (failsafe)
    setTimeout(() => {
        hideLoading();
        clearInterval(progressInterval);
    }, duration);
}

// Show a quick version of the loading screen for transitions like story changes
function showQuickLoading() {
    showLoading(1000); // Shorter duration
}

// Hide the loading screen
function hideLoading() {
    const loadingOverlay = document.querySelector('.loading-overlay');
    loadingOverlay.classList.remove('active');
}

// Show a character transition between modes
function showTransition(modeType) {
    const transitionOverlay = document.querySelector('.transition-overlay');
    transitionOverlay.classList.add('active');
    
    // Pick an appropriate character based on mode or random
    let characterId;
    if (modeType === 'story') {
        characterId = 'fox';
    } else if (modeType === 'game') {
        characterId = 'monkey';
    } else {
        // Random character if mode not specified
        const randomChar = characters[Math.floor(Math.random() * characters.length)];
        characterId = randomChar.id;
    }
    
    // Get the character element
    const characterElement = transitionOverlay.querySelector(`[data-character="${characterId}"]`);
    
    // Show the character with animation
    characterElement.classList.add('active');
    
    // After animation, hide the character and overlay
    setTimeout(() => {
        characterElement.classList.add('exit');
        
        setTimeout(() => {
            transitionOverlay.classList.remove('active');
            
            setTimeout(() => {
                characterElement.classList.remove('active', 'exit');
            }, 500);
            
            // Show a loading screen after the transition
            showLoading();
        }, 600);
    }, 1000);
}

// Get a random loading message
function getRandomMessage() {
    return loadingMessages[Math.floor(Math.random() * loadingMessages.length)];
}

// Initialize the loading system when the DOM is ready
document.addEventListener('DOMContentLoaded', initLoadingSystem);

// Show a loading screen on initial page load
window.addEventListener('load', () => {
    // Short delay to ensure everything is ready
    setTimeout(() => {
        showLoading(2000);
    }, 300);
});

// Export functions for use in other modules
window.loadingAnimations = {
    showLoading,
    hideLoading,
    showTransition,
    showQuickLoading
};
// Game loading messages
const gameLoadingMessages = [
    "Loading your fun game...",
    "Getting your game ready to play...",
    "Preparing a fun challenge...",
    "Setting up your playtime...",
    "Creating a fun activity for you..."
];

// Success messages for game completion
const successMessages = [
    "Great job! You did it!",
    "Awesome work! You finished!",
    "Congratulations! You completed it!",
    "Fantastic! You're amazing!",
    "Wonderful! You're a superstar!"
];

// Update the showTransition function to handle new types
const originalShowTransition = window.loadingAnimations.showTransition;

// Override the showTransition function to handle more transition types
window.loadingAnimations.showTransition = function(modeType) {
    const transitionOverlay = document.querySelector('.transition-overlay');
    transitionOverlay.classList.add('active');
    
    // Pick an appropriate character based on mode
    let characterId;
    let message;
    let animationClass = '';
    
    if (modeType === 'story') {
        characterId = 'fox';
        message = getRandomMessage();
    } else if (modeType === 'game') {
        characterId = 'monkey';
        message = gameLoadingMessages[Math.floor(Math.random() * gameLoadingMessages.length)];
        animationClass = 'jump-higher';
    } else if (modeType === 'success') {
        characterId = 'bear';
        message = successMessages[Math.floor(Math.random() * successMessages.length)];
        animationClass = 'celebrate';
    } else {
        // Random character if mode not specified
        const randomChar = characters[Math.floor(Math.random() * characters.length)];
        characterId = randomChar.id;
        message = getRandomMessage();
    }
    
    // Update loading message if visible
    const loadingText = document.querySelector('.loading-text');
    if (loadingText) {
        loadingText.innerText = message;
    }
    
    // Get the character element
    const characterElement = transitionOverlay.querySelector(`[data-character="${characterId}"]`);
    
    // Remove any existing animation classes
    characterElement.classList.remove('jump-higher', 'celebrate');
    
    // Add the specific animation class if needed
    if (animationClass) {
        characterElement.classList.add(animationClass);
    }
    
    // Show the character with animation
    characterElement.classList.add('active');
    
    // After animation, hide the character and overlay
    setTimeout(() => {
        characterElement.classList.add('exit');
        
        setTimeout(() => {
            transitionOverlay.classList.remove('active');
            
            setTimeout(() => {
                characterElement.classList.remove('active', 'exit', 'jump-higher', 'celebrate');
            }, 500);
            
            // Show a loading screen after the transition
            if (modeType !== 'success') {
                showLoading();
            }
        }, 600);
    }, 1000);
};

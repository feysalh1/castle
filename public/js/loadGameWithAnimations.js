/**
 * Game Loading Animation Functions
 * These functions manage loading animations when transitioning between games
 */

// Show loading animation with animal characters
function showLoadingAnimation(message = "Loading your game...") {
    // Create overlay if it doesn't exist
    if (!document.getElementById('loading-overlay')) {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'loading-overlay';
        
        const animation = document.createElement('div');
        animation.className = 'loading-animation';
        
        const animals = document.createElement('div');
        animals.className = 'animal-container';
        
        // Add animal characters
        const characters = ['fox', 'bear', 'pig', 'monkey'];
        characters.forEach(animal => {
            const animalDiv = document.createElement('div');
            animalDiv.className = `animal ${animal}`;
            animals.appendChild(animalDiv);
        });
        
        const text = document.createElement('div');
        text.className = 'loading-text';
        text.textContent = message;
        
        animation.appendChild(animals);
        animation.appendChild(text);
        overlay.appendChild(animation);
        
        document.body.appendChild(overlay);
    } else {
        // Just update the message if overlay exists
        document.querySelector('.loading-text').textContent = message;
        document.getElementById('loading-overlay').classList.remove('hidden');
    }
    
    // Add active class to show animation
    document.getElementById('loading-overlay').classList.add('active');
}

// Hide loading animation
function hideLoadingAnimation() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.classList.add('hidden');
        setTimeout(() => {
            overlay.classList.remove('active');
        }, 300);
    }
}

// Transition between games or pages with a zoom effect
function transitionWithZoom(callback, duration = 1500) {
    // Show overlay
    showLoadingAnimation("Switching games...");
    
    // Add zoom effect to body
    document.body.classList.add('zoom-effect');
    
    // Execute callback after animation
    setTimeout(() => {
        // Remove zoom effect
        document.body.classList.remove('zoom-effect');
        
        // Execute callback (like loading new game)
        if (typeof callback === 'function') {
            callback();
        }
        
        // Hide loading animation
        hideLoadingAnimation();
    }, duration);
}

// Change game with animal character animations
function changeGameWithAnimation(gameId, difficulty, title) {
    // Show loading with animal characters
    showLoadingAnimation(`${getRandomLoadingMessage()} ${title}...`);
    
    // After delay, load the game
    setTimeout(() => {
        // Load the game
        if (typeof loadGame === 'function') {
            loadGame(gameId, difficulty, title);
        } else {
            console.warn('loadGame function not found');
        }
        
        // Hide loading animation
        hideLoadingAnimation();
        
        // Show game area
        document.getElementById('game-area').classList.remove('hidden');
        document.getElementById('current-game-title').textContent = title;
    }, 1800); // Showing animation for 1.8 seconds
}

// Random loading messages for children
function getRandomLoadingMessage() {
    const messages = [
        "Getting ready for",
        "Preparing your fun with",
        "The animals are setting up",
        "Here comes",
        "Setting up",
        "Time for fun with",
        "The magic forest is preparing",
        "Let's play"
    ];
    
    return messages[Math.floor(Math.random() * messages.length)];
}

// Listen for game play button clicks
document.addEventListener('DOMContentLoaded', () => {
    // If any play buttons exist
    const playButtons = document.querySelectorAll('.play-btn');
    
    if (playButtons.length > 0) {
        playButtons.forEach(button => {
            button.addEventListener('click', function() {
                const game = this.getAttribute('data-game');
                const difficulty = this.getAttribute('data-difficulty');
                const gameTitle = this.closest('.game-card').querySelector('h3').textContent;
                
                // Use the animation to change game
                changeGameWithAnimation(game, difficulty, gameTitle);
            });
        });
    }
});
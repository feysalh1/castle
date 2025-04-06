/**
 * Enhanced game loading functionality with animations
 * This file extends the game loading functionality with animated transitions
 */

/**
 * Load a game with loading animations
 * @param {string} gameId - The ID of the game to load
 */
function loadGameWithAnimation(gameId) {
    // Show the loading animation before loading the game
    showTransition('game');
    
    // After a delay to show the animation, load the actual game
    setTimeout(() => {
        // Call the original loadGame function from games.js
        loadGame(gameId);
    }, 1500); // 1.5 seconds animation time
}

/**
 * Load an external game with loading animations
 * @param {string} url - The URL of the external game
 * @param {string} title - The title of the external game
 */
function loadExternalGameWithAnimation(url, title) {
    // Show the loading animation before loading the external game
    showTransition('game');
    
    // After a delay to show the animation, load the actual external game
    setTimeout(() => {
        // Call the original loadExternalGame function from games.js
        loadExternalGame(url, title);
    }, 1500); // 1.5 seconds animation time
}

/**
 * Complete a game with success animation
 * @param {string} gameId - The ID of the completed game
 */
function completeGameWithAnimation(gameId) {
    // Show a success transition animation
    showTransition('success');
    
    // Create confetti effect
    createConfetti();
    
    // Show success message
    showSuccessMessage();
    
    // Play success sound if available
    playSuccessSound();
    
    // After a delay to show the animation, complete the game
    setTimeout(() => {
        // Call the original completeGame function from games.js
        completeGame(gameId);
    }, 2000); // 2 seconds animation time
}

/**
 * Creates a confetti animation effect
 */
function createConfetti() {
    const transitionOverlay = document.querySelector('.transition-overlay');
    
    // Create multiple confetti pieces with random colors and sizes
    const colors = ['#ff6b6b', '#feca57', '#1dd1a1', '#48dbfb', '#ff9ff3', '#f368e0'];
    const confettiCount = 50;
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.width = Math.random() * 10 + 5 + 'px';
        confetti.style.height = Math.random() * 10 + 5 + 'px';
        confetti.style.left = Math.random() * 100 + '%';
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.borderRadius = Math.random() > 0.5 ? '50%' : '0';
        
        transitionOverlay.appendChild(confetti);
        
        // Animate the confetti
        const animationDuration = Math.random() * 2 + 1;
        confetti.style.animation = `fall ${animationDuration}s ease-in forwards`;
        confetti.style.transform = `rotate(${Math.random() * 360}deg)`;
        confetti.style.opacity = Math.random();
        
        // Remove confetti after animation completes
        setTimeout(() => {
            confetti.remove();
        }, animationDuration * 1000);
    }
}

/**
 * Shows a success message
 */
function showSuccessMessage() {
    const transitionOverlay = document.querySelector('.transition-overlay');
    
    // Create success message element
    const successMessage = document.createElement('div');
    successMessage.className = 'success-message';
    successMessage.textContent = "Great Job!";
    
    transitionOverlay.appendChild(successMessage);
    
    // Remove message after the animation
    setTimeout(() => {
        successMessage.remove();
    }, 2000);
}

/**
 * Plays a success sound
 */
function playSuccessSound() {
    // Check if we have the playAchievementSound function from rewards.js
    if (typeof playAchievementSound === 'function') {
        playAchievementSound();
    } else {
        // Fallback - create a simple sound
        try {
            const audio = new Audio('static/audio/success.mp3');
            audio.volume = 0.5;
            audio.play().catch(e => console.log('Could not play success sound'));
        } catch (e) {
            console.log('Success sound not available');
        }
    }
}

// Add event listeners when the document is ready
document.addEventListener('DOMContentLoaded', function() {
    // Update game cards to use the animated loading functions
    const gameCards = document.querySelectorAll('.game-card');
    
    gameCards.forEach(card => {
        // We need to replace the original click handlers with our animated versions
        const originalOnClick = card.onclick;
        
        if (originalOnClick) {
            // Remove the original event listener
            card.onclick = null;
            
            // Add our enhanced event listener
            card.addEventListener('click', function(e) {
                e.preventDefault();
                
                const gameId = this.dataset.gameId;
                if (gameId) {
                    loadGameWithAnimation(gameId);
                } else if (this.dataset.externalUrl) {
                    loadExternalGameWithAnimation(
                        this.dataset.externalUrl,
                        this.dataset.title || 'External Game'
                    );
                }
            });
        }
    });
    
    // Also update any external game links
    const externalGameLinks = document.querySelectorAll('.external-game-link');
    
    externalGameLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const url = this.getAttribute('href');
            const title = this.textContent || 'External Game';
            
            loadExternalGameWithAnimation(url, title);
        });
    });
    
    // Update the game completion buttons to use animations
    const gameCompletionButtons = document.querySelectorAll('.complete-game-btn');
    
    gameCompletionButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            
            const gameId = this.dataset.gameId;
            if (gameId) {
                completeGameWithAnimation(gameId);
            }
        });
    });
});

/**
 * Standalone initialization script for shooting stars
 * This ensures the effect works properly on the static showcase site
 */

// Create container for shooting stars immediately
const shootingStarContainer = document.createElement('div');
shootingStarContainer.className = 'shooting-star-container';
document.body.appendChild(shootingStarContainer);

// Function to create a shooting star
function createShootingStar(delay = 0) {
    setTimeout(() => {
        const star = document.createElement('div');
        star.className = 'shooting-star';
        
        // Random starting position
        const startX = Math.random() * window.innerWidth;
        const startY = Math.random() * (window.innerHeight / 3);
        
        // Random travel distance
        const travelX = (Math.random() * window.innerWidth) - (window.innerWidth / 2);
        const travelY = Math.random() * window.innerHeight + (window.innerHeight / 2);
        
        // Random rotation
        const rotation = Math.random() * 360;
        
        // Set custom properties
        star.style.setProperty('--travel-distance-x', `${travelX}px`);
        star.style.setProperty('--travel-distance-y', `${travelY}px`);
        star.style.setProperty('--rotation', `${rotation}deg`);
        
        // Set position
        star.style.top = `${startY}px`;
        star.style.left = `${startX}px`;
        
        // Add to container
        shootingStarContainer.appendChild(star);
        
        // Remove after animation completes
        setTimeout(() => {
            star.remove();
        }, 3000);
    }, delay);
}

// Function to create multiple stars
function createMultipleStars(count = 3) {
    for (let i = 0; i < count; i++) {
        createShootingStar(i * 200);
    }
}

// Create stars immediately and periodically
document.addEventListener('DOMContentLoaded', function() {
    console.log('Standalone shooting stars initialized');
    
    // Initial stars
    createMultipleStars(3);
    
    // Create periodic stars
    setInterval(() => {
        createShootingStar();
    }, 8000);
    
    // Create occasional bursts of stars
    setInterval(() => {
        createMultipleStars(Math.floor(Math.random() * 3) + 2);
    }, 25000);
});
/**
 * Shooting Star Animation
 * Creates a magical shooting star transition when selecting a story
 */

// Wait for the document to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Shooting star script loaded');
    
    // Initialize the shooting star functionality
    enhanceStorySelection();
});

/**
 * Creates the container for shooting stars
 * @returns {HTMLElement} The container element
 */
function createShootingStarContainer() {
    // Check if container already exists
    let container = document.querySelector('.shooting-star-container');
    
    if (!container) {
        container = document.createElement('div');
        container.className = 'shooting-star-container';
        document.body.appendChild(container);
    }
    
    return container;
}

/**
 * Creates a single shooting star
 * @param {HTMLElement} container The container to add the star to
 */
function createShootingStar(container) {
    // Create the star element
    const star = document.createElement('div');
    star.className = 'shooting-star';
    
    // Random starting position (top edge)
    const startX = Math.random() * window.innerWidth * 0.8 + window.innerWidth * 0.1;
    const startY = Math.random() * window.innerHeight * 0.3;
    
    // Calculate travel distance (diagonal path)
    const travelDistanceX = (Math.random() * 300) - 150;
    const travelDistanceY = Math.random() * 300 + 200;
    
    // Set random rotation
    const rotation = Math.random() * 45;
    
    // Set CSS variables for the animation
    star.style.setProperty('--travel-distance-x', `${travelDistanceX}px`);
    star.style.setProperty('--travel-distance-y', `${travelDistanceY}px`);
    star.style.setProperty('--rotation', `${rotation}deg`);
    
    // Position the star
    star.style.left = `${startX}px`;
    star.style.top = `${startY}px`;
    
    // Add to container
    container.appendChild(star);
    
    // Remove after animation completes
    setTimeout(() => {
        star.remove();
    }, 3000);
}

/**
 * Creates multiple shooting stars
 * @param {number} numStars Number of stars to create
 */
function runShootingStarAnimation(numStars = 5) {
    const container = createShootingStarContainer();
    
    // Create stars with slight delay between each
    for (let i = 0; i < numStars; i++) {
        setTimeout(() => {
            createShootingStar(container);
        }, i * 300);
    }
}

/**
 * Applies zoom transition effect to an element
 * @param {HTMLElement} element The element to apply the effect to
 */
function applyZoomTransition(element) {
    // Add transition class
    element.classList.add('zoom-transition');
    
    // Apply active state after a small delay (to ensure the class is applied first)
    setTimeout(() => {
        element.classList.add('active');
    }, 50);
}

/**
 * Enhances story selection with animations
 */
function enhanceStorySelection() {
    // Add event listeners to both select dropdown and read book buttons
    const storySelect = document.getElementById('story-select');
    const readBookButtons = document.querySelectorAll('.read-book-btn');
    
    // For the dropdown selection
    if (storySelect) {
        storySelect.addEventListener('change', function() {
            console.log('Story selected from dropdown');
            
            if (this.value) {
                // Run the shooting star animation
                runShootingStarAnimation(7);
                
                // Apply zoom effect to the select element
                applyZoomTransition(this.parentElement);
            }
        });
    }
    
    // For the book cards with read buttons
    if (readBookButtons.length > 0) {
        readBookButtons.forEach(button => {
            button.addEventListener('click', function(event) {
                console.log('Book card button clicked');
                
                // Run the shooting star animation
                runShootingStarAnimation(7);
                
                // Apply zoom effect to the book card
                const bookCard = this.closest('.book-card');
                if (bookCard) {
                    applyZoomTransition(bookCard);
                }
                
                // Don't stop the event here - let it propagate to load the story
            });
        });
    }
    
    console.log(`Enhanced story selection: ${storySelect ? 'dropdown active' : 'dropdown not found'}, ${readBookButtons.length} book buttons found`);
}
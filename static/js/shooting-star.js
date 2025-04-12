/**
 * Shooting Star Animation
 * Creates a magical shooting star transition when selecting a story
 */

function createShootingStarContainer() {
    // Check if container already exists
    if (document.querySelector('.shooting-star-container')) {
        return document.querySelector('.shooting-star-container');
    }

    // Create container for the shooting stars
    const container = document.createElement('div');
    container.className = 'shooting-star-container';
    document.body.appendChild(container);
    return container;
}

function createShootingStar(container) {
    // Create a shooting star element
    const star = document.createElement('div');
    star.className = 'shooting-star';
    
    // Add random positioning
    const startX = Math.random() * 100 - 50; // Random X position
    const startY = Math.random() * 100 + 50; // Random Y position
    star.style.top = `${startY}px`;
    star.style.left = `${startX}px`;
    
    // Add to container
    container.appendChild(star);
    
    // Remove after animation completes
    setTimeout(() => {
        star.remove();
    }, 1500);
}

function runShootingStarAnimation(numStars = 5) {
    const container = createShootingStarContainer();
    container.style.display = 'block';
    
    // Create multiple shooting stars with staggered timing
    for (let i = 0; i < numStars; i++) {
        setTimeout(() => {
            createShootingStar(container);
        }, i * 300); // Stagger the stars
    }
    
    // Hide container after all animations complete
    setTimeout(() => {
        container.style.display = 'none';
    }, numStars * 300 + 1500);
}

function applyZoomTransition(element) {
    element.classList.add('zoom-transition');
    
    // Remove class after animation completes
    setTimeout(() => {
        element.classList.remove('zoom-transition');
    }, 1200);
}

// Enhance the story button click
function enhanceStorySelection() {
    document.addEventListener('DOMContentLoaded', function() {
        console.log('Shooting star script loaded');
        
        const readBookButtons = document.querySelectorAll('.read-book-btn');
        
        if (readBookButtons.length > 0) {
            readBookButtons.forEach(button => {
                // Keep the original click handler but add our fancy effects
                const originalClick = button.onclick;
                
                button.addEventListener('click', function(event) {
                    event.preventDefault();
                    
                    // Find the parent card and apply selected state
                    const card = this.closest('.story-card-container');
                    if (card) {
                        card.classList.add('selected');
                    }
                    
                    // Run shooting star animation
                    runShootingStarAnimation(7);
                    
                    // Apply zoom transition to the book card
                    setTimeout(() => {
                        if (card) {
                            applyZoomTransition(card);
                        }
                        
                        // Get the book ID
                        const bookId = this.getAttribute('data-book-id');
                        
                        // After visual effects, navigate to the story
                        setTimeout(() => {
                            fetch(`/api/story/${bookId}`)
                                .then(response => response.json())
                                .then(data => {
                                    console.log('Story data loaded with magical transition:', data);
                                    
                                    if (data.success) {
                                        // Hide loading if necessary
                                        if (typeof hideLoading === 'function') {
                                            hideLoading();
                                        } else if (document.getElementById('loading-animation')) {
                                            document.getElementById('loading-animation').style.display = 'none';
                                        }
                                    } else {
                                        console.error('Error loading story:', data.message);
                                        alert('Sorry, there was a problem loading the story. Please try again.');
                                        
                                        // Hide loading if necessary
                                        if (typeof hideLoading === 'function') {
                                            hideLoading();
                                        } else if (document.getElementById('loading-animation')) {
                                            document.getElementById('loading-animation').style.display = 'none';
                                        }
                                    }
                                })
                                .catch(error => {
                                    console.error('Error fetching story:', error);
                                    alert('Sorry, there was a problem loading the story. Please try again.');
                                    
                                    // Hide loading if necessary
                                    if (typeof hideLoading === 'function') {
                                        hideLoading();
                                    } else if (document.getElementById('loading-animation')) {
                                        document.getElementById('loading-animation').style.display = 'none';
                                    }
                                });
                        }, 1000); // Wait for zoom animation before loading
                    }, 500); // Small delay before zoom
                });
            });
        }
    });
}

// Initialize the enhanced story selection
enhanceStorySelection();
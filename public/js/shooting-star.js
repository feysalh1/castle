/**
 * Shooting Star Animation
 * Creates a magical shooting star animation when selecting a story
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Shooting star script loaded');

    // Create container for shooting stars
    const container = document.createElement('div');
    container.className = 'shooting-star-container';
    document.body.appendChild(container);

    // Function to run shooting star animation
    window.runShootingStarAnimation = function(starCount = 5) {
        // Remove any existing stars
        container.innerHTML = '';
        
        // Create new stars
        for (let i = 0; i < starCount; i++) {
            createShootingStar(container, i * 200);
        }
    };

    // Function to create a shooting star
    function createShootingStar(container, delay = 0) {
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
            container.appendChild(star);
            
            // Remove after animation completes
            setTimeout(() => {
                star.remove();
            }, 3000);
        }, delay);
    }

    // Function to apply zoom transition effect to elements
    window.applyZoomTransition = function(element, duration = 1500) {
        if (!element) return;
        
        // Add transition class
        element.classList.add('zoom-transition');
        element.classList.add('active');
        
        // Remove active class after animation
        setTimeout(() => {
            element.classList.remove('active');
            
            // Remove transition class after animation
            setTimeout(() => {
                element.classList.remove('zoom-transition');
            }, 500);
        }, duration);
    };

    // Apply zoom effect to book cards when clicked
    document.querySelectorAll('.read-book-btn').forEach(button => {
        button.addEventListener('click', () => {
            runShootingStarAnimation(7);
            
            // Find parent book card
            const bookCard = button.closest('.book-card');
            if (bookCard) {
                applyZoomTransition(bookCard);
            }
        });
    });

    // Show as many shooting stars as there are story pages when a story completes
    document.querySelectorAll('.nav-btn').forEach(button => {
        if (button.id === 'next-btn') {
            button.addEventListener('click', () => {
                const currentPage = parseInt(document.getElementById('current-page').textContent);
                const totalPages = parseInt(document.getElementById('total-pages').textContent);
                
                if (currentPage === totalPages) {
                    runShootingStarAnimation(totalPages);
                }
            });
        }
    });
});
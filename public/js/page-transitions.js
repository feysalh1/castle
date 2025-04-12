/**
 * Page Transitions with Zoom Effect
 * This script handles the smooth transitions between pages with a zoom effect.
 */

// Create the transition overlay element if it doesn't exist
function createTransitionOverlay() {
    if (!document.getElementById('page-transition-overlay')) {
        const overlay = document.createElement('div');
        overlay.id = 'page-transition-overlay';
        overlay.className = 'page-transition';
        
        // Create castle image for zoom effect
        const castleImg = document.createElement('img');
        castleImg.src = '/static/images/background/night-castle-new.png';
        castleImg.alt = 'Castle';
        castleImg.style.maxWidth = '90%';
        castleImg.style.maxHeight = '90vh';
        castleImg.className = 'zoom-effect';
        castleImg.style.display = 'none';
        
        overlay.appendChild(castleImg);
        document.body.appendChild(overlay);
    }
}

// Trigger the page transition when navigating
function triggerPageTransition(url) {
    createTransitionOverlay();
    
    const overlay = document.getElementById('page-transition-overlay');
    const castleImg = overlay.querySelector('img');
    
    // Show the overlay
    overlay.classList.add('active');
    
    // Show and animate the castle image
    setTimeout(() => {
        castleImg.style.display = 'block';
    }, 100);
    
    // Navigate to the new page after the animation
    setTimeout(() => {
        window.location.href = url;
    }, 1200);
    
    return false; // Prevent default link behavior
}

// Intercept all internal navigation links and apply the transition effect
document.addEventListener('DOMContentLoaded', function() {
    createTransitionOverlay();
    
    // Handle links with transition effect
    document.body.addEventListener('click', function(e) {
        // Check if clicked element is a link or has a parent that is a link
        let linkElement = e.target.closest('a');
        
        if (linkElement) {
            const href = linkElement.getAttribute('href');
            
            // Skip external links, anchor links, or javascript actions
            if (href && href.indexOf('#') !== 0 && href.indexOf('javascript:') !== 0 && href.indexOf('http') !== 0) {
                e.preventDefault();
                triggerPageTransition(href);
            }
        }
    });
    
    // Add transition effect for page load
    const overlay = document.getElementById('page-transition-overlay');
    const castleImg = overlay.querySelector('img');
    
    // For page load, animate content in
    document.body.style.opacity = '0';
    
    setTimeout(() => {
        document.body.style.transition = 'opacity 1s';
        document.body.style.opacity = '1';
    }, 100);
});
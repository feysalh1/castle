/**
 * Story Mode JavaScript
 * Handles story selection and loading.
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('Story mode script loaded');

    // Set up click event listeners for the "Read Book" buttons
    const readBookButtons = document.querySelectorAll('.read-book-btn');

    if (readBookButtons.length > 0) {
        console.log(`Found ${readBookButtons.length} read book buttons`);

        readBookButtons.forEach(button => {
            button.addEventListener('click', function(event) {
                event.preventDefault();

                const bookId = this.getAttribute('data-book-id');
                console.log(`Book button clicked: ${bookId}`);

                if (bookId) {
                    // Run shooting star animation if available
                    if (typeof runShootingStarAnimation === 'function') {
                        runShootingStarAnimation(7);
                    }

                    // Apply zoom effect if available
                    if (typeof applyZoomTransition === 'function') {
                        const bookCard = this.closest('.book-card');
                        if (bookCard) {
                            applyZoomTransition(bookCard);
                        }
                    }

                    // Create a modal loading container if needed
                    let loadingContainer = document.getElementById('story-loading-container');
                    if (!loadingContainer) {
                        loadingContainer = document.createElement('div');
                        loadingContainer.id = 'story-loading-container';
                        loadingContainer.className = 'loading-container';

                        const loadingContent = document.createElement('div');
                        loadingContent.className = 'loading-content';

                        const foxAnimation = document.createElement('div');
                        foxAnimation.className = 'fox-animation';

                        const loadingText = document.createElement('p');
                        loadingText.textContent = 'Loading your story...';

                        loadingContent.appendChild(foxAnimation);
                        loadingContent.appendChild(loadingText);
                        loadingContainer.appendChild(loadingContent);
                        document.body.appendChild(loadingContainer);
                    } else {
                        loadingContainer.style.display = 'flex';
                    }

                    // Navigate to story page after animation
                    setTimeout(() => {
                        window.location.href = `/story/${bookId}`;
                    }, 1500);
                }
            });
        });
    } else {
        console.log('No read book buttons found');
    }

    // Set up age group filter functionality
    const ageFilter = document.getElementById('age-filter');

    if (ageFilter) {
        ageFilter.addEventListener('change', function() {
            const selectedAgeGroup = this.value;

            // Get all age group sections
            const ageGroupSections = document.querySelectorAll('.age-group-section');

            if (selectedAgeGroup === 'all') {
                // Show all sections
                ageGroupSections.forEach(section => {
                    section.style.display = 'block';
                });
            } else {
                // Show only selected age group
                ageGroupSections.forEach(section => {
                    if (section.getAttribute('data-age-group') === selectedAgeGroup) {
                        section.style.display = 'block';
                    } else {
                        section.style.display = 'none';
                    }
                });
            }
        });
    }
});

// Function to hide all loading animations
function hideAllLoadingAnimations() {
    // Hide main loading animation
    const loadingAnimation = document.getElementById('loading-animation');
    if (loadingAnimation) {
        loadingAnimation.style.display = 'none';
    }

    // Hide story loading container
    const storyLoadingContainer = document.getElementById('story-loading-container');
    if (storyLoadingContainer) {
        storyLoadingContainer.style.display = 'none';
    }

    // Call external hideLoading function if it exists
    if (typeof hideLoading === 'function') {
        hideLoading();
    }
}

function loadStoryById(bookId) {
    if (!bookId) {
        console.error('Invalid book ID');
        hideAllLoadingAnimations();
        return;
    }

    fetch(`/api/stories/${bookId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.error) {
                throw new Error(data.error);
            }
            console.log('Story data loaded:', data);
            hideAllLoadingAnimations();
        })
        .catch(error => {
            console.error('Error loading story:', error);
            alert('Sorry, there was a problem loading the story. Please try again.  Details: ' + error);
            hideAllLoadingAnimations();
        });
}
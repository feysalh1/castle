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
                    
                    // Show loading animation after a short delay to let the shooting star animation finish
                    setTimeout(() => {
                        const loadingAnimation = document.getElementById('loading-animation');
                        if (loadingAnimation) {
                            loadingAnimation.style.display = 'flex';
                        }
                        loadStoryById(bookId);
                    }, 1500);
                            showLoading(true);
                        } else if (document.getElementById('loading-animation')) {
                            document.getElementById('loading-animation').style.display = 'flex';
                        }
                    }, 1000);
                    
                    // Load the story content
                    fetch(`/api/story/${bookId}`)
                        .then(response => response.json())
                        .then(data => {
                            console.log('Story data loaded:', data);
                            
                            if (data.success) {
                                // If we have an enhanced story with pages data, 
                                // let the story-reader.js handle it
                                // Otherwise, we might need to manually display the content
                                
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
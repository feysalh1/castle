/**
 * Main script for Children's Castle
 * Handles story mode and general interactions
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize audio elements
    const storyAudio = document.getElementById('story-audio');
    
    // Story-related elements
    const storySelect = document.getElementById('story-select');
    const storyContainer = document.getElementById('story-container');
    const storyIllustration = document.getElementById('story-illustration');
    const storyParagraph = document.getElementById('story-paragraph');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const playBtn = document.getElementById('play-btn');
    const progressFill = document.getElementById('progress-fill');
    const currentPageSpan = document.getElementById('current-page');
    const totalPagesSpan = document.getElementById('total-pages');
    
    // Story data
    let currentStory = null;
    let storyData = {};
    let currentPage = 0;
    
    // Initialize story selection if on story mode page
    if (storySelect) {
        storySelect.addEventListener('change', function() {
            const storyId = this.value;
            if (storyId) {
                showLoading();
                
                // Fetch the story data or generate dummy data for testing
                fetch(`/static/stories/${storyId}.json`)
                    .then(response => {
                        if (!response.ok) {
                            // If the story JSON doesn't exist yet, create dummy data
                            const dummyStory = generateDummyStory(storyId);
                            return Promise.resolve(dummyStory);
                        }
                        return response.json();
                    })
                    .then(data => {
                        currentStory = storyId;
                        storyData = data;
                        currentPage = 0;
                        
                        updateStory(currentPage);
                        document.querySelector('.empty-story-message').style.display = 'none';
                        document.querySelector('.story-content-wrapper').style.display = 'block';
                        
                        // Track progress
                        trackProgress(storyId, 'story', false);
                        
                        hideLoading();
                    })
                    .catch(error => {
                        console.error('Error loading story:', error);
                        alert('Unable to load the story. Please try again.');
                        hideLoading();
                    });
            }
        });
        
        // Story navigation
        if (prevBtn) {
            prevBtn.addEventListener('click', function() {
                if (currentPage > 0) {
                    currentPage--;
                    updateStory(currentPage);
                    if (storyAudio) {
                        storyAudio.pause();
                        playBtn.textContent = 'Play';
                    }
                }
            });
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', function() {
                if (storyData.pages && currentPage < storyData.pages.length - 1) {
                    currentPage++;
                    updateStory(currentPage);
                    if (storyAudio) {
                        storyAudio.pause();
                        playBtn.textContent = 'Play';
                    }
                    
                    // If this is the last page, mark as completed
                    if (currentPage === storyData.pages.length - 1) {
                        trackProgress(currentStory, 'story', true);
                        if (typeof awardStoryCompletionBadge === 'function') {
                            awardStoryCompletionBadge(currentStory);
                        }
                    }
                }
            });
        }
        
        if (playBtn) {
            playBtn.addEventListener('click', function() {
                if (storyAudio) {
                    if (storyAudio.paused) {
                        storyAudio.play();
                        playBtn.textContent = 'Pause';
                    } else {
                        storyAudio.pause();
                        playBtn.textContent = 'Play';
                    }
                } else {
                    console.warn('Story audio element not found');
                }
            });
        }
        
        // Audio ended event
        if (storyAudio) {
            storyAudio.addEventListener('ended', function() {
                playBtn.textContent = 'Play';
                
                // Auto-advance to next page if not on the last page
                if (storyData.pages && currentPage < storyData.pages.length - 1) {
                    currentPage++;
                    updateStory(currentPage);
                }
            });
        }
    }
    
    /**
     * Update the story display for the current page
     */
    function updateStory(pageIndex) {
        if (!storyData || !storyData.pages || !storyData.pages[pageIndex]) {
            console.warn('Story data not available');
            return;
        }
        
        const page = storyData.pages[pageIndex];
        
        // Update illustration if it exists
        if (storyIllustration) {
            storyIllustration.src = page.image || `/static/images/stories/${currentStory}/page${pageIndex + 1}.svg`;
            storyIllustration.alt = `Illustration for ${storyData.title}, page ${pageIndex + 1}`;
        }
        
        // Update text
        if (storyParagraph) {
            storyParagraph.textContent = page.text;
        }
        
        // Update audio
        if (storyAudio) {
            storyAudio.src = page.audio || `/static/audio/${currentStory}/page${pageIndex + 1}.mp3`;
            storyAudio.load();
        }
        
        // Update progress indicators
        if (progressFill) {
            progressFill.style.width = `${((pageIndex + 1) / storyData.pages.length) * 100}%`;
        }
        
        if (currentPageSpan) {
            currentPageSpan.textContent = pageIndex + 1;
        }
        
        if (totalPagesSpan) {
            totalPagesSpan.textContent = storyData.pages.length;
        }
        
        // Update navigation buttons
        if (prevBtn) {
            prevBtn.disabled = pageIndex === 0;
        }
        
        if (nextBtn) {
            nextBtn.disabled = pageIndex === storyData.pages.length - 1;
        }
    }
    
    /**
     * Generate dummy story data for testing
     */
    function generateDummyStory(storyId) {
        // Format story ID into a title
        const formatTitle = id => id.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
        
        const storyTitle = formatTitle(storyId);
        
        // Generate 3-5 pages
        const pageCount = Math.floor(Math.random() * 3) + 3;
        const pages = [];
        
        for (let i = 0; i < pageCount; i++) {
            pages.push({
                image: `/static/images/stories/${storyId}/page${i + 1}.svg`,
                text: `This is page ${i + 1} of "${storyTitle}". The actual story content will be loaded here.`,
                audio: `/static/audio/${storyId}/page${i + 1}.mp3`
            });
        }
        
        return {
            title: storyTitle,
            author: "Children's Castle",
            pages: pages
        };
    }
    
    /**
     * Track progress in the database
     */
    function trackProgress(contentId, contentType, completed) {
        fetch('/api/track-progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                content_type: contentType,
                content_id: contentId,
                completed: completed,
                time_spent: 30 // Placeholder value in seconds
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Progress tracked:', data);
        })
        .catch(error => {
            console.error('Error tracking progress:', error);
        });
    }
    
    /**
     * Play click sound for buttons
     */
    function playClickSound() {
        const clickSound = new Audio('/static/audio/click.mp3');
        clickSound.volume = 0.5;
        clickSound.play();
    }
    
    // Add click sound to all buttons
    document.querySelectorAll('button, .btn').forEach(button => {
        button.addEventListener('click', playClickSound);
    });
    
    // Create folders for the stories
    const storyIds = ['little_fox', 'three_little_pigs', 'goldilocks', 'wild_things', 
                      'brown_bear', 'hungry_caterpillar', 'rainbow_fish', 'five_monkeys',
                      'black_sheep', 'bo_peep', 'jack_jill', 'hickory_dickory'];
    
    storyIds.forEach(storyId => {
        // This would normally happen server-side
        console.log(`Ensuring directories exist for ${storyId}`);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize modal close button
    const closeModalBtn = document.getElementById('close-story-modal');
    
    // Add animation handlers for book cards
    const bookCards = document.querySelectorAll('.book-card');
    bookCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Only trigger if the click wasn't on the button
            if (!e.target.classList.contains('read-book-btn')) {
                // Remove expanded class from all cards
                bookCards.forEach(c => c.classList.remove('expanded'));
                // Add expanded class to clicked card
                this.classList.add('expanded');
                // Add animation class
                this.classList.add('animate');
                // Remove animation class after animation completes
                setTimeout(() => {
                    this.classList.remove('animate');
                }, 800);
            }
        });
    });
    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeStoryModal);
    }
    
    // Close modal when clicking on overlay (outside the content)
    const storyModal = document.getElementById('story-modal');
    if (storyModal) {
        storyModal.addEventListener('click', function(event) {
            if (event.target === storyModal) {
                closeStoryModal();
            }
        });
    }
    
    // Close modal with escape key
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape' && storyModal && storyModal.classList.contains('active')) {
            closeStoryModal();
        }
    });
    
    // Function to close the story modal
    function closeStoryModal() {
        if (storyModal) {
            storyModal.classList.remove('active');
            
            // If there's audio playing, pause it
            if (storyAudio && isAudioPlaying) {
                storyAudio.pause();
                isAudioPlaying = false;
                playButton.textContent = 'Play / Pause';
            }
        }
    }
    // Story elements
    const storySelect = document.getElementById('story-select');
    const storyContainer = document.getElementById('story-container');
    const emptyMessage = document.querySelector('.empty-story-message');
    const storyWrapper = document.querySelector('.story-content-wrapper');
    const storyIllustration = document.getElementById('story-illustration');
    const storyParagraph = document.getElementById('story-paragraph');
    const prevButton = document.getElementById('prev-btn');
    const nextButton = document.getElementById('next-btn');
    const playButton = document.getElementById('play-btn');
    const progressFill = document.getElementById('progress-fill');
    const currentPageSpan = document.getElementById('current-page');
    const totalPagesSpan = document.getElementById('total-pages');
    const loadingAnimation = document.getElementById('loading-animation');

    // For the new age-based UI
    const readBookButtons = document.querySelectorAll('.read-book-btn');

    // Story state
    let storyContent = '';
    let storyPages = [];
    let currentPage = 0;
    let storyAudio = null;
    let isAudioPlaying = false;

    // Add event listeners for the read book buttons (new UI)
    if (readBookButtons.length > 0) {
        readBookButtons.forEach(button => {
            button.addEventListener('click', async function() {
                const bookId = this.getAttribute('data-book-id');
                if (bookId) {
                    // Load story after a short delay to allow shooting star animation to complete
                    setTimeout(async () => {
                        await loadStoryById(bookId);
                    }, 1200);
                }
            });
        });
    }

    // Add event listener for the story select dropdown (legacy UI)
    if (storySelect) {
        storySelect.addEventListener('change', async function() {
            const storyId = this.value;
            if (storyId) {
                // Run shooting star animation if available
                if (typeof runShootingStarAnimation === 'function') {
                    runShootingStarAnimation(7);
                }
                
                // Apply zoom effect if available
                if (typeof applyZoomTransition === 'function') {
                    applyZoomTransition(this.parentElement);
                }
                
                // Load story after a short delay to allow shooting star animation to complete
                setTimeout(async () => {
                    await loadStoryById(storyId);
                }, 1200);
            }
        });
    }

    // Load story content from server
    async function loadStoryById(storyId) {
        showLoading(true);

        try {
            const response = await fetch(`/api/story/${storyId}`);
            const data = await response.json();

            if (data.success) {
                // Store story content
                storyContent = data.content;

                // If enhanced story with pages
                if (data.enhanced && data.pages) {
                    // For enhanced stories, use the pre-defined pages
                    storyPages = data.pages;
                } else {
                    // For regular stories, split by paragraphs
                    storyPages = storyContent.split('\n\n').filter(p => p.trim() !== '');
                }

                // Initialize story display
                currentPage = 0;
                totalPagesSpan.textContent = storyPages.length;

                // Show story modal
                emptyMessage.style.display = 'none';
                storyWrapper.style.display = 'block';
                document.getElementById('story-modal').classList.add('active');
                document.getElementById('story-modal-title').textContent = data.title || 'Reading Story';

                // Display first page
                displayPage(0);

                // Track progress with the story
                trackProgress(storyId, data.title || 'Untitled Story', false);

                // Set up page navigation
                setupPageNavigation();
            } else {
                showError(data.message || 'Failed to load story');
            }
        } catch (error) {
            showError('Error loading story: ' + error.message);
        } finally {
            showLoading(false);
        }
    }

    // Display a specific page of the story
    function displayPage(pageIndex) {
        if (pageIndex >= 0 && pageIndex < storyPages.length) {
            currentPage = pageIndex;

            // For enhanced stories with pages object
            if (typeof storyPages[pageIndex] === 'object') {
                const page = storyPages[pageIndex];

                // Set text content
                storyParagraph.textContent = page.text || '';

                // Set illustration if available
                if (page.image) {
                    storyIllustration.src = page.image;
                    storyIllustration.style.display = 'block';
                } else {
                    storyIllustration.style.display = 'none';
                }

                // Set up audio if available
                if (page.audio) {
                    setupAudio(page.audio);
                } else {
                    storyAudio = null;
                    isAudioPlaying = false;
                    playButton.textContent = 'Play / Pause';
                }
            } else {
                // For regular text-only stories
                storyParagraph.textContent = storyPages[pageIndex];
                storyIllustration.style.display = 'none';
                storyAudio = null;
                isAudioPlaying = false;
                playButton.textContent = 'Play / Pause';
            }

            // Update UI elements
            currentPageSpan.textContent = currentPage + 1;
            const progressPercent = ((currentPage + 1) / storyPages.length) * 100;
            progressFill.style.width = progressPercent + '%';

            // Update button states
            prevButton.disabled = currentPage === 0;
            nextButton.disabled = currentPage === storyPages.length - 1;

            // If this is the last page, mark story as completed
            if (currentPage === storyPages.length - 1) {
                const storyId = storySelect ? storySelect.value : 
                                document.querySelector('.read-book-btn[data-book-id]')?.getAttribute('data-book-id');
                const storyTitle = storySelect ? 
                                  storySelect.options[storySelect.selectedIndex].text : 
                                  document.querySelector('.book-card h4')?.textContent || 'Untitled Story';

                trackProgress(storyId, storyTitle, true);
            }
        }
    }

    // Setup audio player
    function setupAudio(audioSrc) {
        if (storyAudio) {
            storyAudio.pause();
            storyAudio = null;
        }

        // Get selected voice
        const narratorVoice = document.getElementById('narrator-voice').value;

        // Generate audio with selected voice if it's a text source
        if (typeof audioSrc === 'string' && !audioSrc.startsWith('http') && !audioSrc.startsWith('/')) {
            fetch('/api/generate-voice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    text: audioSrc,
                    voice_id: narratorVoice
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success && data.audio_url) {
                    storyAudio = new Audio(data.audio_url);
                    storyAudio.addEventListener('ended', function() {
                        isAudioPlaying = false;
                        playButton.textContent = 'Play / Pause';
                    });
                }
            })
            .catch(error => console.error('Error generating voice:', error));
        } else {
            storyAudio = new Audio(audioSrc);
            storyAudio.addEventListener('ended', function() {
                isAudioPlaying = false;
                playButton.textContent = 'Play / Pause';
            });
        }

        playButton.disabled = false;
    }

    // Setup page navigation buttons
    function setupPageNavigation() {
        prevButton.addEventListener('click', function() {
            if (currentPage > 0) {
                displayPage(currentPage - 1);
                if (storyAudio) {
                    storyAudio.pause();
                    isAudioPlaying = false;
                    playButton.textContent = 'Play / Pause';
                }
            }
        });

        nextButton.addEventListener('click', function() {
            if (currentPage < storyPages.length - 1) {
                displayPage(currentPage + 1);
                if (storyAudio) {
                    storyAudio.pause();
                    isAudioPlaying = false;
                    playButton.textContent = 'Play / Pause';
                }
            }
        });

        playButton.addEventListener('click', function() {
            if (storyAudio) {
                if (isAudioPlaying) {
                    storyAudio.pause();
                    isAudioPlaying = false;
                    playButton.textContent = 'Play / Pause';
                } else {
                    storyAudio.play();
                    isAudioPlaying = true;
                    playButton.textContent = 'Pause';
                }
            }
        });
    }

    // Track progress in the story
    function trackProgress(storyId, storyTitle, completed) {
        // Check if we have a valid child ID to prevent database errors
        const childIdElement = document.getElementById('child-id');
        if (!childIdElement) {
            console.log('No child ID found, skipping progress tracking');
            return;
        }
        
        const data = {
            content_type: 'story',
            content_id: storyId,
            content_title: storyTitle,
            completed: completed,
            time_spent: 60, // Default to 1 minute
            pages_read: currentPage + 1
        };

        fetch('/api/track-progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to track progress');
            }
            return response.json();
        })
        .then(data => {
            if (!data.success) {
                console.warn('Progress tracking response indicated failure:', data.message || 'Unknown error');
            }
        })
        .catch(error => {
            console.error('Error tracking progress:', error);
            // Continue loading the story even if progress tracking fails
        });
    }

    // Show loading animation
    function showLoading(isLoading) {
        if (loadingAnimation) {
            loadingAnimation.style.display = isLoading ? 'flex' : 'none';
            
            // Show the loading animation inside the modal if it's open
            if (isLoading) {
                const storyModal = document.getElementById('story-modal');
                if (storyModal && storyModal.classList.contains('active')) {
                    // Append loading animation to modal instead of body
                    storyModal.appendChild(loadingAnimation);
                } else {
                    // Make sure it's in the body when no modal is active
                    document.body.appendChild(loadingAnimation);
                }
            }
        }
    }

    // Show error message
    function showError(message) {
        emptyMessage.style.display = 'block';
        storyWrapper.style.display = 'none';
        const errorParagraph = emptyMessage.querySelector('p');
        errorParagraph.textContent = message;

        // Log error to server
        fetch('/api/log-error', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                error_type: 'story_reader',
                error_message: message,
                error_context: { location: 'story_reader.js' }
            })
        }).catch(err => console.error('Failed to log error:', err));
    }

    // Enable keyboard navigation
    document.addEventListener('keydown', function(event) {
        if (storyWrapper.style.display === 'block') {
            if (event.key === 'ArrowLeft' && !prevButton.disabled) {
                prevButton.click();
            } else if (event.key === 'ArrowRight' && !nextButton.disabled) {
                nextButton.click();
            } else if (event.key === ' ' || event.key === 'Spacebar') {
                if (storyAudio) {
                    playButton.click();
                    event.preventDefault();  // Prevent page scrolling
                }
            }
        }
    });

    // Track emotional feedback with emoji reactions
    const emojiContainer = document.createElement('div');
    emojiContainer.className = 'emoji-reactions';
    emojiContainer.innerHTML = `
        <span class="emoji-title">How did this story make you feel?</span>
        <div class="emoji-buttons">
            <button class="emoji-btn" data-emotion="happy">😄</button>
            <button class="emoji-btn" data-emotion="sad">😢</button>
            <button class="emoji-btn" data-emotion="excited">🤩</button>
            <button class="emoji-btn" data-emotion="scared">😱</button>
            <button class="emoji-btn" data-emotion="curious">🤔</button>
        </div>
    `;

    storyContainer.appendChild(emojiContainer);

    // Add styles for emoji reactions
    const style = document.createElement('style');
    style.textContent = `
        .emoji-reactions {
            margin-top: 30px;
            text-align: center;
            padding: 15px;
            background-color: #f7f5ff;
            border-radius: 12px;
            display: none;
        }

        .emoji-reactions.show {
            display: block;
            animation: fadeIn 0.5s;
        }

        .emoji-title {
            display: block;
            margin-bottom: 10px;
            font-size: 1rem;
            color: #5a208f;
        }

        .emoji-buttons {
            display: flex;
            justify-content: center;
            gap: 15px;
        }

        .emoji-btn {
            font-size: 1.8rem;
            background: none;
            border: 2px solid transparent;
            border-radius: 50%;
            padding: 5px;
            cursor: pointer;
            transition: transform 0.2s, border-color 0.2s;
        }

        .emoji-btn:hover {
            transform: scale(1.2);
            border-color: #7e57c2;
        }

        .emoji-btn.selected {
            border-color: #7e57c2;
            background-color: #f0e6ff;
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
    `;
    document.head.appendChild(style);

    // Show emoji reactions when near the end of the story
    function updateEmojiDisplay() {
        if (currentPage >= Math.floor(storyPages.length * 0.75)) {
            emojiContainer.classList.add('show');
        } else {
            emojiContainer.classList.remove('show');
        }
    }

    // Add event listener to track page changes for emoji display
    const originalDisplayPage = displayPage;
    displayPage = function(pageIndex) {
        originalDisplayPage(pageIndex);
        updateEmojiDisplay();
    };

    // Add event listeners to emoji buttons
    document.querySelectorAll('.emoji-btn').forEach(button => {
        button.addEventListener('click', function() {
            // Remove selected class from all buttons
            document.querySelectorAll('.emoji-btn').forEach(btn => {
                btn.classList.remove('selected');
            });

            // Add selected class to clicked button
            this.classList.add('selected');

            // Get the story ID
            const storyId = storySelect ? storySelect.value : 
                            document.querySelector('.read-book-btn[data-book-id]')?.getAttribute('data-book-id');

            if (storyId) {
                // Track emotional feedback
                fetch('/api/track-event', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        event_type: 'emotional_feedback',
                        event_name: 'story_reaction',
                        event_data: {
                            content_type: 'story',
                            content_id: storyId,
                            emotion: this.getAttribute('data-emotion')
                        }
                    })
                })
                .catch(error => console.error('Error tracking emotion:', error));
            }
        });
    });

    // Check for query parameters to load a story directly
    const urlParams = new URLSearchParams(window.location.search);
    const storyParam = urlParams.get('story');

    if (storyParam) {
        // If using dropdown, select the option
        if (storySelect) {
            storySelect.value = storyParam;
        }

        // Load the story
        loadStoryById(storyParam);
    }
});
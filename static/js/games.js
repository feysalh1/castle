/**
 * Games functionality for Children's Castle
 * Handles game mode and all interactive games
 */

document.addEventListener('DOMContentLoaded', function() {
    // Game mode elements
    const tabButtons = document.querySelectorAll('.tab-btn');
    const gameGrids = document.querySelectorAll('.game-grid');
    const gameCards = document.querySelectorAll('.game-card:not(.external)');
    const externalGameCards = document.querySelectorAll('.game-card.external');
    const gamePlayContainer = document.getElementById('game-play-container');
    const gameContent = document.getElementById('game-content');
    const currentGameTitle = document.getElementById('current-game-title');
    const closeGameBtn = document.getElementById('close-game-btn');

    // Initialize game settings
    const gameSettings = loadExternalGameSettings();
    
    // Initialize game tabs
    if (tabButtons.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Update active tab
                tabButtons.forEach(btn => btn.classList.remove('active'));
                this.classList.add('active');
                
                // Show the corresponding game grid
                const category = this.getAttribute('data-category');
                gameGrids.forEach(grid => {
                    if (grid.classList.contains(`${category}-games`)) {
                        grid.style.display = 'grid';
                    } else {
                        grid.style.display = 'none';
                    }
                });
                
                // Hide the game play container if it's visible
                if (gamePlayContainer) {
                    gamePlayContainer.style.display = 'none';
                }
            });
        });
    }
    
    // Game card clicks
    if (gameCards.length > 0) {
        gameCards.forEach(card => {
            card.addEventListener('click', function() {
                const gameId = this.getAttribute('data-game-id');
                const gameTitle = this.querySelector('h3').textContent;
                
                showLoading();
                
                // Hide all game grids
                gameGrids.forEach(grid => {
                    grid.style.display = 'none';
                });
                
                // Show game play container
                if (gamePlayContainer) {
                    gamePlayContainer.style.display = 'block';
                    currentGameTitle.textContent = gameTitle;
                }
                
                // Load the game
                loadGame(gameId);
                
                // Track this in the database
                trackProgress(gameId, 'game', false);
                
                hideLoading();
            });
        });
    }
    
    // External game card clicks
    if (externalGameCards.length > 0) {
        externalGameCards.forEach(card => {
            card.addEventListener('click', function() {
                const externalUrl = this.getAttribute('data-external-url');
                const externalTitle = this.getAttribute('data-external-title');
                
                // Check parent settings
                if (gameSettings.parentalControlsEnabled) {
                    showParentalControls(externalUrl, externalTitle);
                } else {
                    loadExternalGame(externalUrl, externalTitle);
                }
            });
        });
    }
    
    // Close game button
    if (closeGameBtn) {
        closeGameBtn.addEventListener('click', function() {
            // Hide game play container
            gamePlayContainer.style.display = 'none';
            
            // Show the appropriate game grid based on active tab
            const activeTab = document.querySelector('.tab-btn.active');
            if (activeTab) {
                const category = activeTab.getAttribute('data-category');
                
                gameGrids.forEach(grid => {
                    if (grid.classList.contains(`${category}-games`)) {
                        grid.style.display = 'grid';
                    }
                });
            } else {
                // Show the first grid if no active tab
                if (gameGrids.length > 0) {
                    gameGrids[0].style.display = 'grid';
                }
            }
            
            // Clear game content
            if (gameContent) {
                gameContent.innerHTML = '';
            }
        });
    }
    
    // Initialize games
    initGames();
});

/**
 * Load external game settings from localStorage
 */
function loadExternalGameSettings() {
    const defaultSettings = {
        parentalControlsEnabled: true,
        ageFilter: 4
    };
    
    const savedSettings = localStorage.getItem('childrensCastleGameSettings');
    return savedSettings ? JSON.parse(savedSettings) : defaultSettings;
}

/**
 * Save external game settings to localStorage
 */
function saveExternalGameSettings(settings) {
    localStorage.setItem('childrensCastleGameSettings', JSON.stringify(settings));
}

/**
 * Initialize games functionality
 */
function initGames() {
    // Set up window resize handler for game iframes
    window.addEventListener('resize', adjustIframeHeight);
    
    // Add click feedback to all interactive elements
    addClickFeedback('.game-card');
    addClickFeedback('.tab-btn');
    addClickFeedback('.close-btn');
}

/**
 * Switch between game sources (internal vs external)
 */
function switchGameSource(source) {
    const gameSettings = loadExternalGameSettings();
    gameSettings.gameSource = source;
    saveExternalGameSettings(gameSettings);
    
    document.querySelectorAll('.source-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelector(`.source-tab[data-source="${source}"]`).classList.add('active');
    
    document.querySelectorAll('.games-container').forEach(container => {
        container.style.display = 'none';
    });
    
    document.getElementById(`${source}-games`).style.display = 'block';
}

/**
 * Show parental controls overlay
 */
function showParentalControls(externalUrl, externalTitle) {
    const overlay = document.createElement('div');
    overlay.className = 'parental-controls-overlay';
    
    const content = document.createElement('div');
    content.className = 'parental-controls-content';
    
    content.innerHTML = `
        <h3>Parental Confirmation</h3>
        <p>Your child is trying to visit an external website:</p>
        <p class="external-site">${externalTitle}</p>
        <p>Please confirm this is allowed.</p>
        <div class="pc-actions">
            <button id="pc-cancel-btn" class="btn outline-btn">Cancel</button>
            <button id="pc-approve-btn" class="btn">Approve</button>
        </div>
    `;
    
    overlay.appendChild(content);
    document.body.appendChild(overlay);
    
    // Button actions
    document.getElementById('pc-cancel-btn').addEventListener('click', function() {
        overlay.remove();
    });
    
    document.getElementById('pc-approve-btn').addEventListener('click', function() {
        overlay.remove();
        loadExternalGame(externalUrl, externalTitle);
    });
}

/**
 * Filter games by age
 */
function filterGamesByAge(ageFilter) {
    const gameSettings = loadExternalGameSettings();
    gameSettings.ageFilter = ageFilter;
    saveExternalGameSettings(gameSettings);
    
    document.querySelectorAll('.age-tab').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelector(`.age-tab[data-age="${ageFilter}"]`).classList.add('active');
    
    document.querySelectorAll('.game-card').forEach(game => {
        const gameAge = parseInt(game.getAttribute('data-age') || '0');
        
        if (gameAge <= ageFilter) {
            game.style.display = 'block';
        } else {
            game.style.display = 'none';
        }
    });
}

/**
 * Load an external game in an iframe
 */
function loadExternalGame(url, title) {
    // Track this in the database
    trackProgress(`external_${title.replace(/\s+/g, '_').toLowerCase()}`, 'game', false);
    
    // Open in a new tab
    window.open(url, '_blank');
}

/**
 * Load a game into the game container
 */
function loadGame(gameId) {
    const gameContent = document.getElementById('game-content');
    if (!gameContent) return;
    
    // Clear the container
    gameContent.innerHTML = '';
    
    // Load different games based on ID
    switch (gameId) {
        case 'matching_shapes':
            loadShapeMatchGame(gameContent);
            break;
        case 'letter_match':
            loadLetterMatchGame(gameContent);
            break;
        case 'number_game':
            loadNumberGame(gameContent);
            break;
        case 'memory_game':
            loadMemoryGame(gameContent);
            break;
        case 'coloring':
            // Placeholder for coloring game
            gameContent.innerHTML = '<div class="game-placeholder"><p>The coloring game is under construction. Check back soon!</p></div>';
            break;
        case 'animal_sounds':
            // Placeholder for animal sounds game
            gameContent.innerHTML = '<div class="game-placeholder"><p>The animal sounds game is under construction. Check back soon!</p></div>';
            break;
        case 'counting':
            // Simplified counting game (similar to number game but simpler)
            loadNumberGame(gameContent, true); // Simple version
            break;
        case 'puzzle':
            // Placeholder for puzzle game
            gameContent.innerHTML = '<div class="game-placeholder"><p>The puzzle game is under construction. Check back soon!</p></div>';
            break;
        default:
            gameContent.innerHTML = '<div class="game-placeholder"><p>This game is under construction. Check back soon!</p></div>';
    }
}

/**
 * Load the shape matching game
 */
function loadShapeMatchGame(container) {
    const shapes = ['circle', 'square', 'triangle', 'rectangle', 'star'];
    const gameArea = document.createElement('div');
    gameArea.className = 'shape-match-game';
    
    // Create game instructions
    const instructions = document.createElement('p');
    instructions.textContent = 'Drag the shapes to their matching outlines!';
    gameArea.appendChild(instructions);
    
    // Create drop targets
    const dropArea = document.createElement('div');
    dropArea.className = 'shape-drop-area';
    
    shapes.forEach(shape => {
        const target = document.createElement('div');
        target.className = `shape-target ${shape}-target`;
        target.setAttribute('data-shape', shape);
        dropArea.appendChild(target);
    });
    
    gameArea.appendChild(dropArea);
    
    // Create draggable shapes
    const shapesArea = document.createElement('div');
    shapesArea.className = 'shape-drag-area';
    
    // Shuffle shapes
    const shuffledShapes = [...shapes].sort(() => Math.random() - 0.5);
    
    shuffledShapes.forEach(shape => {
        const dragShape = document.createElement('div');
        dragShape.className = `shape-draggable ${shape}-shape`;
        dragShape.setAttribute('data-shape', shape);
        dragShape.setAttribute('draggable', 'true');
        shapesArea.appendChild(dragShape);
        
        // Add drag functionality
        dragShape.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', shape);
        });
    });
    
    gameArea.appendChild(shapesArea);
    
    // Add drop functionality to targets
    const targets = dropArea.querySelectorAll('.shape-target');
    targets.forEach(target => {
        target.addEventListener('dragover', function(e) {
            e.preventDefault();
        });
        
        target.addEventListener('drop', function(e) {
            e.preventDefault();
            const shapeName = e.dataTransfer.getData('text/plain');
            const targetShape = this.getAttribute('data-shape');
            
            if (shapeName === targetShape) {
                // Correct match
                this.classList.add('matched');
                
                // Find and hide the draggable shape
                const draggedShape = document.querySelector(`.shape-draggable[data-shape="${shapeName}"]`);
                if (draggedShape) {
                    draggedShape.style.visibility = 'hidden';
                }
                
                // Play success sound
                playSuccessSound();
                
                // Check if game is complete
                const allMatched = document.querySelectorAll('.shape-target.matched').length === shapes.length;
                if (allMatched) {
                    setTimeout(() => {
                        // Show completion message
                        createConfetti();
                        alert('Great job! You matched all the shapes!');
                        completeGame('matching_shapes');
                    }, 500);
                }
            }
        });
    });
    
    container.appendChild(gameArea);
}

/**
 * Load the letter matching game
 */
function loadLetterMatchGame(container) {
    const letters = ['A', 'B', 'C', 'D', 'E'];
    const gameArea = document.createElement('div');
    gameArea.className = 'letter-match-game';
    
    // Create game instructions
    const instructions = document.createElement('p');
    instructions.textContent = 'Match the uppercase letters with their lowercase pairs!';
    gameArea.appendChild(instructions);
    
    // Create the game board
    const gameBoard = document.createElement('div');
    gameBoard.className = 'letter-game-board';
    
    // Create uppercase letters (targets)
    const upperRow = document.createElement('div');
    upperRow.className = 'letter-row upper-row';
    
    letters.forEach(letter => {
        const upperLetter = document.createElement('div');
        upperLetter.className = 'letter-target';
        upperLetter.setAttribute('data-letter', letter);
        upperLetter.textContent = letter;
        upperRow.appendChild(upperLetter);
    });
    
    gameBoard.appendChild(upperRow);
    
    // Create lowercase letters (draggables)
    const lowerRow = document.createElement('div');
    lowerRow.className = 'letter-row lower-row';
    
    // Shuffle lowercase letters
    const shuffledLetters = [...letters].sort(() => Math.random() - 0.5);
    
    shuffledLetters.forEach(letter => {
        const lowerLetter = document.createElement('div');
        lowerLetter.className = 'letter-draggable';
        lowerLetter.setAttribute('data-letter', letter);
        lowerLetter.setAttribute('draggable', 'true');
        lowerLetter.textContent = letter.toLowerCase();
        lowerRow.appendChild(lowerLetter);
        
        // Add drag functionality
        lowerLetter.addEventListener('dragstart', function(e) {
            e.dataTransfer.setData('text/plain', letter);
        });
    });
    
    gameBoard.appendChild(lowerRow);
    gameArea.appendChild(gameBoard);
    
    // Add drop functionality to targets
    const targets = upperRow.querySelectorAll('.letter-target');
    targets.forEach(target => {
        target.addEventListener('dragover', function(e) {
            e.preventDefault();
        });
        
        target.addEventListener('drop', function(e) {
            e.preventDefault();
            const letterDragged = e.dataTransfer.getData('text/plain');
            const targetLetter = this.getAttribute('data-letter');
            
            if (letterDragged === targetLetter) {
                // Correct match
                this.classList.add('matched');
                
                // Find and hide the draggable letter
                const draggedLetter = document.querySelector(`.letter-draggable[data-letter="${letterDragged}"]`);
                if (draggedLetter) {
                    draggedLetter.style.visibility = 'hidden';
                }
                
                // Play success sound
                playSuccessSound();
                
                // Check if game is complete
                const allMatched = document.querySelectorAll('.letter-target.matched').length === letters.length;
                if (allMatched) {
                    setTimeout(() => {
                        // Show completion message
                        createConfetti();
                        alert('Great job! You matched all the letters!');
                        completeGame('letter_match');
                    }, 500);
                }
            }
        });
    });
    
    container.appendChild(gameArea);
}

/**
 * Load the number game
 */
function loadNumberGame(container, simpleMode = false) {
    const gameArea = document.createElement('div');
    gameArea.className = 'number-game';
    
    // Create game instructions
    const instructions = document.createElement('p');
    instructions.textContent = simpleMode ? 
        'Count the objects and select the correct number!' :
        'Solve the simple math problems!';
    gameArea.appendChild(instructions);
    
    // Set up game state
    let correctAnswers = 0;
    const maxRounds = 5;
    let currentRound = 1;
    
    // Create game content
    function createProblem() {
        const gameContent = document.createElement('div');
        gameContent.className = 'number-game-content';
        
        if (simpleMode) {
            // Simple counting game
            // Generate random number of objects (1-5)
            const objectCount = Math.floor(Math.random() * 5) + 1;
            
            // Create objects container
            const objectsContainer = document.createElement('div');
            objectsContainer.className = 'objects-container';
            
            // Add objects
            for (let i = 0; i < objectCount; i++) {
                const object = document.createElement('div');
                object.className = 'counting-object';
                objectsContainer.appendChild(object);
            }
            
            gameContent.appendChild(objectsContainer);
            
            // Create number options
            const numbersContainer = document.createElement('div');
            numbersContainer.className = 'numbers-container';
            
            // Generate 3 options (including the correct answer)
            const options = [objectCount];
            
            // Add 2 more unique options
            while (options.length < 3) {
                const option = Math.floor(Math.random() * 5) + 1;
                if (!options.includes(option)) {
                    options.push(option);
                }
            }
            
            // Shuffle options
            options.sort(() => Math.random() - 0.5);
            
            // Create number buttons
            options.forEach(number => {
                const numberButton = document.createElement('button');
                numberButton.className = 'number-option';
                numberButton.textContent = number;
                
                numberButton.addEventListener('click', function() {
                    if (parseInt(this.textContent) === objectCount) {
                        // Correct answer
                        this.classList.add('correct');
                        playSuccessSound();
                        correctAnswers++;
                        
                        setTimeout(() => {
                            // Move to next round or complete game
                            if (currentRound < maxRounds) {
                                currentRound++;
                                gameArea.removeChild(gameContent);
                                createProblem();
                            } else {
                                // Game complete
                                completeNumberGame();
                            }
                        }, 1000);
                    } else {
                        // Incorrect answer
                        this.classList.add('incorrect');
                        setTimeout(() => {
                            this.classList.remove('incorrect');
                        }, 500);
                    }
                });
                
                numbersContainer.appendChild(numberButton);
            });
            
            gameContent.appendChild(numbersContainer);
        } else {
            // Math game (addition/subtraction)
            const operation = Math.random() > 0.5 ? '+' : '-';
            let num1, num2, answer;
            
            if (operation === '+') {
                // Addition (result max 10)
                num1 = Math.floor(Math.random() * 5) + 1;
                num2 = Math.floor(Math.random() * 5) + 1;
                answer = num1 + num2;
            } else {
                // Subtraction (ensure positive result)
                num1 = Math.floor(Math.random() * 5) + 6; // 6-10
                num2 = Math.floor(Math.random() * 5) + 1; // 1-5
                answer = num1 - num2;
            }
            
            // Create problem display
            const problemDisplay = document.createElement('div');
            problemDisplay.className = 'math-problem';
            problemDisplay.innerHTML = `<span>${num1}</span> <span>${operation}</span> <span>${num2}</span> <span>=</span> <span>?</span>`;
            gameContent.appendChild(problemDisplay);
            
            // Create answer options
            const answersContainer = document.createElement('div');
            answersContainer.className = 'numbers-container';
            
            // Generate 3 options (including the correct answer)
            const options = [answer];
            
            // Add 2 more unique options (within reasonable range)
            while (options.length < 3) {
                const offset = Math.floor(Math.random() * 5) - 2; // -2 to +2
                const option = answer + offset;
                if (!options.includes(option) && option >= 0 && option <= 10) {
                    options.push(option);
                }
            }
            
            // Shuffle options
            options.sort(() => Math.random() - 0.5);
            
            // Create answer buttons
            options.forEach(number => {
                const numberButton = document.createElement('button');
                numberButton.className = 'number-option';
                numberButton.textContent = number;
                
                numberButton.addEventListener('click', function() {
                    if (parseInt(this.textContent) === answer) {
                        // Correct answer
                        this.classList.add('correct');
                        playSuccessSound();
                        correctAnswers++;
                        
                        setTimeout(() => {
                            // Move to next round or complete game
                            if (currentRound < maxRounds) {
                                currentRound++;
                                gameArea.removeChild(gameContent);
                                createProblem();
                            } else {
                                // Game complete
                                completeNumberGame();
                            }
                        }, 1000);
                    } else {
                        // Incorrect answer
                        this.classList.add('incorrect');
                        setTimeout(() => {
                            this.classList.remove('incorrect');
                        }, 500);
                    }
                });
                
                answersContainer.appendChild(numberButton);
            });
            
            gameContent.appendChild(answersContainer);
        }
        
        // Add progress indicator
        const progressIndicator = document.createElement('div');
        progressIndicator.className = 'game-progress';
        progressIndicator.textContent = `Question ${currentRound} of ${maxRounds}`;
        gameContent.appendChild(progressIndicator);
        
        gameArea.appendChild(gameContent);
    }
    
    function completeNumberGame() {
        // Determine if the player passed (got more than half correct)
        const passed = correctAnswers >= Math.ceil(maxRounds / 2);
        
        // Create completion message
        const completionMessage = document.createElement('div');
        completionMessage.className = 'game-completion';
        
        if (passed) {
            createConfetti();
            playSuccessSound();
            
            completionMessage.innerHTML = `
                <h3>Great job!</h3>
                <p>You got ${correctAnswers} out of ${maxRounds} correct!</p>
                <div class="completion-stars">
                    ${Array(Math.ceil(correctAnswers / maxRounds * 5)).fill('<span class="star">⭐</span>').join('')}
                </div>
            `;
            
            // Mark game as complete
            completeGame(simpleMode ? 'counting' : 'number_game');
        } else {
            completionMessage.innerHTML = `
                <h3>Good try!</h3>
                <p>You got ${correctAnswers} out of ${maxRounds} correct.</p>
                <p>Keep practicing!</p>
                <button class="btn primary-btn retry-btn">Try Again</button>
            `;
            
            // Add retry button functionality
            setTimeout(() => {
                const retryBtn = completionMessage.querySelector('.retry-btn');
                if (retryBtn) {
                    retryBtn.addEventListener('click', function() {
                        // Reset game
                        correctAnswers = 0;
                        currentRound = 1;
                        gameArea.innerHTML = '';
                        gameArea.appendChild(instructions);
                        createProblem();
                    });
                }
            }, 100);
        }
        
        gameArea.innerHTML = '';
        gameArea.appendChild(completionMessage);
    }
    
    // Start the first problem
    createProblem();
    
    container.appendChild(gameArea);
}

/**
 * Load the memory matching game
 */
function loadMemoryGame(container) {
    const gameArea = document.createElement('div');
    gameArea.className = 'memory-game';
    
    // Create game instructions
    const instructions = document.createElement('p');
    instructions.textContent = 'Find matching pairs of cards!';
    gameArea.appendChild(instructions);
    
    // Create game grid
    const gameGrid = document.createElement('div');
    gameGrid.className = 'memory-game-grid';
    
    // Define card types (pairs)
    const cardTypes = ['🐶', '🐱', '🐭', '🐰', '🦊', '🐻', '🐼', '🐨'];
    
    // Create pairs of cards
    const cardsArray = [...cardTypes, ...cardTypes];
    
    // Shuffle cards
    cardsArray.sort(() => Math.random() - 0.5);
    
    // Game variables
    let hasFlippedCard = false;
    let lockBoard = false;
    let firstCard, secondCard;
    let matchedPairs = 0;
    
    // Create cards
    cardsArray.forEach((type, index) => {
        const card = document.createElement('div');
        card.className = 'memory-card';
        card.setAttribute('data-card', type);
        
        const cardFront = document.createElement('div');
        cardFront.className = 'card-front';
        cardFront.textContent = '?';
        
        const cardBack = document.createElement('div');
        cardBack.className = 'card-back';
        cardBack.textContent = type;
        
        card.appendChild(cardFront);
        card.appendChild(cardBack);
        
        // Add click event
        card.addEventListener('click', flipCard);
        
        gameGrid.appendChild(card);
    });
    
    gameArea.appendChild(gameGrid);
    container.appendChild(gameArea);
    
    function flipCard() {
        if (lockBoard) return;
        if (this === firstCard) return;
        
        this.classList.add('flipped');
        
        if (!hasFlippedCard) {
            // First card flipped
            hasFlippedCard = true;
            firstCard = this;
            return;
        }
        
        // Second card flipped
        secondCard = this;
        checkForMatch();
    }
    
    function checkForMatch() {
        const isMatch = firstCard.getAttribute('data-card') === secondCard.getAttribute('data-card');
        isMatch ? disableCards() : unflipCards();
    }
    
    function disableCards() {
        firstCard.removeEventListener('click', flipCard);
        secondCard.removeEventListener('click', flipCard);
        
        firstCard.classList.add('matched');
        secondCard.classList.add('matched');
        
        playSuccessSound();
        matchedPairs++;
        
        if (matchedPairs === cardTypes.length) {
            setTimeout(() => {
                createConfetti();
                alert('Great job! You found all the matches!');
                completeGame('memory_game');
            }, 500);
        }
        
        resetBoard();
    }
    
    function unflipCards() {
        lockBoard = true;
        
        setTimeout(() => {
            firstCard.classList.remove('flipped');
            secondCard.classList.remove('flipped');
            resetBoard();
        }, 1000);
    }
    
    function resetBoard() {
        [hasFlippedCard, lockBoard] = [false, false];
        [firstCard, secondCard] = [null, null];
    }
}

/**
 * Mark a game as complete
 */
function completeGame(gameId) {
    // Track progress in the database
    trackProgress(gameId, 'game', true);
    
    // Play success sound
    playSuccessSound();
    
    // Award badge if rewards.js is loaded
    if (typeof awardBadge === 'function') {
        awardBadge(`game_${gameId}`);
    }
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
 * Adjust iframe height based on window size
 */
function adjustIframeHeight() {
    const iframes = document.querySelectorAll('.game-iframe');
    iframes.forEach(iframe => {
        iframe.style.height = `${window.innerHeight * 0.7}px`;
    });
}

/**
 * Play success sound
 */
function playSuccessSound() {
    const audio = document.getElementById('game-audio');
    if (audio) {
        audio.src = "/static/audio/success.mp3";
        audio.play();
    }
}

/**
 * Create confetti animation effect
 */
function createConfetti() {
    const confettiContainer = document.createElement('div');
    confettiContainer.className = 'confetti-container';
    document.body.appendChild(confettiContainer);
    
    // Create confetti pieces
    for (let i = 0; i < 50; i++) {
        const confetti = document.createElement('div');
        confetti.className = 'confetti';
        confetti.style.left = `${Math.random() * 100}%`;
        confetti.style.animationDelay = `${Math.random() * 2}s`;
        confetti.style.backgroundColor = `hsl(${Math.random() * 360}, 100%, 50%)`;
        confettiContainer.appendChild(confetti);
    }
    
    // Remove confetti after animation
    setTimeout(() => {
        confettiContainer.remove();
    }, 4000);
}

/**
 * Add click feedback to interactive elements
 */
function addClickFeedback(selector) {
    document.querySelectorAll(selector).forEach(element => {
        element.addEventListener('click', function() {
            this.classList.add('clicked');
            setTimeout(() => {
                this.classList.remove('clicked');
            }, 150);
        });
    });
}

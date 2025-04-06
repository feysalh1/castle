// Games Management

// Constants
const GAMES_BY_AGE = {
    4: [
        { id: 'animal_puzzle', title: 'Animal Puzzle', description: 'Match animal pieces together' },
        { id: 'coloring_fun', title: 'Coloring Fun', description: 'Color cute pictures' },
        { id: 'shape_match', title: 'Shape Match', description: 'Match shapes and colors' }
    ],
    5: [
        { id: 'letter_match', title: 'Letter Match', description: 'Match uppercase and lowercase letters' },
        { id: 'number_fun', title: 'Number Fun', description: 'Count and match numbers' },
        { id: 'memory_game', title: 'Memory Game', description: 'Find matching pairs' }
    ]
};

// External educational games that are safe for children
const EXTERNAL_GAMES = {
    4: [
        { id: 'abcya_shapes', title: 'Shape Matching', url: 'https://www.abcya.com/games/shapes_colors_bingo', description: 'Learn shapes and colors', enabled: true },
        { id: 'pbs_games', title: 'PBS Kids Games', url: 'https://pbskids.org/games/all-topics/', description: 'Educational games from PBS Kids', enabled: true },
        { id: 'sesame_street', title: 'Sesame Street Games', url: 'https://www.sesamestreet.org/games', description: 'Play with Sesame Street characters', enabled: true }
    ],
    5: [
        { id: 'starfall', title: 'Starfall', url: 'https://www.starfall.com/h/index-kindergarten.php', description: 'Learn to read games', enabled: true },
        { id: 'funbrain', title: 'Funbrain Jr', url: 'https://www.funbrain.com/pre-k-and-k-playground', description: 'Math and reading games', enabled: true },
        { id: 'national_geographic', title: 'National Geographic Kids', url: 'https://kids.nationalgeographic.com/games/', description: 'Science and nature games', enabled: true }
    ]
};

// Load enabled status from localStorage if available
function loadExternalGameSettings() {
    const savedSettings = localStorage.getItem('babyGirlExternalGameSettings');
    if (savedSettings) {
        const settings = JSON.parse(savedSettings);
        
        // Update enabled status for each game
        Object.keys(EXTERNAL_GAMES).forEach(ageGroup => {
            EXTERNAL_GAMES[ageGroup].forEach(game => {
                if (settings[game.id] !== undefined) {
                    game.enabled = settings[game.id];
                }
            });
        });
    }
}

// Save enabled status to localStorage
function saveExternalGameSettings() {
    const settings = {};
    
    // Collect enabled status for each game
    Object.keys(EXTERNAL_GAMES).forEach(ageGroup => {
        EXTERNAL_GAMES[ageGroup].forEach(game => {
            settings[game.id] = game.enabled;
        });
    });
    
    localStorage.setItem('babyGirlExternalGameSettings', JSON.stringify(settings));
}

// Current game state
let currentGame = null;
let currentAgeFilter = 4; // Default to age 4
let gameSource = 'internal'; // 'internal' or 'external'

// Initialize game section
function initGames() {
    // Load external game settings
    loadExternalGameSettings();
    
    // Set up age filter buttons
    document.getElementById('age-4-btn')?.addEventListener('click', () => filterGamesByAge(4));
    document.getElementById('age-5-btn')?.addEventListener('click', () => filterGamesByAge(5));
    
    // Set up game source buttons
    document.getElementById('internal-games-btn')?.addEventListener('click', () => switchGameSource('internal'));
    document.getElementById('external-games-btn')?.addEventListener('click', () => switchGameSource('external'));
    
    // Set up parental controls button
    document.getElementById('parental-controls-btn')?.addEventListener('click', showParentalControls);
    
    // Init with age 4 internal games
    filterGamesByAge(4);
}

// Switch between internal and external games
function switchGameSource(source) {
    gameSource = source;
    
    // Update active button
    document.querySelectorAll('.source-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const activeBtn = document.getElementById(`${source}-games-btn`);
    if (activeBtn) {
        activeBtn.classList.add('active');
    }
    
    // Re-filter games with current age
    filterGamesByAge(currentAgeFilter);
}

// Show parental controls modal
function showParentalControls() {
    // Create modal background
    const modalBackground = document.createElement('div');
    modalBackground.className = 'modal-background';
    
    // Create modal container
    const modalContainer = document.createElement('div');
    modalContainer.className = 'modal-container';
    modalContainer.innerHTML = `
        <h3>Parental Controls</h3>
        <p>Enable or disable external websites. Disabled sites won't be shown to your child.</p>
        <div class="parental-controls-content">
            <h4>Age 4 Games</h4>
            <div id="age-4-controls" class="controls-list"></div>
            
            <h4>Age 5+ Games</h4>
            <div id="age-5-controls" class="controls-list"></div>
        </div>
        <div class="modal-buttons">
            <button id="save-controls-btn" class="btn btn-primary">Save Settings</button>
            <button id="close-controls-btn" class="btn btn-secondary">Close</button>
        </div>
    `;
    
    // Add to body
    modalBackground.appendChild(modalContainer);
    document.body.appendChild(modalBackground);
    
    // Populate controls for each age group
    [4, 5].forEach(age => {
        const controlsList = document.getElementById(`age-${age}-controls`);
        if (!controlsList) return;
        
        EXTERNAL_GAMES[age].forEach(game => {
            const controlItem = document.createElement('div');
            controlItem.className = 'control-item';
            controlItem.innerHTML = `
                <label>
                    <input type="checkbox" data-game-id="${game.id}" ${game.enabled ? 'checked' : ''}>
                    ${game.title} - ${game.description}
                </label>
            `;
            controlsList.appendChild(controlItem);
        });
    });
    
    // Set up event listeners
    document.getElementById('save-controls-btn')?.addEventListener('click', () => {
        // Save all checkbox states
        document.querySelectorAll('.control-item input[type="checkbox"]').forEach(checkbox => {
            const gameId = checkbox.getAttribute('data-game-id');
            
            // Find and update the game
            Object.keys(EXTERNAL_GAMES).forEach(ageGroup => {
                EXTERNAL_GAMES[ageGroup].forEach(game => {
                    if (game.id === gameId) {
                        game.enabled = checkbox.checked;
                    }
                });
            });
        });
        
        // Save settings
        saveExternalGameSettings();
        
        // Refresh games list
        filterGamesByAge(currentAgeFilter);
        
        // Close modal
        document.body.removeChild(modalBackground);
    });
    
    document.getElementById('close-controls-btn')?.addEventListener('click', () => {
        document.body.removeChild(modalBackground);
    });
}

// Filter games by age
function filterGamesByAge(ageFilter) {
    currentAgeFilter = ageFilter;
    
    // Update active button
    document.querySelectorAll('.age-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    const ageBtn = document.getElementById(`age-${ageFilter}-btn`);
    if (ageBtn) {
        ageBtn.classList.add('active');
    }
    
    // Get games list container
    const gamesListContainer = document.getElementById('games-list');
    if (!gamesListContainer) return;
    
    gamesListContainer.innerHTML = '';
    
    if (gameSource === 'internal') {
        // Display internal games
        const games = GAMES_BY_AGE[ageFilter] || [];
        
        if (games.length === 0) {
            gamesListContainer.innerHTML = '<p>No games available for this age.</p>';
            return;
        }
        
        // Create game cards for internal games
        games.forEach(game => {
            const gameCard = document.createElement('div');
            gameCard.className = 'game-card';
            gameCard.innerHTML = `
                <div class="game-icon">🎮</div>
                <h3>${game.title}</h3>
                <p>${game.description}</p>
                <button class="play-game-btn" data-game-id="${game.id}">Play</button>
            `;
            
            gamesListContainer.appendChild(gameCard);
            
            // Add event listener to play button
            const playButton = gameCard.querySelector('.play-game-btn');
            playButton.addEventListener('click', () => loadGame(game.id));
        });
    } else {
        // Display only enabled external games
        const externalGames = (EXTERNAL_GAMES[ageFilter] || []).filter(game => game.enabled);
        
        if (externalGames.length === 0) {
            gamesListContainer.innerHTML = '<p>No external games available for this age. Parents can enable games in Parental Controls.</p>';
            return;
        }
        
        // Create game cards for external games
        externalGames.forEach(game => {
            const gameCard = document.createElement('div');
            gameCard.className = 'game-card external-game';
            gameCard.innerHTML = `
                <div class="game-icon">🌐</div>
                <h3>${game.title}</h3>
                <p>${game.description}</p>
                <button class="play-external-btn" data-game-url="${game.url}">Play</button>
            `;
            
            gamesListContainer.appendChild(gameCard);
            
            // Add event listener to play button
            const playButton = gameCard.querySelector('.play-external-btn');
            playButton.addEventListener('click', () => {
                loadExternalGame(game.url, game.title);
            });
        });
    }
}

// Load an external game
function loadExternalGame(url, title) {
    const gameContentContainer = document.getElementById('game-content-container');
    if (!gameContentContainer) return;
    
    // Hide games list, show game content
    const gamesListContainer = document.getElementById('games-list-container');
    if (gamesListContainer) {
        gamesListContainer.style.display = 'none';
    }
    
    gameContentContainer.style.display = 'block';
    
    // Clear previous game content
    gameContentContainer.innerHTML = '';
    
    // Create iframe for external game with parent message
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content external-game-content';
    gameContent.innerHTML = `
        <h3>${title}</h3>
        <div class="parent-message">
            <p><strong>Parents:</strong> This is an external educational website. You can manage which sites are available in the Parental Controls.</p>
        </div>
        <div class="external-game-container">
            <iframe 
                src="${url}"
                title="${title}"
                class="external-game-frame"
                allow="fullscreen"
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
            ></iframe>
        </div>
        <p class="game-instructions">If you can't see the game, you can use the button below to open it in a new tab.</p>
        <a href="${url}" target="_blank" class="open-external-btn">Open in New Tab</a>
    `;
    
    gameContentContainer.appendChild(gameContent);
    
    // Add back button
    const backButton = document.createElement('button');
    backButton.className = 'btn back-to-games-btn';
    backButton.innerHTML = '<i class="fas fa-arrow-left"></i> Back to Games';
    backButton.addEventListener('click', () => {
        const gamesListContainer = document.getElementById('games-list-container');
        if (gamesListContainer) {
            gamesListContainer.style.display = 'block';
        }
        gameContentContainer.style.display = 'none';
    });
    
    // Add buttons to container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'game-buttons';
    buttonContainer.appendChild(backButton);
    gameContentContainer.appendChild(buttonContainer);
}

// Load a specific internal game
function loadGame(gameId) {
    currentGame = gameId;
    
    // Hide games list, show game content
    const gamesListContainer = document.getElementById('games-list-container');
    const gameContentContainer = document.getElementById('game-content-container');
    
    if (!gamesListContainer || !gameContentContainer) return;
    
    gamesListContainer.style.display = 'none';
    gameContentContainer.style.display = 'block';
    
    // Clear previous game content
    gameContentContainer.innerHTML = '';
    
    // Load game based on ID
    switch(gameId) {
        case 'animal_puzzle':
            loadAnimalPuzzleGame(gameContentContainer);
            break;
        case 'coloring_fun':
            loadColoringGame(gameContentContainer);
            break;
        case 'shape_match':
            loadShapeMatchGame(gameContentContainer);
            break;
        case 'letter_match':
            loadLetterMatchGame(gameContentContainer);
            break;
        case 'number_fun':
            loadNumberGame(gameContentContainer);
            break;
        case 'memory_game':
            loadMemoryGame(gameContentContainer);
            break;
        default:
            gameContentContainer.innerHTML = '<p>Game not found.</p>';
            break;
    }
    
    // Add back button
    const backButton = document.createElement('button');
    backButton.className = 'btn back-to-games-btn';
    backButton.innerHTML = '<i class="fas fa-arrow-left"></i> Back to Games';
    backButton.addEventListener('click', () => {
        document.getElementById('games-list-container').style.display = 'block';
        gameContentContainer.style.display = 'none';
        currentGame = null;
    });
    
    // Add complete button
    const completeButton = document.createElement('button');
    completeButton.className = 'btn game-complete-btn';
    completeButton.textContent = 'I Finished This Game!';
    completeButton.addEventListener('click', () => completeGame(gameId));
    
    // Add buttons to container
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'game-buttons';
    buttonContainer.appendChild(backButton);
    buttonContainer.appendChild(completeButton);
    gameContentContainer.appendChild(buttonContainer);
}

// Load Animal Puzzle Game (Age 4)
function loadAnimalPuzzleGame(container) {
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content animal-puzzle';
    gameContent.innerHTML = `
        <h3>Animal Puzzle</h3>
        <p>Help put the animal puzzle together! Tap or click the pieces to rotate them.</p>
        <div class="puzzle-container">
            <div class="puzzle-pieces">
                <div class="puzzle-piece" data-emoji="🦁" onclick="this.classList.toggle('rotated')">🦁</div>
                <div class="puzzle-piece" data-emoji="🐯" onclick="this.classList.toggle('rotated')">🐯</div>
                <div class="puzzle-piece" data-emoji="🐘" onclick="this.classList.toggle('rotated')">🐘</div>
                <div class="puzzle-piece" data-emoji="🦒" onclick="this.classList.toggle('rotated')">🦒</div>
                <div class="puzzle-piece" data-emoji="🦓" onclick="this.classList.toggle('rotated')">🦓</div>
                <div class="puzzle-piece" data-emoji="🐒" onclick="this.classList.toggle('rotated')">🐒</div>
            </div>
            <div class="puzzle-board">
                <div class="puzzle-target"></div>
                <div class="puzzle-target"></div>
                <div class="puzzle-target"></div>
                <div class="puzzle-target"></div>
                <div class="puzzle-target"></div>
                <div class="puzzle-target"></div>
            </div>
        </div>
    `;
    
    container.appendChild(gameContent);
    
    // Initialize puzzle interaction
    setTimeout(() => {
        const pieces = gameContent.querySelectorAll('.puzzle-piece');
        const targets = gameContent.querySelectorAll('.puzzle-target');
        
        pieces.forEach(piece => {
            piece.addEventListener('click', () => {
                piece.classList.toggle('selected');
            });
            
            piece.addEventListener('dragstart', e => {
                e.dataTransfer.setData('text/plain', piece.getAttribute('data-emoji'));
                piece.classList.add('dragging');
            });
            
            piece.addEventListener('dragend', () => {
                piece.classList.remove('dragging');
            });
            
            // Make pieces draggable
            piece.setAttribute('draggable', 'true');
        });
        
        targets.forEach(target => {
            target.addEventListener('dragover', e => {
                e.preventDefault();
                target.classList.add('drag-over');
            });
            
            target.addEventListener('dragleave', () => {
                target.classList.remove('drag-over');
            });
            
            target.addEventListener('drop', e => {
                e.preventDefault();
                target.classList.remove('drag-over');
                if (!target.hasChildNodes()) {
                    const emoji = e.dataTransfer.getData('text/plain');
                    // Find the piece by data attribute
                    const draggedPiece = document.querySelector(`.puzzle-piece[data-emoji="${emoji}"]`);
                    if (draggedPiece) {
                        const clone = draggedPiece.cloneNode(true);
                        target.appendChild(clone);
                        draggedPiece.style.visibility = 'hidden';
                    }
                }
            });
        });
    }, 100);
}

// Load Coloring Game (Age 4)
function loadColoringGame(container) {
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content coloring-game';
    gameContent.innerHTML = `
        <h3>Coloring Fun</h3>
        <p>Color the picture! Choose a color and tap inside the areas.</p>
        <div class="color-palette">
            <div class="color-swatch" style="background-color: #FF0000;" data-color="#FF0000"></div>
            <div class="color-swatch" style="background-color: #0000FF;" data-color="#0000FF"></div>
            <div class="color-swatch" style="background-color: #008000;" data-color="#008000"></div>
            <div class="color-swatch" style="background-color: #FFFF00;" data-color="#FFFF00"></div>
            <div class="color-swatch" style="background-color: #800080;" data-color="#800080"></div>
            <div class="color-swatch" style="background-color: #FFA500;" data-color="#FFA500"></div>
        </div>
        <div class="coloring-container">
            <div class="coloring-area">
                <div class="coloring-region" data-name="sky"></div>
                <div class="coloring-region" data-name="sun"></div>
                <div class="coloring-region" data-name="ground"></div>
                <div class="coloring-region" data-name="tree"></div>
                <div class="coloring-region" data-name="house"></div>
                <div class="coloring-region" data-name="roof"></div>
            </div>
        </div>
    `;
    
    container.appendChild(gameContent);
    
    // Set up coloring game interaction
    setTimeout(() => {
        let currentColor = '#FF0000';
        
        const colorSwatches = gameContent.querySelectorAll('.color-swatch');
        const coloringRegions = gameContent.querySelectorAll('.coloring-region');
        
        colorSwatches.forEach(swatch => {
            swatch.addEventListener('click', () => {
                currentColor = swatch.getAttribute('data-color');
                colorSwatches.forEach(s => s.classList.remove('selected'));
                swatch.classList.add('selected');
            });
        });
        
        coloringRegions.forEach(region => {
            region.addEventListener('click', () => {
                region.style.backgroundColor = currentColor;
            });
        });
        
        // Select the first color by default
        colorSwatches[0].classList.add('selected');
    }, 100);
}

// Load Shape Match Game (Age 4)
function loadShapeMatchGame(container) {
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content shape-match-game';
    gameContent.innerHTML = `
        <h3>Shape Match</h3>
        <p>Drag the shapes to their matching outlines!</p>
        <div class="shape-game-container">
            <div class="shapes-to-match">
                <div class="shape circle" draggable="true">●</div>
                <div class="shape square" draggable="true">■</div>
                <div class="shape triangle" draggable="true">▲</div>
                <div class="shape star" draggable="true">★</div>
            </div>
            <div class="shape-targets">
                <div class="shape-target" data-shape="circle">○</div>
                <div class="shape-target" data-shape="square">□</div>
                <div class="shape-target" data-shape="triangle">△</div>
                <div class="shape-target" data-shape="star">☆</div>
            </div>
        </div>
    `;
    
    container.appendChild(gameContent);
    
    // Initialize shape matching
    setTimeout(() => {
        const shapes = gameContent.querySelectorAll('.shape');
        const targets = gameContent.querySelectorAll('.shape-target');
        
        shapes.forEach(shape => {
            shape.addEventListener('dragstart', e => {
                // Get shape type from class name (circle, square, etc.)
                const className = Array.from(shape.classList).find(cls => 
                    ['circle', 'square', 'triangle', 'star'].includes(cls));
                    
                e.dataTransfer.setData('text/plain', className);
                shape.classList.add('dragging');
            });
            
            shape.addEventListener('dragend', () => {
                shape.classList.remove('dragging');
            });
        });
        
        targets.forEach(target => {
            target.addEventListener('dragover', e => {
                e.preventDefault();
                target.classList.add('drag-over');
            });
            
            target.addEventListener('dragleave', () => {
                target.classList.remove('drag-over');
            });
            
            target.addEventListener('drop', e => {
                e.preventDefault();
                target.classList.remove('drag-over');
                
                const data = e.dataTransfer.getData('text/plain');
                const shapeType = target.getAttribute('data-shape');
                
                if (data === shapeType) {
                    target.classList.add('matched');
                    document.querySelector(`.shape.${shapeType}`)?.classList.add('matched');
                }
            });
        });
    }, 100);
}

// Load Letter Match Game (Age 5+)
function loadLetterMatchGame(container) {
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content letter-match';
    gameContent.innerHTML = `
        <h3>Letter Match</h3>
        <p>Match the uppercase and lowercase letters!</p>
        <div class="match-container">
            <div class="match-card" data-letter="a">A</div>
            <div class="match-card" data-letter="b">B</div>
            <div class="match-card" data-letter="c">C</div>
            <div class="match-card" data-letter="a">a</div>
            <div class="match-card" data-letter="b">b</div>
            <div class="match-card" data-letter="c">c</div>
        </div>
    `;
    
    container.appendChild(gameContent);
    
    // Initialize letter matching
    setTimeout(() => {
        const cards = gameContent.querySelectorAll('.match-card');
        let selectedCard = null;
        
        cards.forEach(card => {
            card.addEventListener('click', () => {
                card.classList.add('flipped');
                
                if (!selectedCard) {
                    // First card selected
                    selectedCard = card;
                } else {
                    // Second card selected
                    if (selectedCard.getAttribute('data-letter') === card.getAttribute('data-letter') && 
                        selectedCard !== card) {
                        // Match found
                        selectedCard.classList.add('matched');
                        card.classList.add('matched');
                    } else {
                        // No match
                        setTimeout(() => {
                            selectedCard.classList.remove('flipped');
                            card.classList.remove('flipped');
                        }, 1000);
                    }
                    selectedCard = null;
                }
            });
        });
    }, 100);
}

// Load Number Game (Age 5+)
function loadNumberGame(container) {
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content number-game';
    gameContent.innerHTML = `
        <h3>Number Fun</h3>
        <p>Count the objects and select the right number!</p>
        <div class="number-container">
            <div class="number-question">
                <div class="number-objects">🌟 🌟 🌟</div>
                <p>How many stars do you see?</p>
                <div class="number-options">
                    <button class="number-option" data-value="2">2</button>
                    <button class="number-option" data-value="3">3</button>
                    <button class="number-option" data-value="4">4</button>
                </div>
            </div>
        </div>
    `;
    
    container.appendChild(gameContent);
    
    // Initialize number game
    setTimeout(() => {
        const options = gameContent.querySelectorAll('.number-option');
        const correctAnswer = "3";
        
        options.forEach(option => {
            option.addEventListener('click', () => {
                const value = option.getAttribute('data-value');
                options.forEach(opt => opt.classList.remove('selected', 'correct', 'incorrect'));
                
                option.classList.add('selected');
                
                if (value === correctAnswer) {
                    option.classList.add('correct');
                } else {
                    option.classList.add('incorrect');
                }
            });
        });
    }, 100);
}

// Load Memory Game (Age 5+)
function loadMemoryGame(container) {
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content memory-game';
    gameContent.innerHTML = `
        <h3>Memory Game</h3>
        <p>Find the matching pairs of animals!</p>
        <div class="memory-board">
            <div class="memory-card" data-animal="cat">🐱</div>
            <div class="memory-card" data-animal="dog">🐶</div>
            <div class="memory-card" data-animal="rabbit">🐰</div>
            <div class="memory-card" data-animal="cat">🐱</div>
            <div class="memory-card" data-animal="dog">🐶</div>
            <div class="memory-card" data-animal="rabbit">🐰</div>
        </div>
    `;
    
    container.appendChild(gameContent);
    
    // Initialize memory game
    setTimeout(() => {
        const cards = gameContent.querySelectorAll('.memory-card');
        let hasFlippedCard = false;
        let lockBoard = false;
        let firstCard, secondCard;
        
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
            const isMatch = firstCard.dataset.animal === secondCard.dataset.animal;
            isMatch ? disableCards() : unflipCards();
        }
        
        function disableCards() {
            firstCard.classList.add('matched');
            secondCard.classList.add('matched');
            
            resetBoard();
        }
        
        function unflipCards() {
            lockBoard = true;
            
            setTimeout(() => {
                firstCard.classList.remove('flipped');
                secondCard.classList.remove('flipped');
                
                resetBoard();
            }, 1500);
        }
        
        function resetBoard() {
            [hasFlippedCard, lockBoard] = [false, false];
            [firstCard, secondCard] = [null, null];
        }
        
        cards.forEach(card => card.addEventListener('click', flipCard));
        
        // Shuffle cards
        cards.forEach(card => {
            const randomPosition = Math.floor(Math.random() * cards.length);
            card.style.order = randomPosition;
        });
    }, 100);
}

// Handle game completion and rewards
function completeGame(gameId) {
    // Map game IDs to badge IDs
    const badgeMap = {
        'animal_puzzle': 'puzzle_master',
        'coloring_fun': 'coloring_master',
        'shape_match': 'shape_master',
        'letter_match': 'letter_master',
        'number_fun': 'number_master',
        'memory_game': 'memory_master'
    };
    
    // Award badge if it exists in the map
    const badgeId = badgeMap[gameId];
    if (badgeId && typeof awardBadge === 'function') {
        awardBadge(badgeId);
    }
    
    // Award some stars
    if (typeof awardStars === 'function') {
        awardStars(3);
    }
    
    // Go back to games list
    document.getElementById('games-list-container').style.display = 'block';
    document.getElementById('game-content-container').style.display = 'none';
    currentGame = null;
}

// Initialize games on load
document.addEventListener('DOMContentLoaded', () => {
    // Init games if we're in game mode section
    const gameSection = document.getElementById('game-mode');
    if (gameSection) {
        initGames();
    }
});

// Function to adjust iframe height
function adjustIframeHeight() {
    // Make the iframe take up more space on the page
    const externalContainers = document.querySelectorAll('.external-game-container');
    
    if (externalContainers.length > 0) {
        // Adjust the height based on available viewport height
        const viewportHeight = window.innerHeight;
        const containerHeight = Math.max(450, viewportHeight * 0.7); // At least 450px or 70% of viewport
        
        externalContainers.forEach(container => {
            container.style.height = `${containerHeight}px`;
        });
    }
}

// Modify loadExternalGame function to include height adjustment
const originalLoadExternalGame = loadExternalGame;
loadExternalGame = function(url, title) {
    originalLoadExternalGame(url, title);
    
    // After loading the external game, adjust iframe height
    setTimeout(adjustIframeHeight, 100);
    
    // Also listen for window resize to readjust
    window.addEventListener('resize', adjustIframeHeight);
};

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Original initialization
    const gameSection = document.getElementById('game-mode');
    if (gameSection) {
        initGames();
    }
    
    // Set up fullscreen button for external games
    document.body.addEventListener('click', (e) => {
        if (e.target && e.target.classList.contains('open-external-btn')) {
            // Prevent default link behavior
            e.preventDefault();
            
            // Get the URL from the href attribute
            const url = e.target.getAttribute('href');
            
            // Open in a new tab that takes up the full screen
            window.open(url, '_blank', 'noopener,noreferrer');
        }
    });
});

// More click responsiveness improvements
document.addEventListener('DOMContentLoaded', function() {
    // Make all clickable game elements more responsive
    function addClickFeedback(selector) {
        document.querySelectorAll(selector).forEach(element => {
            element.addEventListener('click', function() {
                // Add a temporary class for visual feedback
                this.classList.add('clicked');
                
                // Remove it after animation completes
                setTimeout(() => {
                    this.classList.remove('clicked');
                }, 150);
            });
        });
    }
    
    // For dynamically added elements, use event delegation
    document.body.addEventListener('click', function(e) {
        // Check if the clicked element is one we want to add feedback to
        if (e.target.matches('.puzzle-piece, .match-card, .memory-card, .number-option')) {
            e.target.classList.add('clicked');
            
            setTimeout(() => {
                e.target.classList.remove('clicked');
            }, 150);
        }
    });
    
    // Remove any delay in the loadExternalGame and loadGame functions
    const originalLoadGame = window.loadGame;
    if (originalLoadGame) {
        window.loadGame = function(gameId) {
            // Call original function
            originalLoadGame(gameId);
            
            // Force layout recalculation to prevent delay
            document.body.offsetHeight;
        };
    }
    
    // Optimize external game loading
    if (typeof loadExternalGame === 'function') {
        const origLoadExternal = loadExternalGame;
        loadExternalGame = function(url, title) {
            // Show loading indicator
            const gameContentContainer = document.getElementById('game-content-container');
            if (gameContentContainer) {
                gameContentContainer.innerHTML = '<div class="loading-indicator">Loading game...</div>';
                gameContentContainer.style.display = 'block';
                
                // Hide games list immediately
                const gamesListContainer = document.getElementById('games-list-container');
                if (gamesListContainer) {
                    gamesListContainer.style.display = 'none';
                }
            }
            
            // Short timeout to allow UI to update before heavy iframe loading
            setTimeout(() => {
                origLoadExternal(url, title);
            }, 10);
        };
    }
});

// Add clicked class styling
document.head.insertAdjacentHTML('beforeend', `
    <style>
        .clicked {
            transform: scale(0.9) !important;
            opacity: 0.8 !important;
            transition: transform 0.1s ease, opacity 0.1s ease !important;
        }
        
        .loading-indicator {
            padding: 20px;
            text-align: center;
            font-size: 1.2rem;
            color: var(--primary-color);
        }
    </style>
`);

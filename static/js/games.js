// Games Management

// Constants
const GAMES_BY_AGE = {
    4: [
        { id: 'animal_puzzle', title: 'Animal Puzzle', description: 'Match animal pieces together' },
        { id: 'coloring_fun', title: 'Coloring Fun', description: 'Color cute pictures' }
    ],
    5: [
        { id: 'letter_match', title: 'Letter Match', description: 'Match uppercase and lowercase letters' },
        { id: 'number_fun', title: 'Number Fun', description: 'Count and match numbers' }
    ]
};

// Current game state
let currentGame = null;
let currentAgeFilter = 4; // Default to age 4

// Initialize game section
function initGames() {
    // Set up age filter buttons
    document.getElementById('age-4-btn').addEventListener('click', () => filterGamesByAge(4));
    document.getElementById('age-5-btn').addEventListener('click', () => filterGamesByAge(5));
    
    // Init with age 4 games
    filterGamesByAge(4);
}

// Filter games by age
function filterGamesByAge(ageFilter) {
    currentAgeFilter = ageFilter;
    
    // Update active button
    document.querySelectorAll('.age-filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    document.getElementById(`age-${ageFilter}-btn`).classList.add('active');
    
    // Get games list container
    const gamesListContainer = document.getElementById('games-list');
    gamesListContainer.innerHTML = '';
    
    // Populate games for the selected age
    const games = GAMES_BY_AGE[ageFilter] || [];
    
    if (games.length === 0) {
        gamesListContainer.innerHTML = '<p>No games available for this age.</p>';
        return;
    }
    
    // Create game cards
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
}

// Load a specific game
function loadGame(gameId) {
    currentGame = gameId;
    
    // Hide games list, show game content
    document.getElementById('games-list-container').style.display = 'none';
    const gameContentContainer = document.getElementById('game-content-container');
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
        case 'letter_match':
            loadLetterMatchGame(gameContentContainer);
            break;
        case 'number_fun':
            loadNumberGame(gameContentContainer);
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
        <p>Help put the animal puzzle together! Tap or click pieces to rotate them.</p>
        <div class="puzzle-container">
            <img src="/static/images/games/animal_puzzle.jpg" alt="Animal Puzzle" class="puzzle-image">
        </div>
        <p class="game-instructions">This is a simple puzzle. In a real implementation, pieces would be interactive.</p>
    `;
    
    container.appendChild(gameContent);
}

// Load Coloring Game (Age 4)
function loadColoringGame(container) {
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content coloring-game';
    gameContent.innerHTML = `
        <h3>Coloring Fun</h3>
        <p>Color the picture! Choose a color and tap inside the areas.</p>
        <div class="color-palette">
            <div class="color-swatch" style="background-color: red;"></div>
            <div class="color-swatch" style="background-color: blue;"></div>
            <div class="color-swatch" style="background-color: green;"></div>
            <div class="color-swatch" style="background-color: yellow;"></div>
            <div class="color-swatch" style="background-color: purple;"></div>
            <div class="color-swatch" style="background-color: orange;"></div>
        </div>
        <div class="coloring-container">
            <img src="/static/images/games/coloring_page.jpg" alt="Coloring Page" class="coloring-image">
        </div>
        <p class="game-instructions">This is a simple coloring page. In a real implementation, you would be able to color different areas.</p>
    `;
    
    container.appendChild(gameContent);
}

// Load Letter Match Game (Age 5+)
function loadLetterMatchGame(container) {
    const gameContent = document.createElement('div');
    gameContent.className = 'game-content letter-match';
    gameContent.innerHTML = `
        <h3>Letter Match</h3>
        <p>Match the uppercase and lowercase letters!</p>
        <div class="match-container">
            <div class="match-card">A</div>
            <div class="match-card">B</div>
            <div class="match-card">C</div>
            <div class="match-card">a</div>
            <div class="match-card">b</div>
            <div class="match-card">c</div>
        </div>
        <p class="game-instructions">This is a simple letter matching game. In a real implementation, you would be able to flip and match cards.</p>
    `;
    
    container.appendChild(gameContent);
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
                    <button class="number-option">2</button>
                    <button class="number-option">3</button>
                    <button class="number-option">4</button>
                </div>
            </div>
        </div>
        <p class="game-instructions">This is a simple counting game. In a real implementation, you would get feedback on your answer.</p>
    `;
    
    container.appendChild(gameContent);
}

// Handle game completion and rewards
function completeGame(gameId) {
    // Map game IDs to badge IDs
    const badgeMap = {
        'animal_puzzle': 'puzzle_master',
        'coloring_fun': 'coloring_master',
        'letter_match': 'letter_master',
        'number_fun': 'number_master'
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

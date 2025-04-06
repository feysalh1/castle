// Game System for Baby Girl App

// Game configurations
const games = {
    'animal-puzzle': {
        title: 'Animal Puzzle',
        age: 4,
        content: `
            <div class="game-content animal-puzzle">
                <h3>Animal Puzzle</h3>
                <p>Drag the animal pieces to complete the puzzle!</p>
                <div class="puzzle-container">
                    <img src="static/images/games/animal-puzzle.svg" alt="Animal Puzzle" class="puzzle-image">
                </div>
                <button class="action-btn game-complete-btn" onclick="completeGame('animal-puzzle')">Complete Puzzle</button>
            </div>
        `
    },
    'coloring': {
        title: 'Coloring Fun',
        age: 4,
        content: `
            <div class="game-content coloring">
                <h3>Coloring Fun</h3>
                <p>Touch the colors and then touch the picture to color it!</p>
                <div class="coloring-container">
                    <img src="static/images/games/coloring-page.svg" alt="Coloring Page" class="coloring-image">
                </div>
                <div class="color-palette">
                    <div class="color-swatch" style="background-color: red;"></div>
                    <div class="color-swatch" style="background-color: blue;"></div>
                    <div class="color-swatch" style="background-color: green;"></div>
                    <div class="color-swatch" style="background-color: yellow;"></div>
                    <div class="color-swatch" style="background-color: purple;"></div>
                </div>
                <button class="action-btn game-complete-btn" onclick="completeGame('coloring')">Finish Coloring</button>
            </div>
        `
    },
    'letter-match': {
        title: 'Letter Match',
        age: 5,
        content: `
            <div class="game-content letter-match">
                <h3>Letter Match</h3>
                <p>Match the uppercase and lowercase letters!</p>
                <div class="match-container">
                    <div class="match-card">Aa</div>
                    <div class="match-card">Bb</div>
                    <div class="match-card">Cc</div>
                    <div class="match-card">Dd</div>
                </div>
                <button class="action-btn game-complete-btn" onclick="completeGame('letter-match')">Finish Matching</button>
            </div>
        `
    },
    'number-fun': {
        title: 'Number Fun',
        age: 5,
        content: `
            <div class="game-content number-fun">
                <h3>Number Fun</h3>
                <p>Count the objects and select the correct number!</p>
                <div class="number-container">
                    <div class="number-question">
                        <div class="number-objects">🍎 🍎 🍎</div>
                        <div class="number-options">
                            <button class="number-option">2</button>
                            <button class="number-option">3</button>
                            <button class="number-option">4</button>
                        </div>
                    </div>
                </div>
                <button class="action-btn game-complete-btn" onclick="completeGame('number-fun')">Finish Counting</button>
            </div>
        `
    }
};

// Initialize game system
document.addEventListener('DOMContentLoaded', function() {
    // Set up age filter buttons
    const ageFilterButtons = document.querySelectorAll('.age-filter-btn');
    if (ageFilterButtons.length > 0) {
        ageFilterButtons.forEach(button => {
            button.addEventListener('click', function() {
                // Remove active class from all buttons
                ageFilterButtons.forEach(btn => btn.classList.remove('active'));
                // Add active class to clicked button
                this.classList.add('active');
                
                // Get selected age filter
                const ageFilter = this.getAttribute('data-age');
                filterGamesByAge(ageFilter);
            });
        });
        
        // Initial filtering (show age 4 games by default)
        filterGamesByAge('4');
    }
    
    // Set up game selection
    const playButtons = document.querySelectorAll('.play-game-btn');
    if (playButtons.length > 0) {
        playButtons.forEach(button => {
            button.addEventListener('click', function() {
                const gameId = this.getAttribute('data-game');
                loadGame(gameId);
            });
        });
    }
});

// Filter games by age
function filterGamesByAge(ageFilter) {
    const gameCards = document.querySelectorAll('.game-card');
    
    gameCards.forEach(card => {
        const gameAge = card.getAttribute('data-age');
        
        if (ageFilter === 'all' || gameAge === ageFilter) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

// Load a game
function loadGame(gameId) {
    const gameContainer = document.getElementById('game-container');
    const gameGrid = document.querySelector('.games-grid');
    
    if (!gameContainer || !gameGrid || !games[gameId]) {
        console.error('Game loading error');
        return;
    }
    
    // Hide game grid and show game container
    gameGrid.style.display = 'none';
    gameContainer.style.display = 'block';
    gameContainer.classList.remove('hide-container');
    
    // Set game content
    gameContainer.innerHTML = games[gameId].content;
    
    // Add back button
    const backButton = document.createElement('button');
    backButton.className = 'back-btn';
    backButton.innerHTML = '<i class="fas fa-arrow-left"></i> Back to Games';
    backButton.addEventListener('click', () => {
        // Hide game container and show grid
        gameContainer.style.display = 'none';
        gameGrid.style.display = 'grid';
        
        // Clear game container
        gameContainer.innerHTML = '';
    });
    
    gameContainer.prepend(backButton);
}

// Complete a game and earn rewards
function completeGame(gameId) {
    // Map game IDs to badge IDs
    const gameMap = {
        'animal-puzzle': 'puzzle_master',
        'coloring': 'coloring_master',
        'letter-match': 'letter_master',
        'number-fun': 'number_master'
    };
    
    // Award badge if available
    const badgeId = gameMap[gameId];
    if (badgeId) {
        awardBadge(badgeId);
    }
    
    // Return to game grid
    const gameContainer = document.getElementById('game-container');
    const gameGrid = document.querySelector('.games-grid');
    
    if (gameContainer && gameGrid) {
        gameContainer.style.display = 'none';
        gameGrid.style.display = 'grid';
        gameContainer.innerHTML = '';
    }
}

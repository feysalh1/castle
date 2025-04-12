#!/bin/bash
# Script to prepare the Children's Castle application for deployment

echo "===== Preparing Children's Castle for Firebase Hosting ====="

# Step 1: Create directory structure
echo "Creating public directory structure..."
rm -rf public
mkdir -p public
mkdir -p public/css
mkdir -p public/js
mkdir -p public/images
mkdir -p public/audio
mkdir -p public/data

# Step 2: Copy static files
echo "Copying static files..."
cp -r static/* public/

# Step 3: Export templates to static HTML
echo "Exporting Flask templates to static HTML..."

# Create a special HTML version of the Firebase login page
cat > public/index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Children's Castle - Login</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="/css/shooting-star.css">
    <script type="module">
        // Import the functions you need from the SDKs
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
        import { getAuth, signInWithEmailAndPassword, createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
        
        // Your web app's Firebase configuration
        const firebaseConfig = {
            apiKey: "FIREBASE_API_KEY",
            authDomain: "story-time-fun.firebaseapp.com",
            projectId: "story-time-fun",
            storageBucket: "story-time-fun.firebasestorage.app",
            messagingSenderId: "225122848236",
            appId: "FIREBASE_APP_ID"
        };
        
        // Initialize Firebase
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        const provider = new GoogleAuthProvider();
        
        // DOM elements
        const googleLoginBtn = document.getElementById('google-login');
        const guestLoginBtn = document.getElementById('guest-login');
        
        // Listen for auth state changes
        auth.onAuthStateChanged(user => {
            if (user) {
                // User is signed in
                window.location.href = '/story-mode.html';
            }
        });
        
        // Google Sign-in
        if (googleLoginBtn) {
            googleLoginBtn.addEventListener('click', () => {
                signInWithPopup(auth, provider)
                    .then((result) => {
                        console.log('Google sign-in successful');
                    })
                    .catch((error) => {
                        console.error('Google sign-in error:', error);
                        alert('Login failed: ' + error.message);
                    });
            });
        }
        
        // Guest login
        if (guestLoginBtn) {
            guestLoginBtn.addEventListener('click', () => {
                signInAnonymously(auth)
                    .then(() => {
                        console.log('Anonymous sign-in successful');
                    })
                    .catch((error) => {
                        console.error('Anonymous sign-in error:', error);
                        alert('Guest login failed: ' + error.message);
                    });
            });
        }
        
        // Initialize shooting stars
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof initShootingStars === 'function') {
                initShootingStars();
            }
        });
    </script>
</head>
<body class="login-page">
    <div class="login-container">
        <div class="login-card">
            <h1>Children's Castle</h1>
            <h2>Interactive Storytime & Games</h2>
            
            <div class="login-options">
                <button id="google-login" class="google-btn">
                    <img src="/images/google-icon.png" alt="Google">
                    Sign in with Google
                </button>
                
                <div class="divider">
                    <span>or</span>
                </div>
                
                <a href="https://childrencastle.replit.app" class="replit-btn">
                    Go to Full Version
                </a>
                
                <p class="login-note">
                    This demo version has limited functionality.<br>
                    Visit the full version for all features!
                </p>
            </div>
        </div>
    </div>
    
    <script src="/js/shooting-star.js"></script>
</body>
</html>
EOF

# Create a story mode page
cat > public/story-mode.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Children's Castle - Story Mode</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="/css/story-mode.css">
    <link rel="stylesheet" href="/css/shooting-star.css">
</head>
<body>
    <header>
        <h1>Children's Castle</h1>
        <div class="nav-buttons">
            <a href="game-mode.html" class="mode-toggle-btn">Game Mode</a>
            <button id="logout-btn" class="logout-btn">Sign Out</button>
        </div>
    </header>
    
    <main class="story-container">
        <div class="story-selection">
            <h2>Choose a Story</h2>
            <div class="story-grid">
                <!-- Stories will be loaded here -->
                <div class="story-card" data-story-id="three_little_pigs">
                    <img src="/images/three_pigs.svg" alt="Three Little Pigs">
                    <h3>Three Little Pigs</h3>
                </div>
                <div class="story-card" data-story-id="goldilocks">
                    <img src="/images/goldilocks.svg" alt="Goldilocks">
                    <h3>Goldilocks</h3>
                </div>
                <div class="story-card" data-story-id="little_fox">
                    <img src="/images/little_fox.svg" alt="Little Fox">
                    <h3>Little Fox</h3>
                </div>
                <!-- More story cards here -->
            </div>
        </div>
        
        <div id="story-reader" class="story-reader hidden">
            <div class="story-controls">
                <button id="back-btn" class="circle-btn">←</button>
                <h2 id="story-title">Story Title</h2>
                <button id="close-story-btn" class="circle-btn">✕</button>
            </div>
            
            <div class="story-content">
                <div id="story-page" class="story-page">
                    <img id="story-image" src="" alt="Story illustration">
                    <p id="story-text">Story text will appear here...</p>
                </div>
                
                <div class="page-controls">
                    <button id="prev-page-btn" class="nav-btn" disabled>Previous</button>
                    <span id="page-counter">Page 1 of 5</span>
                    <button id="next-page-btn" class="nav-btn">Next</button>
                </div>
            </div>
        </div>
    </main>
    
    <script src="/js/shooting-star.js"></script>
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
        import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
        
        // Firebase configuration
        const firebaseConfig = {
            apiKey: "FIREBASE_API_KEY",
            authDomain: "story-time-fun.firebaseapp.com",
            projectId: "story-time-fun",
            storageBucket: "story-time-fun.firebasestorage.app",
            messagingSenderId: "225122848236",
            appId: "FIREBASE_APP_ID"
        };
        
        // Initialize Firebase
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        
        // Check if user is logged in
        auth.onAuthStateChanged(user => {
            if (!user) {
                // Redirect to login if not authenticated
                window.location.href = '/index.html';
            }
        });
        
        // Sign out functionality
        document.getElementById('logout-btn').addEventListener('click', () => {
            signOut(auth).then(() => {
                window.location.href = '/index.html';
            }).catch(error => {
                console.error('Sign out error:', error);
            });
        });
        
        // Initialize UI and story functionality
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof initShootingStars === 'function') {
                initShootingStars();
            }
            
            // Story selection logic
            const storyCards = document.querySelectorAll('.story-card');
            const storyReader = document.getElementById('story-reader');
            const storySelection = document.querySelector('.story-selection');
            const storyTitle = document.getElementById('story-title');
            const storyImage = document.getElementById('story-image');
            const storyText = document.getElementById('story-text');
            const pageCounter = document.getElementById('page-counter');
            const prevPageBtn = document.getElementById('prev-page-btn');
            const nextPageBtn = document.getElementById('next-page-btn');
            const backBtn = document.getElementById('back-btn');
            const closeStoryBtn = document.getElementById('close-story-btn');
            
            let currentStory = null;
            let currentPage = 0;
            
            // Sample story data
            const stories = {
                three_little_pigs: {
                    title: "The Three Little Pigs",
                    pages: [
                        {
                            image: "/images/three_pigs_1.svg",
                            text: "Once upon a time, there were three little pigs who set out to build their own houses."
                        },
                        {
                            image: "/images/three_pigs_2.svg",
                            text: "The first pig built a house of straw because it was the easiest thing to do."
                        },
                        {
                            image: "/images/three_pigs_3.svg",
                            text: "The second pig built a house of sticks. It was a bit stronger than the straw house."
                        },
                        {
                            image: "/images/three_pigs_4.svg",
                            text: "The third pig worked hard to build a house of bricks. It took a long time, but it was very strong."
                        },
                        {
                            image: "/images/three_pigs_5.svg",
                            text: "Then along came a wolf who huffed and puffed and blew down the straw house!"
                        }
                    ]
                },
                goldilocks: {
                    title: "Goldilocks and the Three Bears",
                    pages: [
                        {
                            image: "/images/goldilocks_1.svg",
                            text: "Once upon a time, there was a little girl named Goldilocks. She went for a walk in the forest."
                        },
                        {
                            image: "/images/goldilocks_2.svg",
                            text: "She came upon a house and knocked. When no one answered, she walked right in."
                        },
                        {
                            image: "/images/goldilocks_3.svg",
                            text: "Goldilocks saw three bowls of porridge. She tasted the first one, but it was too hot!"
                        }
                    ]
                }
            };
            
            // Open a story when its card is clicked
            storyCards.forEach(card => {
                card.addEventListener('click', () => {
                    const storyId = card.dataset.storyId;
                    if (stories[storyId]) {
                        openStory(storyId);
                    }
                });
            });
            
            // Function to open a story
            function openStory(storyId) {
                currentStory = stories[storyId];
                currentPage = 0;
                
                // Update UI
                storyTitle.textContent = currentStory.title;
                updatePageContent();
                
                // Show reader, hide selection
                storySelection.classList.add('hidden');
                storyReader.classList.remove('hidden');
                
                // Create shooting star effect
                if (typeof createShootingStar === 'function') {
                    createShootingStar();
                }
            }
            
            // Update page content based on current page
            function updatePageContent() {
                const page = currentStory.pages[currentPage];
                storyImage.src = page.image;
                storyText.textContent = page.text;
                pageCounter.textContent = `Page ${currentPage + 1} of ${currentStory.pages.length}`;
                
                // Update navigation buttons
                prevPageBtn.disabled = currentPage === 0;
                nextPageBtn.disabled = currentPage === currentStory.pages.length - 1;
            }
            
            // Navigation button event listeners
            prevPageBtn.addEventListener('click', () => {
                if (currentPage > 0) {
                    currentPage--;
                    updatePageContent();
                }
            });
            
            nextPageBtn.addEventListener('click', () => {
                if (currentPage < currentStory.pages.length - 1) {
                    currentPage++;
                    updatePageContent();
                }
            });
            
            // Close story and return to selection
            function closeStory() {
                storyReader.classList.add('hidden');
                storySelection.classList.remove('hidden');
                currentStory = null;
            }
            
            backBtn.addEventListener('click', closeStory);
            closeStoryBtn.addEventListener('click', closeStory);
        });
    </script>
</body>
</html>
EOF

# Create a game mode page
cat > public/game-mode.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Children's Castle - Game Mode</title>
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="/css/style.css">
    <link rel="stylesheet" href="/css/game-mode.css">
    <link rel="stylesheet" href="/css/shooting-star.css">
</head>
<body>
    <header>
        <h1>Children's Castle</h1>
        <div class="nav-buttons">
            <a href="story-mode.html" class="mode-toggle-btn">Story Mode</a>
            <button id="logout-btn" class="logout-btn">Sign Out</button>
        </div>
    </header>
    
    <main class="game-container">
        <div class="game-selection">
            <h2>Choose a Game</h2>
            <div class="game-grid">
                <!-- Games will be loaded here -->
                <div class="game-card" data-game="word_builder">
                    <img src="/images/word_builder.svg" alt="Word Builder">
                    <h3>Word Builder</h3>
                    <p>Learn spelling with fun!</p>
                </div>
                <div class="game-card" data-game="fun_addition">
                    <img src="/images/fun_addition.svg" alt="Fun Addition">
                    <h3>Fun Addition</h3>
                    <p>Learn to add numbers!</p>
                </div>
                <!-- More game cards here -->
            </div>
        </div>
        
        <div id="game-player" class="game-player hidden">
            <div class="game-controls">
                <button id="back-to-games-btn" class="circle-btn">←</button>
                <h2 id="game-title">Game Title</h2>
                <button id="close-game-btn" class="circle-btn">✕</button>
            </div>
            
            <div id="game-content" class="game-content">
                <!-- Game content will be loaded here -->
                <div id="word-builder-game" class="game-module hidden">
                    <div class="game-instructions">
                        <p>Drag the letters to spell the word shown in the picture!</p>
                    </div>
                    <div class="word-builder-container">
                        <div class="word-image-container">
                            <img id="word-image" src="" alt="Word to spell">
                        </div>
                        <div id="word-target" class="word-target"></div>
                        <div id="letter-bank" class="letter-bank"></div>
                    </div>
                    <div class="game-controls">
                        <button id="check-word-btn" class="game-btn">Check</button>
                        <button id="next-word-btn" class="game-btn" disabled>Next Word</button>
                    </div>
                </div>
                
                <div id="addition-game" class="game-module hidden">
                    <div class="game-instructions">
                        <p>Solve the addition problems!</p>
                    </div>
                    <div class="addition-container">
                        <div id="addition-problem" class="addition-problem">
                            <span id="num1">5</span> + <span id="num2">3</span> = <input type="number" id="addition-answer" min="0" max="20">
                        </div>
                    </div>
                    <div class="game-controls">
                        <button id="check-addition-btn" class="game-btn">Check</button>
                        <button id="next-addition-btn" class="game-btn" disabled>Next Problem</button>
                    </div>
                </div>
            </div>
        </div>
    </main>
    
    <script src="/js/shooting-star.js"></script>
    <script type="module">
        import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
        import { getAuth, signOut } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
        
        // Firebase configuration
        const firebaseConfig = {
            apiKey: "FIREBASE_API_KEY",
            authDomain: "story-time-fun.firebaseapp.com",
            projectId: "story-time-fun",
            storageBucket: "story-time-fun.firebasestorage.app",
            messagingSenderId: "225122848236",
            appId: "FIREBASE_APP_ID"
        };
        
        // Initialize Firebase
        const app = initializeApp(firebaseConfig);
        const auth = getAuth(app);
        
        // Check if user is logged in
        auth.onAuthStateChanged(user => {
            if (!user) {
                // Redirect to login if not authenticated
                window.location.href = '/index.html';
            }
        });
        
        // Sign out functionality
        document.getElementById('logout-btn').addEventListener('click', () => {
            signOut(auth).then(() => {
                window.location.href = '/index.html';
            }).catch(error => {
                console.error('Sign out error:', error);
            });
        });
        
        // Initialize UI and game functionality
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof initShootingStars === 'function') {
                initShootingStars();
            }
            
            // Game selection logic
            const gameCards = document.querySelectorAll('.game-card');
            const gamePlayer = document.getElementById('game-player');
            const gameSelection = document.querySelector('.game-selection');
            const gameTitle = document.getElementById('game-title');
            const gameContent = document.getElementById('game-content');
            const backToGamesBtn = document.getElementById('back-to-games-btn');
            const closeGameBtn = document.getElementById('close-game-btn');
            
            // Word Builder game elements
            const wordBuilderGame = document.getElementById('word-builder-game');
            const wordImage = document.getElementById('word-image');
            const wordTarget = document.getElementById('word-target');
            const letterBank = document.getElementById('letter-bank');
            const checkWordBtn = document.getElementById('check-word-btn');
            const nextWordBtn = document.getElementById('next-word-btn');
            
            // Addition game elements
            const additionGame = document.getElementById('addition-game');
            const num1Element = document.getElementById('num1');
            const num2Element = document.getElementById('num2');
            const additionAnswer = document.getElementById('addition-answer');
            const checkAdditionBtn = document.getElementById('check-addition-btn');
            const nextAdditionBtn = document.getElementById('next-addition-btn');
            
            // Sample word list for Word Builder game
            const wordList = [
                { word: "CAT", image: "/images/word_cat.svg" },
                { word: "DOG", image: "/images/word_dog.svg" },
                { word: "SUN", image: "/images/word_sun.svg" },
                { word: "TREE", image: "/images/word_tree.svg" }
            ];
            
            let currentWordIndex = 0;
            let currentWord = null;
            let placedLetters = [];
            
            // Open a game when its card is clicked
            gameCards.forEach(card => {
                card.addEventListener('click', () => {
                    const gameType = card.dataset.game;
                    openGame(gameType);
                });
            });
            
            // Function to open a game
            function openGame(gameType) {
                // Hide all game modules first
                document.querySelectorAll('.game-module').forEach(module => {
                    module.classList.add('hidden');
                });
                
                // Show the appropriate game module
                if (gameType === 'word_builder') {
                    gameTitle.textContent = "Word Builder";
                    wordBuilderGame.classList.remove('hidden');
                    setupWordBuilderGame();
                } else if (gameType === 'fun_addition') {
                    gameTitle.textContent = "Fun Addition";
                    additionGame.classList.remove('hidden');
                    setupAdditionGame();
                }
                
                // Show game player, hide selection
                gameSelection.classList.add('hidden');
                gamePlayer.classList.remove('hidden');
                
                // Create shooting star effect
                if (typeof createShootingStar === 'function') {
                    createShootingStar();
                }
            }
            
            // Set up Word Builder game
            function setupWordBuilderGame() {
                currentWordIndex = 0;
                loadWord();
            }
            
            // Load a word in the Word Builder game
            function loadWord() {
                currentWord = wordList[currentWordIndex];
                
                // Reset UI elements
                wordImage.src = currentWord.image;
                wordTarget.innerHTML = '';
                letterBank.innerHTML = '';
                nextWordBtn.disabled = true;
                
                // Create target slots for each letter
                placedLetters = [];
                for (let i = 0; i < currentWord.word.length; i++) {
                    const slot = document.createElement('div');
                    slot.className = 'letter-slot';
                    slot.dataset.index = i;
                    wordTarget.appendChild(slot);
                }
                
                // Create letter tiles in shuffled order
                const letters = currentWord.word.split('');
                shuffleArray(letters);
                
                letters.forEach((letter, index) => {
                    const tile = document.createElement('div');
                    tile.className = 'letter-tile';
                    tile.textContent = letter;
                    tile.dataset.letter = letter;
                    tile.dataset.index = index;
                    
                    // Add drag functionality
                    tile.draggable = true;
                    tile.addEventListener('dragstart', handleDragStart);
                    
                    letterBank.appendChild(tile);
                });
                
                // Add event listeners for dropping
                const slots = document.querySelectorAll('.letter-slot');
                slots.forEach(slot => {
                    slot.addEventListener('dragover', handleDragOver);
                    slot.addEventListener('drop', handleDrop);
                });
            }
            
            // Drag and drop functions for Word Builder
            function handleDragStart(e) {
                e.dataTransfer.setData('text/plain', e.target.dataset.index);
                e.dataTransfer.effectAllowed = 'move';
            }
            
            function handleDragOver(e) {
                e.preventDefault();
                e.dataTransfer.dropEffect = 'move';
            }
            
            function handleDrop(e) {
                e.preventDefault();
                const tileIndex = e.dataTransfer.getData('text/plain');
                const tile = document.querySelector(`.letter-tile[data-index="${tileIndex}"]`);
                const slotIndex = e.target.dataset.index;
                
                // Place the letter in the slot
                e.target.appendChild(tile);
                tile.classList.add('placed');
                
                // Track placed letters
                placedLetters[slotIndex] = tile.dataset.letter;
            }
            
            // Check if the word is spelled correctly
            checkWordBtn.addEventListener('click', () => {
                // Collect the letters in the target slots
                const spelledWord = placedLetters.join('');
                
                if (spelledWord === currentWord.word) {
                    // Correct answer
                    wordTarget.classList.add('correct');
                    nextWordBtn.disabled = false;
                    
                    // Create celebratory shooting stars
                    if (typeof createShootingStar === 'function') {
                        for (let i = 0; i < 3; i++) {
                            setTimeout(() => {
                                createShootingStar();
                            }, i * 300);
                        }
                    }
                } else {
                    // Incorrect answer
                    wordTarget.classList.add('incorrect');
                    setTimeout(() => {
                        wordTarget.classList.remove('incorrect');
                    }, 1000);
                }
            });
            
            // Move to the next word
            nextWordBtn.addEventListener('click', () => {
                wordTarget.classList.remove('correct');
                currentWordIndex = (currentWordIndex + 1) % wordList.length;
                loadWord();
            });
            
            // Set up Addition game
            function setupAdditionGame() {
                generateAdditionProblem();
            }
            
            // Generate a new addition problem
            function generateAdditionProblem() {
                const num1 = Math.floor(Math.random() * 10) + 1;
                const num2 = Math.floor(Math.random() * 10) + 1;
                
                num1Element.textContent = num1;
                num2Element.textContent = num2;
                additionAnswer.value = '';
                nextAdditionBtn.disabled = true;
                
                // Remove previous styling
                additionAnswer.classList.remove('correct', 'incorrect');
            }
            
            // Check addition answer
            checkAdditionBtn.addEventListener('click', () => {
                const num1 = parseInt(num1Element.textContent);
                const num2 = parseInt(num2Element.textContent);
                const userAnswer = parseInt(additionAnswer.value);
                const correctAnswer = num1 + num2;
                
                if (userAnswer === correctAnswer) {
                    // Correct answer
                    additionAnswer.classList.add('correct');
                    nextAdditionBtn.disabled = false;
                    
                    // Create celebratory shooting stars
                    if (typeof createShootingStar === 'function') {
                        for (let i = 0; i < 3; i++) {
                            setTimeout(() => {
                                createShootingStar();
                            }, i * 300);
                        }
                    }
                } else {
                    // Incorrect answer
                    additionAnswer.classList.add('incorrect');
                    setTimeout(() => {
                        additionAnswer.classList.remove('incorrect');
                    }, 1000);
                }
            });
            
            // Move to the next addition problem
            nextAdditionBtn.addEventListener('click', () => {
                generateAdditionProblem();
            });
            
            // Helper function to shuffle an array
            function shuffleArray(array) {
                for (let i = array.length - 1; i > 0; i--) {
                    const j = Math.floor(Math.random() * (i + 1));
                    [array[i], array[j]] = [array[j], array[i]];
                }
                return array;
            }
            
            // Close game and return to selection
            function closeGame() {
                gamePlayer.classList.add('hidden');
                gameSelection.classList.remove('hidden');
            }
            
            backToGamesBtn.addEventListener('click', closeGame);
            closeGameBtn.addEventListener('click', closeGame);
        });
    </script>
</body>
</html>
EOF

# Step 4: Create required images for the deployment
echo "Creating required images for the story cards..."
mkdir -p public/images

# Make sure all the required SVG files exist, create placeholder ones if needed
mkdir -p public/images
for img in three_pigs goldilocks little_fox word_builder fun_addition three_pigs_1 three_pigs_2 three_pigs_3 three_pigs_4 three_pigs_5 goldilocks_1 goldilocks_2 goldilocks_3; do
  if [ ! -f "public/images/${img}.svg" ]; then
    # Create a simple placeholder SVG
    cat > "public/images/${img}.svg" << SVGEOF
<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200" viewBox="0 0 300 200">
  <rect width="300" height="200" fill="#f0f0f0" />
  <text x="150" y="100" font-family="Arial" font-size="16" text-anchor="middle">${img}</text>
</svg>
SVGEOF
    echo "Created placeholder for ${img}.svg"
  fi
done

# Create a Google icon if needed
if [ ! -f "public/images/google-icon.png" ]; then
  # Create a simple placeholder for the Google icon or copy from static if available
  if [ -f "static/images/google-icon.png" ]; then
    cp "static/images/google-icon.png" "public/images/google-icon.png"
  else
    echo "⚠️ Warning: Missing Google icon, authentication may look broken"
  fi
fi

# Step 5: Inject Firebase config variables from environment
echo "Injecting Firebase configuration from environment variables..."

# Direct replacement of Firebase config in HTML files
echo "Injecting Firebase configuration variables into HTML files..."
find public -type f -name "*.html" -o -name "*.js" | xargs sed -i "s/FIREBASE_API_KEY/${FIREBASE_API_KEY}/g" 2>/dev/null || true
find public -type f -name "*.html" -o -name "*.js" | xargs sed -i "s/FIREBASE_APP_ID/${FIREBASE_APP_ID}/g" 2>/dev/null || true

if [ $? -ne 0 ]; then
  echo "⚠️ Warning: Could not replace Firebase config variables. Check if sed failed or the variables are not set."
  echo "⚠️ This is expected on Windows/Mac as GNU sed may not be available. Firebase functionality may not work correctly."
else
  echo "✅ Firebase configuration injected successfully!"
fi

echo "===== Preparation complete! ====="
echo "The static assets are now prepared for Firebase Hosting."
echo "Run 'firebase deploy --only hosting' to publish the site."
echo "Your site will be available at https://story-time-fun.web.app"
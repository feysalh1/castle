// Rewards System

// Define story badges with their respective icons and descriptions
const storyBadges = {
    'little_fox': { icon: '🦊', title: 'Little Fox Explorer', description: 'Completed The Little Fox story' },
    'three_little_pigs': { icon: '🐷', title: 'Three Pigs Builder', description: 'Completed Three Little Pigs story' },
    'brown_bear': { icon: '🐻', title: 'Brown Bear Friend', description: 'Completed Brown Bear story' },
    'wild_things': { icon: '👹', title: 'Wild Thing', description: 'Completed Where the Wild Things Are story' },
    'black_sheep': { icon: '🐑', title: 'Baa Baa Champion', description: 'Completed Baa Baa Black Sheep story' },
    'hickory_dickory': { icon: '🐭', title: 'Clock Climber', description: 'Completed Hickory Dickory Dock story' },
    'bo_peep': { icon: '🐑', title: 'Sheep Finder', description: 'Completed Little Bo-Peep story' },
    'jack_jill': { icon: '⛰️', title: 'Hill Climber', description: 'Completed Jack and Jill story' }
};

// Game badges
const gameBadges = {
    'puzzle_master': { icon: '🧩', title: 'Puzzle Master', description: 'Completed the animal puzzle game' },
    'fast_solver': { icon: '⏱️', title: 'Speed Champion', description: 'Solved a puzzle in under 1 minute' }
};

// Initialize rewards
let earnedBadges = {};
let starCount = 0;

// Load rewards from localStorage
function loadRewards() {
    const savedBadges = localStorage.getItem('babyGirlEarnedBadges');
    const savedStars = localStorage.getItem('babyGirlStarCount');
    
    if (savedBadges) {
        earnedBadges = JSON.parse(savedBadges);
    }
    
    if (savedStars) {
        starCount = parseInt(savedStars);
    }
    
    updateStarDisplay();
    renderBadges();
}

// Save rewards to localStorage
function saveRewards() {
    localStorage.setItem('babyGirlEarnedBadges', JSON.stringify(earnedBadges));
    localStorage.setItem('babyGirlStarCount', starCount.toString());
}

// Award a badge
function awardBadge(badgeId) {
    // Check if badge is already earned
    if (earnedBadges[badgeId]) {
        return false;
    }
    
    // Determine badge type
    let badgeInfo;
    if (storyBadges[badgeId]) {
        badgeInfo = storyBadges[badgeId];
    } else if (gameBadges[badgeId]) {
        badgeInfo = gameBadges[badgeId];
    } else {
        console.error('Unknown badge ID:', badgeId);
        return false;
    }
    
    // Award the badge
    earnedBadges[badgeId] = true;
    
    // Award stars
    awardStars(5);
    
    // Show achievement popup
    showAchievementPopup(badgeInfo.icon, badgeInfo.title, 'You earned a new badge and 5 stars!');
    
    // Save rewards
    saveRewards();
    
    // Render badges
    renderBadges();
    
    return true;
}

// Award stars
function awardStars(amount) {
    starCount += amount;
    updateStarDisplay();
    
    // Animate stars
    for (let i = 0; i < amount; i++) {
        setTimeout(() => {
            createStarAnimation();
        }, i * 300); // Stagger star animations
    }
}

// Update star display
function updateStarDisplay() {
    const starCountElement = document.getElementById('star-count');
    if (starCountElement) {
        starCountElement.textContent = starCount;
    }
}

// Create star animation
function createStarAnimation() {
    const star = document.createElement('div');
    star.className = 'star-reward';
    star.innerHTML = '<i class="fas fa-star"></i>';
    
    // Random position on screen
    const x = Math.random() * window.innerWidth * 0.8;
    const y = Math.random() * window.innerHeight * 0.5 + 100;
    
    star.style.left = x + 'px';
    star.style.top = y + 'px';
    
    document.body.appendChild(star);
    
    // Remove star after animation completes
    setTimeout(() => {
        document.body.removeChild(star);
    }, 1500);
}

// Render badges in the badges section
function renderBadges() {
    const badgesContainer = document.getElementById('story-badges');
    if (!badgesContainer) return;
    
    // Clear container
    badgesContainer.innerHTML = '';
    
    // Add story badges
    Object.keys(storyBadges).forEach(badgeId => {
        const badge = storyBadges[badgeId];
        const isEarned = earnedBadges[badgeId] || false;
        
        const badgeElement = document.createElement('div');
        badgeElement.className = `badge ${isEarned ? 'earned' : ''}`;
        badgeElement.innerHTML = `
            ${badge.icon}
            <span class="badge-tooltip">${badge.title}</span>
        `;
        
        badgesContainer.appendChild(badgeElement);
    });
    
    // Update reward message
    updateRewardMessage();
}

// Update reward message based on progress
function updateRewardMessage() {
    const rewardMessage = document.getElementById('reward-message');
    if (!rewardMessage) return;
    
    const earnedCount = Object.keys(earnedBadges).length;
    const totalBadges = Object.keys(storyBadges).length + Object.keys(gameBadges).length;
    
    if (earnedCount === 0) {
        rewardMessage.textContent = 'Complete stories to earn badges and stars!';
    } else if (earnedCount < totalBadges / 2) {
        rewardMessage.textContent = `Great job! You've earned ${earnedCount} badges and ${starCount} stars!`;
    } else if (earnedCount < totalBadges) {
        rewardMessage.textContent = `Amazing! You've collected ${earnedCount} badges and ${starCount} stars!`;
    } else {
        rewardMessage.textContent = `WOW! You've collected ALL badges and ${starCount} stars! You're a SUPERSTAR!`;
    }
}

// Show achievement popup
function showAchievementPopup(icon, title, message) {
    // Create popup element
    const popup = document.createElement('div');
    popup.className = 'achievement-popup';
    popup.innerHTML = `
        <div class="achievement-icon">${icon}</div>
        <div class="achievement-title">${title}</div>
        <div class="achievement-message">${message}</div>
        <button class="close-btn">Yay!</button>
    `;
    
    // Add to document
    document.body.appendChild(popup);
    
    // Close button event
    const closeBtn = popup.querySelector('.close-btn');
    closeBtn.addEventListener('click', () => {
        document.body.removeChild(popup);
    });
    
    // Auto close after 5 seconds
    setTimeout(() => {
        if (document.body.contains(popup)) {
            document.body.removeChild(popup);
        }
    }, 5000);
}

// Award story completion badge
function awardStoryCompletionBadge(storyId) {
    // Map story titles to badge IDs
    const storyMap = {
        'little_fox': 'little_fox',
        'three_little_pigs': 'three_little_pigs',
        'brown_bear': 'brown_bear',
        'wild_things': 'wild_things',
        'black_sheep': 'black_sheep',
        'hickory_dickory': 'hickory_dickory',
        'bo_peep': 'bo_peep',
        'jack_jill': 'jack_jill'
    };
    
    const badgeId = storyMap[storyId];
    if (badgeId) {
        return awardBadge(badgeId);
    }
    
    return false;
}

// Initialize rewards system
document.addEventListener('DOMContentLoaded', () => {
    // Load saved rewards
    loadRewards();
    
    // Set up rewards button in mode selection
    const rewardsBtn = document.getElementById('rewards-btn');
    if (rewardsBtn) {
        rewardsBtn.addEventListener('click', () => {
            showSection('badges-section');
        });
    }
    
    // Back button from badges to mode selection
    const backToModesBtn = document.getElementById('back-to-modes-from-badges-btn');
    if (backToModesBtn) {
        backToModesBtn.addEventListener('click', () => {
            showSection('mode-selection');
        });
    }
    
    // Set up story completion tracking
    const doneReadingBtn = document.getElementById('done-reading-btn');
    if (doneReadingBtn) {
        doneReadingBtn.addEventListener('click', () => {
            const storySelect = document.getElementById('story-select');
            if (storySelect) {
                const storyId = storySelect.value;
                awardStoryCompletionBadge(storyId);
            }
        });
    }
});

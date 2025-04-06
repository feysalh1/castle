// Rewards System

// Define story badges with their respective icons and descriptions
const storyBadges = {
    'little_fox': { icon: '🦊', title: 'Little Fox Explorer', description: 'Completed The Little Fox story', stars: 5 },
    'three_little_pigs': { icon: '🐷', title: 'Three Pigs Builder', description: 'Completed Three Little Pigs story', stars: 5 },
    'brown_bear': { icon: '🐻', title: 'Brown Bear Friend', description: 'Completed Brown Bear story', stars: 5 },
    'wild_things': { icon: '👹', title: 'Wild Thing', description: 'Completed Where the Wild Things Are story', stars: 5 },
    'black_sheep': { icon: '🐑', title: 'Baa Baa Champion', description: 'Completed Baa Baa Black Sheep story', stars: 5 },
    'hickory_dickory': { icon: '🐭', title: 'Clock Climber', description: 'Completed Hickory Dickory Dock story', stars: 5 },
    'bo_peep': { icon: '🐑', title: 'Sheep Finder', description: 'Completed Little Bo-Peep story', stars: 5 },
    'jack_jill': { icon: '⛰️', title: 'Hill Climber', description: 'Completed Jack and Jill story', stars: 5 }
};

// Game badges
const gameBadges = {
    // Age 4 badges
    'puzzle_master': { icon: '🧩', title: 'Puzzle Master', description: 'Completed the animal puzzle game', age: 4, stars: 7 },
    'coloring_master': { icon: '🎨', title: 'Coloring Artist', description: 'Completed the coloring game', age: 4, stars: 7 },
    'shape_master': { icon: '📐', title: 'Shape Master', description: 'Completed the shape matching game', age: 4, stars: 7 },
    
    // Age 5+ badges
    'letter_master': { icon: '🔤', title: 'Letter Champion', description: 'Completed the letter matching game', age: 5, stars: 10 },
    'number_master': { icon: '🔢', title: 'Number Whiz', description: 'Completed the number game', age: 5, stars: 10 },
    'memory_master': { icon: '🧠', title: 'Memory Master', description: 'Completed the memory game', age: 5, stars: 10 },
    
    // Special badges
    'fast_solver': { icon: '⏱️', title: 'Speed Champion', description: 'Solved a puzzle in under 1 minute', age: 'special', stars: 15 },
    'star_collector': { icon: '🌟', title: 'Star Collector', description: 'Collected 50 stars total', age: 'special', stars: 0 },
    'story_lover': { icon: '📚', title: 'Story Enthusiast', description: 'Completed all stories', age: 'special', stars: 20 },
    'game_master': { icon: '🏆', title: 'Game Master', description: 'Completed all games', age: 'special', stars: 20 }
};

// Reward tiers
const rewardTiers = [
    { stars: 10, title: "Bronze Reader", icon: "🥉", message: "You've earned the Bronze Reader award!" },
    { stars: 25, title: "Silver Reader", icon: "🥈", message: "You've reached Silver Reader status!" },
    { stars: 50, title: "Gold Reader", icon: "🥇", message: "Congratulations on becoming a Gold Reader!" },
    { stars: 75, title: "Platinum Reader", icon: "💎", message: "Amazing! You're now a Platinum Reader!" },
    { stars: 100, title: "Diamond Reader", icon: "👑", message: "Incredible! You've achieved Diamond Reader status!" }
];

// Initialize rewards
let earnedBadges = {};
let starCount = 0;
let unlockedTiers = {};
let lastCompletedBadgeTime = null;
let badgeStreak = 0;

// Load rewards from localStorage
function loadRewards() {
    // Update localStorage key to match new app name
    const savedBadges = localStorage.getItem('childrensEarnedBadges') || localStorage.getItem('babyGirlEarnedBadges');
    const savedStars = localStorage.getItem('childrensStarCount') || localStorage.getItem('babyGirlStarCount');
    const savedTiers = localStorage.getItem('childrensUnlockedTiers');
    const savedStreak = localStorage.getItem('childrensBadgeStreak');
    
    if (savedBadges) {
        earnedBadges = JSON.parse(savedBadges);
    }
    
    if (savedStars) {
        starCount = parseInt(savedStars);
    }
    
    if (savedTiers) {
        unlockedTiers = JSON.parse(savedTiers);
    }
    
    if (savedStreak) {
        const streakData = JSON.parse(savedStreak);
        badgeStreak = streakData.streak || 0;
        lastCompletedBadgeTime = streakData.lastTime ? new Date(streakData.lastTime) : null;
    }
    
    updateStarDisplay();
    renderBadges();
    checkTierAchievements();
}

// Save rewards to localStorage
function saveRewards() {
    // Update localStorage key to match new app name
    localStorage.setItem('childrensEarnedBadges', JSON.stringify(earnedBadges));
    localStorage.setItem('childrensStarCount', starCount.toString());
    localStorage.setItem('childrensUnlockedTiers', JSON.stringify(unlockedTiers));
    
    // Save streak data
    const streakData = {
        streak: badgeStreak,
        lastTime: lastCompletedBadgeTime ? lastCompletedBadgeTime.toISOString() : null
    };
    localStorage.setItem('childrensBadgeStreak', JSON.stringify(streakData));
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
    const starsToAward = badgeInfo.stars || 5; // Default to 5 stars if not specified
    
    // Check for streaks
    updateBadgeStreak();
    let streakBonus = 0;
    
    // Apply streak bonus (1 extra star for every badge in streak beyond the first)
    if (badgeStreak > 1) {
        streakBonus = badgeStreak - 1;
        showAchievementPopup('🔥', 'Streak Bonus!', `${badgeStreak} in a row! +${streakBonus} bonus stars!`);
    }
    
    // Award stars including any streak bonus
    awardStars(starsToAward + streakBonus);
    
    // Show achievement popup
    showAchievementPopup(
        badgeInfo.icon, 
        badgeInfo.title, 
        `${badgeInfo.description}! +${starsToAward} stars${streakBonus ? ` (+ ${streakBonus} streak bonus)` : ''}!`
    );
    
    // Check for special achievements
    checkSpecialAchievements();
    
    // Save rewards
    saveRewards();
    
    // Render badges
    renderBadges();
    
    return true;
}

// Update badge streak
function updateBadgeStreak() {
    const now = new Date();
    const oneDayMs = 24 * 60 * 60 * 1000;
    
    // If this is the first badge or if it's been more than a day, reset streak
    if (!lastCompletedBadgeTime || (now - new Date(lastCompletedBadgeTime)) > oneDayMs) {
        badgeStreak = 1;
    } else {
        // Otherwise increment streak
        badgeStreak++;
    }
    
    // Update last completion time
    lastCompletedBadgeTime = now;
}

// Check for special achievements
function checkSpecialAchievements() {
    // Check for story lover achievement (all stories completed)
    const storyBadgeIds = Object.keys(storyBadges);
    const allStoriesCompleted = storyBadgeIds.every(id => earnedBadges[id]);
    
    if (allStoriesCompleted && !earnedBadges['story_lover']) {
        awardBadge('story_lover');
    }
    
    // Check for game master achievement (all regular games completed)
    const regularGameBadgeIds = Object.keys(gameBadges).filter(id => 
        gameBadges[id].age === 4 || gameBadges[id].age === 5
    );
    const allGamesCompleted = regularGameBadgeIds.every(id => earnedBadges[id]);
    
    if (allGamesCompleted && !earnedBadges['game_master']) {
        awardBadge('game_master');
    }
    
    // Check for star collector achievement
    if (starCount >= 50 && !earnedBadges['star_collector']) {
        awardBadge('star_collector');
    }
}

// Check for tier achievements
function checkTierAchievements() {
    for (const tier of rewardTiers) {
        if (starCount >= tier.stars && !unlockedTiers[tier.title]) {
            unlockedTiers[tier.title] = true;
            showAchievementPopup(tier.icon, tier.title, tier.message);
            saveRewards();
        }
    }
}

// Award stars
function awardStars(amount) {
    starCount += amount;
    updateStarDisplay();
    
    // Check for tier achievements
    checkTierAchievements();
    
    // Animate stars
    for (let i = 0; i < amount; i++) {
        setTimeout(() => {
            createStarAnimation();
        }, i * 300); // Stagger star animations
    }
    
    saveRewards();
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
    star.className = 'flying-star';
    star.innerHTML = '⭐';
    
    // Position near the star counter
    const starCounter = document.querySelector('.total-stars');
    if (starCounter) {
        const rect = starCounter.getBoundingClientRect();
        
        // Random starting position near the badge or game that was completed
        const x = rect.left + (rect.width / 2) + (Math.random() * 200 - 100);
        const y = rect.top + rect.height + 100 + (Math.random() * 50);
        
        star.style.left = x + 'px';
        star.style.top = y + 'px';
        
        document.body.appendChild(star);
        
        // Remove star after animation completes
        setTimeout(() => {
            if (document.body.contains(star)) {
                document.body.removeChild(star);
            }
        }, 1500);
    }
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
            <div class="badge-name">${badge.title}</div>
        `;
        
        // Add tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'badge-tooltip';
        tooltip.innerHTML = `
            <div><strong>${badge.title}</strong></div>
            <div>${badge.description}</div>
            <div class="tooltip-stars">+${badge.stars || 5} ⭐</div>
        `;
        badgeElement.appendChild(tooltip);
        
        badgesContainer.appendChild(badgeElement);
    });
    
    // Add age-appropriate game badges section
    const badgesSection = document.getElementById('badges-section');
    if (badgesSection) {
        // Remove any existing game badge sections
        const existingGameBadges = badgesSection.querySelectorAll('.age-badges-section');
        existingGameBadges.forEach(el => el.remove());
        
        // Age 4 badges
        addGameBadgeSection(badgesSection, 'Age 4 Game Badges', 4);
        
        // Age 5+ badges
        addGameBadgeSection(badgesSection, 'Age 5+ Game Badges', 5);
        
        // Special badges
        addGameBadgeSection(badgesSection, 'Special Achievements', 'special');
        
        // Add reward tiers section
        addRewardTiersSection(badgesSection);
    }
    
    // Update reward message
    updateRewardMessage();
}

// Add game badge section for specific age
function addGameBadgeSection(container, title, age) {
    const filteredBadges = Object.keys(gameBadges).filter(key => gameBadges[key].age === age);
    
    // Skip if no badges for this age
    if (filteredBadges.length === 0) return;
    
    const sectionDiv = document.createElement('div');
    sectionDiv.className = 'age-badges-section';
    sectionDiv.innerHTML = `<h3 class="badges-title">${title}</h3>`;
    
    const badgesContainer = document.createElement('div');
    badgesContainer.className = 'badges-container';
    
    filteredBadges.forEach(badgeId => {
        const badge = gameBadges[badgeId];
        const isEarned = earnedBadges[badgeId] || false;
        
        const badgeElement = document.createElement('div');
        badgeElement.className = `badge ${isEarned ? 'earned' : ''}`;
        badgeElement.innerHTML = `
            ${badge.icon}
            <div class="badge-name">${badge.title}</div>
        `;
        
        // Add tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'badge-tooltip';
        tooltip.innerHTML = `
            <div><strong>${badge.title}</strong></div>
            <div>${badge.description}</div>
            <div class="tooltip-stars">+${badge.stars || 5} ⭐</div>
        `;
        badgeElement.appendChild(tooltip);
        
        badgesContainer.appendChild(badgeElement);
    });
    
    sectionDiv.appendChild(badgesContainer);
    container.appendChild(sectionDiv);
}

// Add reward tiers section
function addRewardTiersSection(container) {
    const sectionDiv = document.createElement('div');
    sectionDiv.className = 'reward-tiers-section';
    sectionDiv.innerHTML = `<h3 class="badges-title">Reader Achievement Levels</h3>`;
    
    const tiersContainer = document.createElement('div');
    tiersContainer.className = 'tiers-container';
    
    rewardTiers.forEach(tier => {
        const isUnlocked = unlockedTiers[tier.title] || false;
        
        const tierElement = document.createElement('div');
        tierElement.className = `reward-tier ${isUnlocked ? 'unlocked' : 'locked'}`;
        
        const starRequirement = document.createElement('div');
        starRequirement.className = 'tier-requirement';
        starRequirement.textContent = `${tier.stars} ⭐`;
        
        const tierContent = document.createElement('div');
        tierContent.className = 'tier-content';
        tierContent.innerHTML = `
            <div class="tier-icon">${tier.icon}</div>
            <div class="tier-title">${tier.title}</div>
        `;
        
        tierElement.appendChild(starRequirement);
        tierElement.appendChild(tierContent);
        tiersContainer.appendChild(tierElement);
    });
    
    sectionDiv.appendChild(tiersContainer);
    container.appendChild(sectionDiv);
    
    // Add progress bar
    const progressSection = document.createElement('div');
    progressSection.className = 'reward-progress-section';
    
    // Find next tier
    let nextTierIndex = 0;
    while (nextTierIndex < rewardTiers.length && starCount >= rewardTiers[nextTierIndex].stars) {
        nextTierIndex++;
    }
    
    if (nextTierIndex < rewardTiers.length) {
        const nextTier = rewardTiers[nextTierIndex];
        const prevStars = nextTierIndex > 0 ? rewardTiers[nextTierIndex - 1].stars : 0;
        const progress = Math.min(100, Math.round((starCount - prevStars) / (nextTier.stars - prevStars) * 100));
        
        progressSection.innerHTML = `
            <div class="progress-label">Progress to ${nextTier.icon} ${nextTier.title}: ${progress}%</div>
            <div class="progress-container">
                <div class="progress-bar" style="width: ${progress}%"></div>
            </div>
            <div class="progress-details">${starCount} / ${nextTier.stars} stars</div>
        `;
    } else if (rewardTiers.length > 0) {
        // All tiers completed
        progressSection.innerHTML = `
            <div class="progress-complete">All reading levels achieved! 🎉</div>
        `;
    }
    
    container.appendChild(progressSection);
}

// Update reward message based on progress
function updateRewardMessage() {
    const rewardMessage = document.getElementById('reward-message');
    if (!rewardMessage) return;
    
    const earnedCount = Object.keys(earnedBadges).length;
    const totalStoryBadges = Object.keys(storyBadges).length;
    const totalGameBadges = Object.keys(gameBadges).filter(id => gameBadges[id].age !== 'special').length;
    
    // Get the highest unlocked tier
    let highestTier = null;
    for (let i = rewardTiers.length - 1; i >= 0; i--) {
        if (unlockedTiers[rewardTiers[i].title]) {
            highestTier = rewardTiers[i];
            break;
        }
    }
    
    // Create dynamic message
    if (earnedCount === 0) {
        rewardMessage.innerHTML = `Complete stories and games to earn badges and stars!`;
    } else if (highestTier) {
        // Include tier in message if one is unlocked
        rewardMessage.innerHTML = `
            Amazing! You are a <strong>${highestTier.icon} ${highestTier.title}</strong> with 
            ${earnedCount} badges and ${starCount} stars! ${getRandomEncouragement()}
        `;
    } else {
        // Basic message if no tier is unlocked yet
        rewardMessage.innerHTML = `
            Great job! You've earned ${earnedCount} badges and ${starCount} stars! ${getRandomEncouragement()}
        `;
    }
    
    // Add streak info if there's an active streak
    if (badgeStreak > 1) {
        const streakDiv = document.createElement('div');
        streakDiv.className = 'streak-info';
        streakDiv.innerHTML = `<span class="streak-fire">🔥</span> ${badgeStreak} day streak! Keep it going!`;
        rewardMessage.appendChild(streakDiv);
    }
}

// Get random encouragement message
function getRandomEncouragement() {
    const messages = [
        "Keep up the great work!",
        "You're doing fantastic!",
        "What an achievement!",
        "You're a superstar!",
        "Incredible progress!",
        "Keep reading and playing!"
    ];
    return messages[Math.floor(Math.random() * messages.length)];
}

// Show achievement popup
function showAchievementPopup(icon, title, message) {
    // Create popup element
    const popup = document.createElement('div');
    popup.className = 'achievement-popup';
    
    popup.innerHTML = `
        <div class="achievement-icon">${icon}</div>
        <div class="achievement-text">
            <h4>${title}</h4>
            <p>${message}</p>
        </div>
    `;
    
    // Play achievement sound
    playAchievementSound();
    
    // Add to document
    document.body.appendChild(popup);
    
    // Auto close after 4 seconds
    setTimeout(() => {
        if (document.body.contains(popup)) {
            popup.classList.add('popup-fadeout');
            setTimeout(() => {
                if (document.body.contains(popup)) {
                    document.body.removeChild(popup);
                }
            }, 500);
        }
    }, 4000);
}

// Play achievement sound
function playAchievementSound() {
    try {
        const synth = new Tone.Synth().toDestination();
        const now = Tone.now();
        synth.triggerAttackRelease("C5", "8n", now);
        synth.triggerAttackRelease("E5", "8n", now + 0.1);
        synth.triggerAttackRelease("G5", "8n", now + 0.2);
    } catch (e) {
        console.error("Could not play achievement sound", e);
    }
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

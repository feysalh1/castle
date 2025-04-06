/**
 * Rewards system for Children's Castle
 * This script handles badges, stars, and achievement tracking
 */

// Game badges by category
const gameBadges = {
    age4: [
        { id: 'game_matching_shapes', name: 'Shape Master', icon: '🔷', description: 'Completed the Shape Matching game' },
        { id: 'game_coloring', name: 'Colorful Artist', icon: '🎨', description: 'Created beautiful art in Coloring Fun' },
        { id: 'game_animal_sounds', name: 'Animal Whisperer', icon: '🐘', description: 'Matched all animal sounds correctly' },
        { id: 'game_counting', name: 'Counting Champion', icon: '🔢', description: 'Mastered counting from 1 to 10' }
    ],
    age5: [
        { id: 'game_letter_match', name: 'Letter Genius', icon: '🔤', description: 'Matched all uppercase and lowercase letters' },
        { id: 'game_number_game', name: 'Math Wizard', icon: '➕', description: 'Solved all number problems correctly' },
        { id: 'game_memory_game', name: 'Memory Master', icon: '🧠', description: 'Found all matching pairs in Memory Match' },
        { id: 'game_puzzle', name: 'Puzzle Pro', icon: '🧩', description: 'Completed all puzzles successfully' }
    ]
};

// Story badges
const storyBadges = [
    { id: 'story_little_fox', name: 'Fox Friend', icon: '🦊', description: 'Completed "The Little Fox" story' },
    { id: 'story_three_little_pigs', name: 'Pig Pal', icon: '🐷', description: 'Completed "The Three Little Pigs" story' },
    { id: 'story_goldilocks', name: 'Bear Buddy', icon: '🐻', description: 'Completed "Goldilocks and the Three Bears" story' },
    { id: 'story_wild_things', name: 'Wild Explorer', icon: '🌿', description: 'Completed "Where the Wild Things Are" story' },
    { id: 'story_brown_bear', name: 'Color Spotter', icon: '🎨', description: 'Completed "Brown Bear, Brown Bear" story' },
    { id: 'story_hungry_caterpillar', name: 'Bug Buddy', icon: '🐛', description: 'Completed "The Very Hungry Caterpillar" story' },
    { id: 'story_rainbow_fish', name: 'Fish Friend', icon: '🐠', description: 'Completed "The Rainbow Fish" story' },
    { id: 'story_five_monkeys', name: 'Monkey Business', icon: '🐒', description: 'Completed "Five Little Monkeys" story' },
    { id: 'story_black_sheep', name: 'Wool Gatherer', icon: '🐑', description: 'Completed "Baa Baa Black Sheep" story' },
    { id: 'story_bo_peep', name: 'Shepherd Star', icon: '🌟', description: 'Completed "Little Bo Peep" story' },
    { id: 'story_jack_jill', name: 'Hill Climber', icon: '⛰️', description: 'Completed "Jack and Jill" story' },
    { id: 'story_hickory_dickory', name: 'Time Keeper', icon: '🕰️', description: 'Completed "Hickory Dickory Dock" story' }
];

// Special achievement badges
const specialBadges = [
    { id: 'achievement_first_day', name: 'First Day Fun', icon: '🎉', description: 'Completed your first day of learning' },
    { id: 'achievement_daily_streak_3', name: 'Learning Streak', icon: '🔥', description: 'Visited 3 days in a row' },
    { id: 'achievement_daily_streak_7', name: 'Weekly Wonder', icon: '📅', description: 'Visited 7 days in a row' },
    { id: 'achievement_all_age4_games', name: 'Age 4 Expert', icon: '🏆', description: 'Completed all Age 4 games' },
    { id: 'achievement_all_age5_games', name: 'Age 5 Expert', icon: '🏅', description: 'Completed all Age 5 games' },
    { id: 'achievement_5_stories', name: 'Bookworm', icon: '📚', description: 'Read 5 different stories' },
    { id: 'achievement_all_stories', name: 'Story Master', icon: '📖', description: 'Read all available stories' }
];

// Reward tiers
const rewardTiers = [
    { name: 'Bronze', threshold: 5, icon: '🥉', color: '#cd7f32' },
    { name: 'Silver', threshold: 10, icon: '🥈', color: '#c0c0c0' },
    { name: 'Gold', threshold: 15, icon: '🥇', color: '#ffd700' },
    { name: 'Platinum', threshold: 20, icon: '💎', color: '#e5e4e2' },
    { name: 'Diamond', threshold: 25, icon: '👑', color: '#b9f2ff' }
];

// User rewards data
let userRewards = {
    badges: [],
    stars: 0,
    dailyStreak: 0,
    lastVisit: null
};

// Initialize rewards system
document.addEventListener('DOMContentLoaded', function() {
    loadRewards();
    
    // Update daily streak if on a rewards or dashboard page
    if (document.querySelector('.rewards-page') || document.querySelector('.child-dashboard')) {
        updateBadgeStreak();
    }
    
    // Render badges if on the rewards page
    const badgesContainer = document.getElementById('badges-container');
    if (badgesContainer) {
        renderBadges();
    }
    
    // Update star display
    updateStarDisplay();
    
    // Check for special achievements
    checkSpecialAchievements();
});

/**
 * Load rewards data from database or localStorage
 */
function loadRewards() {
    // Try to load from database first via API
    fetch('/api/get-rewards')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Convert database format to our format
                userRewards.badges = data.rewards.map(reward => reward.badge_id);
                userRewards.stars = data.total_rewards * 5; // Estimate stars based on badges
                
                // Daily streak would need to be calculated from login sessions
                
                // Update UI
                updateStarDisplay();
                
                if (document.querySelector('.rewards-page')) {
                    renderBadges();
                }
            } else {
                // If API fails, fall back to localStorage
                const savedRewards = localStorage.getItem('childrensCastleRewards');
                if (savedRewards) {
                    userRewards = JSON.parse(savedRewards);
                }
            }
        })
        .catch(error => {
            console.error('Error loading rewards:', error);
            
            // Fall back to localStorage
            const savedRewards = localStorage.getItem('childrensCastleRewards');
            if (savedRewards) {
                userRewards = JSON.parse(savedRewards);
            }
        });
}

/**
 * Save rewards data to localStorage
 */
function saveRewards() {
    localStorage.setItem('childrensCastleRewards', JSON.stringify(userRewards));
}

/**
 * Award a badge to the user
 */
function awardBadge(badgeId) {
    // Check if badge is already awarded
    if (userRewards.badges.includes(badgeId)) {
        return false;
    }
    
    // Add badge to user's collection
    userRewards.badges.push(badgeId);
    
    // Award stars for the badge
    awardStars(5);
    
    // Save rewards
    saveRewards();
    
    // Find badge details for the popup
    let badgeDetails = null;
    
    // Check game badges
    for (const category in gameBadges) {
        const badge = gameBadges[category].find(b => b.id === badgeId);
        if (badge) {
            badgeDetails = badge;
            break;
        }
    }
    
    // Check story badges
    if (!badgeDetails) {
        badgeDetails = storyBadges.find(b => b.id === badgeId);
    }
    
    // Check special badges
    if (!badgeDetails) {
        badgeDetails = specialBadges.find(b => b.id === badgeId);
    }
    
    // Show achievement popup if badge details found
    if (badgeDetails) {
        showAchievementPopup(
            badgeDetails.icon,
            'New Badge Earned!',
            `You've earned the "${badgeDetails.name}" badge! ${badgeDetails.description}.`
        );
    }
    
    // Check if this badge unlocks any tier achievements
    checkTierAchievements();
    
    return true;
}

/**
 * Update the daily streak and check for streak achievements
 */
function updateBadgeStreak() {
    const today = new Date().toDateString();
    
    if (!userRewards.lastVisit) {
        // First visit
        userRewards.dailyStreak = 1;
    } else {
        const lastVisit = new Date(userRewards.lastVisit);
        const yesterday = new Date();
        yesterday.setDate(yesterday.getDate() - 1);
        
        if (lastVisit.toDateString() === yesterday.toDateString()) {
            // Consecutive day
            userRewards.dailyStreak++;
            
            // Check for streak achievements
            if (userRewards.dailyStreak === 3) {
                awardBadge('achievement_daily_streak_3');
            } else if (userRewards.dailyStreak === 7) {
                awardBadge('achievement_daily_streak_7');
            }
        } else if (lastVisit.toDateString() !== today) {
            // Non-consecutive visit (but not same day)
            userRewards.dailyStreak = 1;
        }
    }
    
    // Update last visit to today
    userRewards.lastVisit = today;
    saveRewards();
}

/**
 * Check for special achievements based on completed content
 */
function checkSpecialAchievements() {
    // First day achievement (if no badges yet)
    if (userRewards.badges.length === 0) {
        awardBadge('achievement_first_day');
    }
    
    // Count completed stories
    const completedStories = userRewards.badges.filter(badge => badge.startsWith('story_')).length;
    
    // 5 stories achievement
    if (completedStories >= 5 && !userRewards.badges.includes('achievement_5_stories')) {
        awardBadge('achievement_5_stories');
    }
    
    // All stories achievement
    if (completedStories >= storyBadges.length && !userRewards.badges.includes('achievement_all_stories')) {
        awardBadge('achievement_all_stories');
    }
    
    // Check for age category completion
    const completedAge4Games = gameBadges.age4.filter(badge => 
        userRewards.badges.includes(badge.id)
    ).length;
    
    const completedAge5Games = gameBadges.age5.filter(badge => 
        userRewards.badges.includes(badge.id)
    ).length;
    
    // Age 4 Expert achievement
    if (completedAge4Games >= gameBadges.age4.length && !userRewards.badges.includes('achievement_all_age4_games')) {
        awardBadge('achievement_all_age4_games');
    }
    
    // Age 5 Expert achievement
    if (completedAge5Games >= gameBadges.age5.length && !userRewards.badges.includes('achievement_all_age5_games')) {
        awardBadge('achievement_all_age5_games');
    }
}

/**
 * Check for tier achievement badges
 */
function checkTierAchievements() {
    const totalBadges = userRewards.badges.length;
    
    // Check each tier
    for (const tier of rewardTiers) {
        const tierBadgeId = `achievement_tier_${tier.name.toLowerCase()}`;
        
        if (totalBadges >= tier.threshold && !userRewards.badges.includes(tierBadgeId)) {
            // Create a tier badge on the fly
            specialBadges.push({
                id: tierBadgeId,
                name: `${tier.name} Explorer`,
                icon: tier.icon,
                description: `Earned ${tier.threshold} badges!`
            });
            
            // Award the badge
            awardBadge(tierBadgeId);
        }
    }
}

/**
 * Award stars to the user
 */
function awardStars(amount) {
    userRewards.stars += amount;
    saveRewards();
    updateStarDisplay();
    createStarAnimation(amount);
}

/**
 * Update the star display in the UI
 */
function updateStarDisplay() {
    const starDisplay = document.querySelector('.star-count');
    if (starDisplay) {
        starDisplay.textContent = userRewards.stars;
    }
}

/**
 * Create a star animation when stars are awarded
 */
function createStarAnimation(amount) {
    const starDisplay = document.querySelector('.star-count');
    if (!starDisplay) return;
    
    const container = document.createElement('div');
    container.className = 'star-animation-container';
    document.body.appendChild(container);
    
    // Position relative to star display
    const rect = starDisplay.getBoundingClientRect();
    container.style.position = 'fixed';
    container.style.top = `${rect.top}px`;
    container.style.left = `${rect.left}px`;
    container.style.width = `${rect.width}px`;
    container.style.height = `${rect.height}px`;
    container.style.zIndex = '1000';
    container.style.pointerEvents = 'none';
    
    // Create flying stars
    for (let i = 0; i < amount; i++) {
        const star = document.createElement('div');
        star.className = 'flying-star';
        star.textContent = '⭐';
        star.style.position = 'absolute';
        star.style.fontSize = '1.5rem';
        star.style.transform = `translate(${Math.random() * 100 - 50}px, ${Math.random() * 100 - 50}px)`;
        star.style.opacity = '0';
        star.style.transition = 'all 1s ease-out';
        container.appendChild(star);
        
        // Animate star
        setTimeout(() => {
            star.style.transform = 'translate(0, 0)';
            star.style.opacity = '1';
        }, 50 + i * 100);
    }
    
    // Remove animation container after animation
    setTimeout(() => {
        container.remove();
    }, 2000);
}

/**
 * Render badges in the badges container
 */
function renderBadges() {
    const badgesContainer = document.getElementById('badges-container');
    if (!badgesContainer) return;
    
    badgesContainer.innerHTML = '';
    
    // Add game badges sections
    addGameBadgeSection(badgesContainer, 'Age 4 Games', 'age4');
    addGameBadgeSection(badgesContainer, 'Age 5+ Games', 'age5');
    
    // Add stories section
    const storiesSection = document.createElement('div');
    storiesSection.className = 'badge-section';
    storiesSection.innerHTML = `<h3>Story Badges</h3>`;
    
    const storiesBadges = document.createElement('div');
    storiesBadges.className = 'badges-grid';
    
    storyBadges.forEach(badge => {
        const badgeElement = document.createElement('div');
        badgeElement.className = `badge-item ${userRewards.badges.includes(badge.id) ? 'earned' : 'locked'}`;
        
        badgeElement.innerHTML = `
            <div class="badge-icon">${badge.icon}</div>
            <div class="badge-info">
                <h4>${badge.name}</h4>
                <p>${badge.description}</p>
            </div>
        `;
        
        storiesBadges.appendChild(badgeElement);
    });
    
    storiesSection.appendChild(storiesBadges);
    badgesContainer.appendChild(storiesSection);
    
    // Add special achievements section
    const specialSection = document.createElement('div');
    specialSection.className = 'badge-section';
    specialSection.innerHTML = `<h3>Special Achievements</h3>`;
    
    const specialBadges = document.createElement('div');
    specialBadges.className = 'badges-grid';
    
    specialBadges.forEach(badge => {
        const badgeElement = document.createElement('div');
        badgeElement.className = `badge-item ${userRewards.badges.includes(badge.id) ? 'earned' : 'locked'}`;
        
        badgeElement.innerHTML = `
            <div class="badge-icon">${badge.icon}</div>
            <div class="badge-info">
                <h4>${badge.name}</h4>
                <p>${badge.description}</p>
            </div>
        `;
        
        specialBadges.appendChild(badgeElement);
    });
    
    specialSection.appendChild(specialBadges);
    badgesContainer.appendChild(specialSection);
    
    // Add reward tiers section
    addRewardTiersSection(badgesContainer);
    
    // Add reward message
    updateRewardMessage();
}

/**
 * Add a game badge section to the container
 */
function addGameBadgeSection(container, title, age) {
    const section = document.createElement('div');
    section.className = 'badge-section';
    section.innerHTML = `<h3>${title}</h3>`;
    
    const badgesGrid = document.createElement('div');
    badgesGrid.className = 'badges-grid';
    
    gameBadges[age].forEach(badge => {
        const badgeElement = document.createElement('div');
        badgeElement.className = `badge-item ${userRewards.badges.includes(badge.id) ? 'earned' : 'locked'}`;
        
        badgeElement.innerHTML = `
            <div class="badge-icon">${badge.icon}</div>
            <div class="badge-info">
                <h4>${badge.name}</h4>
                <p>${badge.description}</p>
            </div>
        `;
        
        badgesGrid.appendChild(badgeElement);
    });
    
    section.appendChild(badgesGrid);
    container.appendChild(section);
}

/**
 * Add reward tiers section to the container
 */
function addRewardTiersSection(container) {
    const section = document.createElement('div');
    section.className = 'badge-section rewards-tier-section';
    section.innerHTML = `<h3>Reward Tiers</h3>`;
    
    const tiersGrid = document.createElement('div');
    tiersGrid.className = 'tiers-grid';
    
    // Total badges count
    const totalBadges = userRewards.badges.length;
    
    rewardTiers.forEach(tier => {
        const tierElement = document.createElement('div');
        tierElement.className = `tier-item ${totalBadges >= tier.threshold ? 'achieved' : 'locked'}`;
        tierElement.style.setProperty('--tier-color', tier.color);
        
        tierElement.innerHTML = `
            <div class="tier-icon">${tier.icon}</div>
            <div class="tier-info">
                <h4>${tier.name}</h4>
                <div class="tier-progress">
                    <div class="tier-progress-bar">
                        <div class="tier-progress-fill" style="width: ${Math.min(100, (totalBadges / tier.threshold) * 100)}%"></div>
                    </div>
                    <div class="tier-progress-text">${totalBadges}/${tier.threshold} badges</div>
                </div>
            </div>
        `;
        
        tiersGrid.appendChild(tierElement);
    });
    
    section.appendChild(tiersGrid);
    container.appendChild(section);
}

/**
 * Update the encouragement message in the rewards page
 */
function updateRewardMessage() {
    const messageContainer = document.querySelector('.rewards-message');
    if (!messageContainer) return;
    
    const totalBadges = userRewards.badges.length;
    let nextTier = null;
    
    // Find the next tier to reach
    for (const tier of rewardTiers) {
        if (totalBadges < tier.threshold) {
            nextTier = tier;
            break;
        }
    }
    
    // Create message
    if (nextTier) {
        const badgesNeeded = nextTier.threshold - totalBadges;
        messageContainer.innerHTML = `
            <p>${getRandomEncouragement()} You need ${badgesNeeded} more ${badgesNeeded === 1 ? 'badge' : 'badges'} to reach the ${nextTier.name} tier!</p>
        `;
    } else {
        // All tiers achieved
        messageContainer.innerHTML = `
            <p>Amazing! You've reached the highest reward tier. Keep exploring to earn all badges!</p>
        `;
    }
}

/**
 * Get a random encouragement message
 */
function getRandomEncouragement() {
    const messages = [
        "You're doing great!",
        "Wow, look at all your badges!",
        "You're a super learner!",
        "Fantastic progress!",
        "You're on a roll!",
        "Amazing work so far!",
        "Keep up the great work!"
    ];
    
    return messages[Math.floor(Math.random() * messages.length)];
}

/**
 * Show achievement popup
 */
function showAchievementPopup(icon, title, message) {
    // Create popup element
    const popup = document.createElement('div');
    popup.className = 'achievement-popup';
    popup.innerHTML = `
        <div class="achievement-icon">${icon}</div>
        <div class="achievement-content">
            <h3>${title}</h3>
            <p>${message}</p>
        </div>
    `;
    
    // Add to document
    document.body.appendChild(popup);
    
    // Play sound
    playAchievementSound();
    
    // Show popup with animation
    setTimeout(() => {
        popup.classList.add('visible');
    }, 100);
    
    // Remove popup after delay
    setTimeout(() => {
        popup.classList.remove('visible');
        setTimeout(() => {
            popup.remove();
        }, 500);
    }, 5000);
}

/**
 * Play achievement sound
 */
function playAchievementSound() {
    const audio = new Audio('/static/audio/achievement.mp3');
    audio.volume = 0.6;
    audio.play();
}

/**
 * Award a story completion badge
 */
function awardStoryCompletionBadge(storyId) {
    awardBadge(`story_${storyId}`);
}

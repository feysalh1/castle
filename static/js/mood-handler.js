/**
 * Mood Handler for Story Mode
 * Handles mood-specific adjustments to the story experience
 */

document.addEventListener('DOMContentLoaded', function() {
    // Check if we have an active mood
    const activeMoodElement = document.getElementById('active-mood');
    if (!activeMoodElement) return;
    
    // Get mood data
    const moodType = activeMoodElement.dataset.mood;
    const moodIntensity = parseInt(activeMoodElement.dataset.intensity || '5');
    const colorTheme = activeMoodElement.dataset.color;
    const backgroundMusic = activeMoodElement.dataset.music;
    
    console.log(`Active mood: ${moodType} (intensity: ${moodIntensity})`);
    
    // Apply mood-specific adjustments
    applyMoodAdjustments(moodType, moodIntensity, colorTheme);
    
    // If background music is specified, play it
    if (backgroundMusic) {
        playBackgroundMusic(backgroundMusic, moodIntensity);
    }
    
    // Add animation effects based on mood
    addMoodAnimations(moodType, moodIntensity);
});

/**
 * Apply mood-specific adjustments to the page
 */
function applyMoodAdjustments(moodType, intensity, colorTheme) {
    const storyTextElements = document.querySelectorAll('.story-text p');
    const storyContainer = document.querySelector('.story-container');
    
    if (!storyContainer) return;
    
    // Adjust text styles based on mood
    switch(moodType) {
        case 'happy':
            // Brighter, more playful text
            storyTextElements.forEach(el => {
                el.style.fontSize = `${2 + (intensity * 0.05)}rem`;
                el.style.lineHeight = '1.8';
                el.style.color = '#333';
            });
            // Adjust border colors
            if (storyContainer) {
                storyContainer.style.boxShadow = '0 8px 30px rgba(255, 193, 7, 0.3)';
            }
            break;
            
        case 'calm':
            // Softer, more relaxed text
            storyTextElements.forEach(el => {
                el.style.fontSize = `${1.8 + (intensity * 0.03)}rem`;
                el.style.lineHeight = '1.9';
                el.style.color = '#445';
                el.style.fontWeight = '400';
            });
            // Adjust border colors
            if (storyContainer) {
                storyContainer.style.boxShadow = '0 8px 30px rgba(3, 169, 244, 0.2)';
            }
            break;
            
        case 'adventurous':
            // Bold, exciting text
            storyTextElements.forEach(el => {
                el.style.fontSize = `${2.1 + (intensity * 0.07)}rem`;
                el.style.lineHeight = '1.7';
                el.style.color = '#333';
                el.style.fontWeight = '500';
            });
            // Adjust border colors
            if (storyContainer) {
                storyContainer.style.boxShadow = '0 8px 30px rgba(233, 30, 99, 0.2)';
            }
            break;
            
        case 'sleepy':
            // Gentle, dreamy text
            storyTextElements.forEach(el => {
                el.style.fontSize = `${1.7 + (intensity * 0.04)}rem`;
                el.style.lineHeight = '2.0';
                el.style.color = '#445';
                el.style.fontWeight = '300';
            });
            // Adjust border colors
            if (storyContainer) {
                storyContainer.style.boxShadow = '0 8px 30px rgba(123, 31, 162, 0.2)';
            }
            break;
            
        case 'curious':
            // Inquisitive, engaging text
            storyTextElements.forEach(el => {
                el.style.fontSize = `${2.0 + (intensity * 0.05)}rem`;
                el.style.lineHeight = '1.8';
                el.style.color = '#3e4a59';
            });
            // Adjust border colors
            if (storyContainer) {
                storyContainer.style.boxShadow = '0 8px 30px rgba(0, 150, 136, 0.2)';
            }
            break;
    }
    
    // Apply color theme if specified
    if (colorTheme) {
        document.documentElement.style.setProperty('--mood-color', colorTheme);
    }
}

/**
 * Play background music appropriate for the mood
 */
function playBackgroundMusic(musicUrl, intensity) {
    // Check if we already have an audio element
    let audioElement = document.getElementById('mood-background-music');
    
    if (!audioElement) {
        // Create a new audio element
        audioElement = document.createElement('audio');
        audioElement.id = 'mood-background-music';
        audioElement.loop = true;
        
        // Calculate volume based on intensity (0.1 to 0.4)
        const volume = 0.1 + (intensity / 30);
        audioElement.volume = Math.min(volume, 0.4);
        
        // Add source
        const source = document.createElement('source');
        source.src = musicUrl;
        source.type = 'audio/mp3';
        audioElement.appendChild(source);
        
        // Add to page
        document.body.appendChild(audioElement);
        
        // Play when user interacts with the page
        document.addEventListener('click', function() {
            audioElement.play().catch(err => {
                console.log('Could not play audio: ', err);
            });
        }, { once: true });
    }
}

/**
 * Add mood-specific animations to the page
 */
function addMoodAnimations(moodType, intensity) {
    // Create a container for animations if needed
    let animationContainer = document.getElementById('mood-animations');
    if (!animationContainer) {
        animationContainer = document.createElement('div');
        animationContainer.id = 'mood-animations';
        document.body.appendChild(animationContainer);
    }
    
    // Clear existing animations
    animationContainer.innerHTML = '';
    
    // Add animations based on mood
    switch(moodType) {
        case 'happy':
            // Add floating sun rays or bubbles
            const numBubbles = Math.floor(5 + (intensity * 1.5));
            for (let i = 0; i < numBubbles; i++) {
                const bubble = document.createElement('div');
                bubble.className = 'mood-bubble';
                bubble.style.left = `${Math.random() * 100}%`;
                bubble.style.animationDuration = `${5 + Math.random() * 10}s`;
                bubble.style.animationDelay = `${Math.random() * 5}s`;
                bubble.style.width = `${20 + Math.random() * 30}px`;
                bubble.style.height = bubble.style.width;
                animationContainer.appendChild(bubble);
            }
            break;
            
        case 'calm':
            // Add gentle floating clouds
            const numClouds = Math.floor(3 + (intensity * 0.8));
            for (let i = 0; i < numClouds; i++) {
                const cloud = document.createElement('div');
                cloud.className = 'mood-cloud';
                cloud.style.top = `${Math.random() * 70}%`;
                cloud.style.animationDuration = `${20 + Math.random() * 40}s`;
                cloud.style.animationDelay = `${Math.random() * 10}s`;
                cloud.style.opacity = 0.2 + (Math.random() * 0.3);
                animationContainer.appendChild(cloud);
            }
            break;
            
        case 'adventurous':
            // Add shooting stars or dynamic elements
            const numStars = Math.floor(2 + (intensity * 0.8));
            for (let i = 0; i < numStars; i++) {
                const star = document.createElement('div');
                star.className = 'shooting-star';
                star.style.top = `${Math.random() * 40}%`;
                star.style.left = `${Math.random() * 30}%`;
                star.style.animationDuration = `${1 + Math.random() * 2}s`;
                star.style.animationDelay = `${i * 3 + Math.random() * 5}s`;
                animationContainer.appendChild(star);
            }
            break;
            
        case 'sleepy':
            // Add twinkling stars or gentle falling elements
            const numTwinkles = Math.floor(20 + (intensity * 3));
            for (let i = 0; i < numTwinkles; i++) {
                const star = document.createElement('div');
                star.className = 'twinkling-star';
                star.style.top = `${Math.random() * 100}%`;
                star.style.left = `${Math.random() * 100}%`;
                star.style.animationDuration = `${2 + Math.random() * 4}s`;
                star.style.animationDelay = `${Math.random() * 5}s`;
                star.style.width = `${1 + Math.random() * 3}px`;
                star.style.height = star.style.width;
                animationContainer.appendChild(star);
            }
            break;
            
        case 'curious':
            // Add question marks or thought bubbles that appear and disappear
            const numBubbles = Math.floor(4 + (intensity * 0.7));
            for (let i = 0; i < numBubbles; i++) {
                const thought = document.createElement('div');
                thought.className = 'thought-bubble';
                thought.style.top = `${Math.random() * 70}%`;
                thought.style.left = `${Math.random() * 80}%`;
                thought.style.animationDuration = `${8 + Math.random() * 7}s`;
                thought.style.animationDelay = `${i * 2 + Math.random() * 5}s`;
                thought.innerHTML = '?';
                animationContainer.appendChild(thought);
            }
            break;
    }
    
    // Add CSS for animations
    addAnimationStyles(moodType);
}

/**
 * Add CSS styles for mood animations
 */
function addAnimationStyles(moodType) {
    // Check if we already have a style element
    let styleElement = document.getElementById('mood-animation-styles');
    if (!styleElement) {
        styleElement = document.createElement('style');
        styleElement.id = 'mood-animation-styles';
        document.head.appendChild(styleElement);
    }
    
    // Define animation styles based on mood
    let css = '';
    
    switch(moodType) {
        case 'happy':
            css = `
                #mood-animations { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
                .mood-bubble {
                    position: absolute;
                    bottom: -20px;
                    background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.8), rgba(255, 255, 0, 0.2));
                    border-radius: 50%;
                    animation: floatBubble linear infinite;
                }
                @keyframes floatBubble {
                    0% { transform: translateY(100vh) scale(1); opacity: 0.7; }
                    100% { transform: translateY(-100px) scale(1.2); opacity: 0; }
                }
            `;
            break;
            
        case 'calm':
            css = `
                #mood-animations { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
                .mood-cloud {
                    position: absolute;
                    width: 180px;
                    height: 60px;
                    background: rgba(255, 255, 255, 0.4);
                    border-radius: 50px;
                    box-shadow: 0 8px 5px rgba(0, 0, 0, 0.1);
                    animation: floatCloud linear infinite;
                    left: -200px;
                }
                .mood-cloud:before, .mood-cloud:after {
                    content: '';
                    position: absolute;
                    background: rgba(255, 255, 255, 0.4);
                    border-radius: 50%;
                }
                .mood-cloud:before {
                    width: 100px;
                    height: 100px;
                    top: -40px;
                    left: 25px;
                }
                .mood-cloud:after {
                    width: 80px;
                    height: 80px;
                    top: -30px;
                    left: 90px;
                }
                @keyframes floatCloud {
                    0% { transform: translateX(0); }
                    100% { transform: translateX(calc(100vw + 400px)); }
                }
            `;
            break;
            
        case 'adventurous':
            css = `
                #mood-animations { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
                .shooting-star {
                    position: absolute;
                    width: 100px;
                    height: 2px;
                    background: linear-gradient(to right, rgba(255, 255, 255, 0), #fff, rgba(255, 255, 255, 0));
                    transform: rotate(45deg);
                    animation: shootingStar linear infinite;
                }
                .shooting-star:after {
                    content: '';
                    position: absolute;
                    top: 0;
                    right: 0;
                    width: 20px;
                    height: 2px;
                    background: linear-gradient(to right, rgba(255, 255, 255, 0), rgba(255, 255, 255, 0.8));
                    border-radius: 50%;
                    filter: blur(1px);
                }
                @keyframes shootingStar {
                    0% { transform: translateX(0) translateY(0) rotate(45deg); opacity: 1; }
                    20% { opacity: 1; }
                    80% { opacity: 0; }
                    100% { transform: translateX(400px) translateY(400px) rotate(45deg); opacity: 0; }
                }
            `;
            break;
            
        case 'sleepy':
            css = `
                #mood-animations { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
                .twinkling-star {
                    position: absolute;
                    background-color: #fff;
                    border-radius: 50%;
                    animation: twinkle ease-in-out infinite;
                }
                @keyframes twinkle {
                    0% { opacity: 0.2; transform: scale(1); }
                    50% { opacity: 0.8; transform: scale(1.2); }
                    100% { opacity: 0.2; transform: scale(1); }
                }
            `;
            break;
            
        case 'curious':
            css = `
                #mood-animations { position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 1; }
                .thought-bubble {
                    position: absolute;
                    width: 30px;
                    height: 30px;
                    background-color: rgba(255, 255, 255, 0.8);
                    border-radius: 50%;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-weight: bold;
                    font-size: 20px;
                    color: #7e57c2;
                    animation: thoughtAppear ease-in-out infinite;
                }
                @keyframes thoughtAppear {
                    0% { opacity: 0; transform: scale(0); }
                    20% { opacity: 1; transform: scale(1); }
                    80% { opacity: 1; transform: scale(1); }
                    100% { opacity: 0; transform: scale(0); }
                }
            `;
            break;
    }
    
    styleElement.innerHTML = css;
}
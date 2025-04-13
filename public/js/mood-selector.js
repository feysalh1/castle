document.addEventListener('DOMContentLoaded', function() {
    // Get all mood cards
    const moodCards = document.querySelectorAll('.mood-card');
    const saveButton = document.getElementById('save-mood');
    let selectedMood = document.querySelector('.mood-card.active')?.dataset.mood || 'happy';
    
    // Add click event to mood cards
    moodCards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove active class from all cards
            moodCards.forEach(c => c.classList.remove('active'));
            
            // Add active class to clicked card
            this.classList.add('active');
            
            // Store selected mood
            selectedMood = this.dataset.mood;
            
            // Apply background color effect
            applyBackgroundEffect(this.dataset.color);
        });
    });
    
    // Handle intensity slider changes
    const intensitySliders = document.querySelectorAll('.intensity-slider');
    intensitySliders.forEach(slider => {
        slider.addEventListener('input', function() {
            // If user adjusts a slider, automatically select that mood
            const moodType = this.dataset.mood;
            const moodCard = document.querySelector(`.mood-card[data-mood="${moodType}"]`);
            
            // Activate the corresponding mood card
            moodCards.forEach(c => c.classList.remove('active'));
            moodCard.classList.add('active');
            selectedMood = moodType;
            
            // Apply background color effect
            applyBackgroundEffect(moodCard.dataset.color);
        });
    });
    
    // Save button functionality
    saveButton.addEventListener('click', function() {
        const activeCard = document.querySelector('.mood-card.active');
        if (!activeCard) {
            alert('Please select a mood first');
            return;
        }
        
        const moodType = activeCard.dataset.mood;
        const intensitySlider = document.querySelector(`.intensity-slider[data-mood="${moodType}"]`);
        const intensity = intensitySlider.value;
        
        // Save mood via API
        saveMoodSelection(moodType, intensity);
    });
    
    // Function to save mood selection
    function saveMoodSelection(moodType, intensity) {
        fetch('/api/save-mood', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                mood_type: moodType,
                intensity: intensity
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Redirect to story mode with mood applied
                window.location.href = '/story-mode';
            } else {
                console.error('Error saving mood:', data.message);
                alert('There was an error saving your mood. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was a connection error. Please try again.');
        });
    }
    
    // Function to apply background color effect based on mood
    function applyBackgroundEffect(color) {
        if (!color) return;
        
        // Apply a subtle background gradient
        document.body.style.backgroundImage = `linear-gradient(to bottom, ${color}22, #f5f5f5)`;
        
        // Also change the container border color
        const container = document.querySelector('.mood-selector-container');
        container.style.borderLeft = `5px solid ${color}`;
    }
    
    // Apply initial background effect if there's an active mood
    const initialActiveCard = document.querySelector('.mood-card.active');
    if (initialActiveCard) {
        applyBackgroundEffect(initialActiveCard.dataset.color);
    }
    
    // Handle animation effects
    animateMoodCards();
    
    function animateMoodCards() {
        moodCards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
    }
});
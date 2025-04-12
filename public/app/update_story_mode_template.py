#!/usr/bin/env python3
"""
Script to update the story_mode.html template to display books by age categories.
"""

import os
from flask import Flask
from models import db, AgeGroup, Book

# Create a Flask app context for database operations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}
db.init_app(app)

# HTML template for the updated story mode page
TEMPLATE = """{% extends "base.html" %}

{% block title %}Story Mode - Children's Castle{% endblock %}

{% block styles %}
<link rel="stylesheet" href="{{ url_for('static', filename='css/story_mode.css') }}">
{% endblock %}

{% block content %}
<div class="container">
    <div class="story-mode-container">
        <h1 class="story-title">Story Mode</h1>
        <p class="story-intro">Welcome to Story Mode! Choose a story to begin your adventure.</p>
        
        <div class="age-filters">
            <label for="age-filter">Filter by age:</label>
            <select id="age-filter" class="form-control">
                <option value="all">All Ages</option>
                {% for age_group in age_groups %}
                <option value="{{ age_group.id }}">{{ age_group.name }} ({{ age_group.min_age }}-{{ age_group.max_age }} years)</option>
                {% endfor %}
            </select>
        </div>
        
        {% for age_group in age_groups %}
        <div class="age-group-section" data-age-group="{{ age_group.id }}">
            <h2 class="age-group-title">{{ age_group.name }} ({{ age_group.min_age }}-{{ age_group.max_age }} years)</h2>
            <p class="age-group-description">{{ age_group.description }}</p>
            
            <div class="story-grid">
                {% for book in books %}
                {% if book.age_group_id == age_group.id %}
                <div class="story-card" data-story-id="{{ book.file_name|replace('.txt', '') }}">
                    <div class="story-icon">
                        <i class="fas fa-book-open"></i>
                    </div>
                    <div class="story-info">
                        <h3 class="story-card-title">{{ book.title }}</h3>
                        <p class="story-author">By {{ book.author }}</p>
                        <p class="story-description">{{ book.description }}</p>
                        <div class="story-metadata">
                            <span class="difficulty-badge {{ book.difficulty_level }}">{{ book.difficulty_level|capitalize }}</span>
                            <span class="reading-time"><i class="far fa-clock"></i> {{ book.reading_time_minutes }} mins</span>
                        </div>
                    </div>
                </div>
                {% endif %}
                {% endfor %}
            </div>
        </div>
        {% endfor %}
    </div>
    
    <div class="story-view-container hidden">
        <button class="btn btn-primary back-to-stories"><i class="fas fa-arrow-left"></i> Back to Stories</button>
        <h2 id="current-story-title">Story Title</h2>
        <div id="story-text-container">
            <p id="story-text">Loading story...</p>
        </div>
        <div class="story-controls">
            <button class="btn btn-secondary" id="toggle-narration">
                <i class="fas fa-volume-up"></i> 
                <span>Start Narration</span>
            </button>
            <select id="voice-selector" class="form-control">
                <option value="">Select Voice</option>
            </select>
            <div class="feedback-emoji">
                <span class="emoji-label">How did you like this story?</span>
                <div class="emoji-options">
                    <span class="emoji" data-reaction="love">❤️</span>
                    <span class="emoji" data-reaction="happy">😃</span>
                    <span class="emoji" data-reaction="neutral">😐</span>
                    <span class="emoji" data-reaction="sad">😢</span>
                    <span class="emoji" data-reaction="confused">🤔</span>
                </div>
            </div>
        </div>
    </div>
</div>
{% endblock %}

{% block scripts %}
<script src="{{ url_for('static', filename='js/story_mode.js') }}"></script>
{% endblock %}
"""

def update_story_mode_template():
    """Update the story_mode.html template"""
    template_path = "templates/story_mode.html"
    
    # Create templates directory if it doesn't exist
    os.makedirs("templates", exist_ok=True)
    
    # Write the template to file
    with open(template_path, "w") as f:
        f.write(TEMPLATE)
    
    print(f"Updated {template_path}")

def create_story_mode_css():
    """Create or update the story_mode.css file"""
    css_content = """/* Story Mode Styles */
.story-mode-container {
    padding: 20px;
    animation: fadeIn 0.5s ease-in-out;
}

.story-title {
    color: #4a4a9c;
    margin-bottom: 20px;
    font-size: 2.5rem;
    text-align: center;
}

.story-intro {
    text-align: center;
    margin-bottom: 30px;
    font-size: 1.2rem;
    color: #555;
}

.age-filters {
    margin-bottom: 30px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 10px;
    display: flex;
    align-items: center;
    gap: 15px;
}

.age-filters label {
    font-weight: bold;
    margin-bottom: 0;
}

.age-group-section {
    margin-bottom: 40px;
    padding: 15px;
    border-radius: 10px;
    animation: fadeIn 0.5s ease-in-out;
}

.age-group-title {
    color: #4a4a9c;
    border-bottom: 2px solid #e0e0ff;
    padding-bottom: 10px;
    margin-bottom: 15px;
}

.age-group-description {
    margin-bottom: 20px;
    color: #555;
    font-style: italic;
}

.story-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-top: 20px;
}

.story-card {
    border: 1px solid #e0e0ff;
    border-radius: 10px;
    padding: 15px;
    display: flex;
    cursor: pointer;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    background-color: white;
}

.story-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.story-icon {
    font-size: 2rem;
    color: #4a4a9c;
    margin-right: 15px;
    display: flex;
    align-items: center;
}

.story-info {
    flex: 1;
}

.story-card-title {
    margin-top: 0;
    margin-bottom: 5px;
    color: #4a4a9c;
}

.story-author {
    font-style: italic;
    margin-bottom: 10px;
    color: #666;
}

.story-description {
    font-size: 0.9rem;
    margin-bottom: 10px;
}

.story-metadata {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 10px;
}

.difficulty-badge {
    padding: 3px 8px;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: bold;
}

.difficulty-badge.easy {
    background-color: #d4edda;
    color: #155724;
}

.difficulty-badge.medium {
    background-color: #fff3cd;
    color: #856404;
}

.difficulty-badge.hard {
    background-color: #f8d7da;
    color: #721c24;
}

.reading-time {
    font-size: 0.8rem;
    color: #666;
}

.story-view-container {
    padding: 20px;
    animation: fadeIn 0.5s ease-in-out;
}

.back-to-stories {
    margin-bottom: 20px;
}

#current-story-title {
    color: #4a4a9c;
    margin-bottom: 20px;
}

#story-text-container {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    min-height: 300px;
    white-space: pre-line;
    line-height: 1.6;
}

.story-controls {
    display: flex;
    flex-wrap: wrap;
    gap: 15px;
    align-items: center;
    margin-top: 20px;
    padding: 15px;
    background-color: #f8f9fa;
    border-radius: 10px;
}

#voice-selector {
    width: auto;
    min-width: 150px;
}

.feedback-emoji {
    margin-left: auto;
    display: flex;
    align-items: center;
    gap: 10px;
}

.emoji-label {
    font-weight: bold;
}

.emoji-options {
    display: flex;
    gap: 10px;
}

.emoji {
    font-size: 1.5rem;
    cursor: pointer;
    transition: transform 0.2s ease;
}

.emoji:hover {
    transform: scale(1.2);
}

.emoji.selected {
    transform: scale(1.2);
    position: relative;
}

.emoji.selected::after {
    content: '';
    position: absolute;
    bottom: -5px;
    left: 50%;
    transform: translateX(-50%);
    width: 5px;
    height: 5px;
    background-color: #4a4a9c;
    border-radius: 50%;
}

.hidden {
    display: none;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Mobile Responsiveness */
@media (max-width: 768px) {
    .story-grid {
        grid-template-columns: 1fr;
    }
    
    .story-controls {
        flex-direction: column;
        align-items: stretch;
    }
    
    .feedback-emoji {
        margin-left: 0;
        flex-direction: column;
        align-items: flex-start;
    }
}
"""
    
    # Create static/css directory if it doesn't exist
    os.makedirs("static/css", exist_ok=True)
    
    # Write the CSS to file
    css_path = "static/css/story_mode.css"
    with open(css_path, "w") as f:
        f.write(css_content)
    
    print(f"Created/updated {css_path}")

def create_story_mode_js():
    """Create or update the story_mode.js file"""
    js_content = """// Story Mode JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const storyModeContainer = document.querySelector('.story-mode-container');
    const storyViewContainer = document.querySelector('.story-view-container');
    const backToStoriesBtn = document.querySelector('.back-to-stories');
    const currentStoryTitle = document.getElementById('current-story-title');
    const storyTextContainer = document.getElementById('story-text-container');
    const storyText = document.getElementById('story-text');
    const toggleNarrationBtn = document.getElementById('toggle-narration');
    const voiceSelector = document.getElementById('voice-selector');
    const ageFilter = document.getElementById('age-filter');
    const emojiOptions = document.querySelectorAll('.emoji');
    
    // Variables
    let currentStoryId = null;
    let narrationAudio = null;
    let isNarrating = false;
    
    // Initialize
    loadVoices();
    
    // Event Listeners
    ageFilter.addEventListener('change', filterByAgeGroup);
    
    document.querySelectorAll('.story-card').forEach(card => {
        card.addEventListener('click', function() {
            const storyId = this.dataset.storyId;
            loadStory(storyId);
        });
    });
    
    backToStoriesBtn.addEventListener('click', function() {
        storyViewContainer.classList.add('hidden');
        storyModeContainer.classList.remove('hidden');
        
        // Stop narration if it's playing
        if (isNarrating) {
            stopNarration();
        }
    });
    
    toggleNarrationBtn.addEventListener('click', function() {
        if (isNarrating) {
            stopNarration();
        } else {
            startNarration();
        }
    });
    
    emojiOptions.forEach(emoji => {
        emoji.addEventListener('click', function() {
            const reaction = this.dataset.reaction;
            submitEmotionalFeedback(reaction);
            
            // Visual feedback
            emojiOptions.forEach(e => e.classList.remove('selected'));
            this.classList.add('selected');
        });
    });
    
    // Functions
    function filterByAgeGroup() {
        const selectedAgeGroupId = parseInt(ageFilter.value);
        const ageGroupSections = document.querySelectorAll('.age-group-section');
        
        if (selectedAgeGroupId === 'all' || isNaN(selectedAgeGroupId)) {
            // Show all age groups
            ageGroupSections.forEach(section => {
                section.style.display = 'block';
            });
        } else {
            // Show only the selected age group
            ageGroupSections.forEach(section => {
                if (parseInt(section.dataset.ageGroup) === selectedAgeGroupId) {
                    section.style.display = 'block';
                } else {
                    section.style.display = 'none';
                }
            });
        }
    }
    
    function loadStory(storyId) {
        currentStoryId = storyId;
        
        // Show loading state
        storyText.textContent = 'Loading story...';
        
        // Find the story card to get the title
        const storyCard = document.querySelector(`[data-story-id="${storyId}"]`);
        const title = storyCard.querySelector('.story-card-title').textContent;
        currentStoryTitle.textContent = title;
        
        // Show the story view
        storyModeContainer.classList.add('hidden');
        storyViewContainer.classList.remove('hidden');
        
        // Fetch the story content
        fetch(`/api/story/${storyId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Story not found');
                }
                return response.json();
            })
            .then(data => {
                storyText.textContent = data.content;
                
                // Track story view
                trackProgress(storyId, 'view');
            })
            .catch(error => {
                storyText.textContent = `Error loading story: ${error.message}`;
            });
    }
    
    function loadVoices() {
        // Clear existing options except the default
        while (voiceSelector.options.length > 1) {
            voiceSelector.remove(1);
        }
        
        // Fetch available voices from the server
        fetch('/api/list-voices')
            .then(response => response.json())
            .then(data => {
                data.voices.forEach(voice => {
                    const option = document.createElement('option');
                    option.value = voice.voice_id;
                    option.textContent = voice.name;
                    voiceSelector.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error loading voices:', error);
            });
    }
    
    function startNarration() {
        const selectedVoice = voiceSelector.value;
        
        if (!selectedVoice) {
            alert('Please select a voice for narration');
            return;
        }
        
        // Get the story text
        const textToNarrate = storyText.textContent;
        
        // Show loading state
        toggleNarrationBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
        
        // Generate narration
        fetch('/api/generate-voice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                text: textToNarrate,
                voice_id: selectedVoice
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Create audio element
                narrationAudio = new Audio(data.audio_url);
                
                // Play audio
                narrationAudio.play();
                isNarrating = true;
                
                // Update button
                toggleNarrationBtn.innerHTML = '<i class="fas fa-volume-mute"></i> Stop Narration';
                
                // When audio ends
                narrationAudio.onended = function() {
                    stopNarration();
                };
                
                // Track narration
                trackProgress(currentStoryId, 'narration');
            } else {
                throw new Error(data.message || 'Failed to generate narration');
            }
        })
        .catch(error => {
            alert(`Error generating narration: ${error.message}`);
            toggleNarrationBtn.innerHTML = '<i class="fas fa-volume-up"></i> Start Narration';
        });
    }
    
    function stopNarration() {
        if (narrationAudio) {
            narrationAudio.pause();
            narrationAudio.currentTime = 0;
        }
        
        isNarrating = false;
        toggleNarrationBtn.innerHTML = '<i class="fas fa-volume-up"></i> Start Narration';
    }
    
    function trackProgress(storyId, action) {
        // Send tracking data to the server
        fetch('/api/track-progress', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content_type: 'story',
                content_id: storyId,
                action: action,
                time_spent: action === 'complete' ? 300 : 0 // Example: 5 minutes for completion
            })
        })
        .catch(error => {
            console.error('Error tracking progress:', error);
        });
    }
    
    function submitEmotionalFeedback(reaction) {
        // Send emotional feedback to the server
        fetch('/api/record-emotional-feedback', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                content_type: 'story',
                content_id: currentStoryId,
                reaction: reaction
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Feedback submitted:', data);
        })
        .catch(error => {
            console.error('Error submitting feedback:', error);
        });
    }
});
"""
    
    # Create static/js directory if it doesn't exist
    os.makedirs("static/js", exist_ok=True)
    
    # Write the JS to file
    js_path = "static/js/story_mode.js"
    with open(js_path, "w") as f:
        f.write(js_content)
    
    print(f"Created/updated {js_path}")

def main():
    """Main function to run the script"""
    with app.app_context():
        print("Updating story mode template and assets...")
        
        # Update the story_mode.html template
        update_story_mode_template()
        
        # Create or update the story_mode.css file
        create_story_mode_css()
        
        # Create or update the story_mode.js file
        create_story_mode_js()
        
        print("Update complete!")

if __name__ == "__main__":
    main()
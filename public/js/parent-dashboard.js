/**
 * Parent Dashboard Functionality
 * Handles all interactive elements of the parent dashboard
 */
document.addEventListener('DOMContentLoaded', function() {
    initParentDashboard();
});

/**
 * Initialize the parent dashboard
 */
function initParentDashboard() {
    // Initialize sections visibility
    showActiveSection('overview-section');
    
    // Initialize section navigation
    setupSectionNavigation();
    
    // Setup child selection
    setupChildSelection();
    
    // Initialize sliders
    initializeSliders();
    
    // Initialize charts if visible
    initializeCharts();
    
    // Setup drag-and-drop for story queue
    setupStoryQueueDragDrop();
    
    // Initialize toggle behaviors
    setupToggles();
    
    // Initialize form handlers
    setupFormHandlers();
    
    // Load data based on selected child
    loadChildData();
}

/**
 * Show active section and hide others
 */
function showActiveSection(sectionId) {
    // Hide all sections
    document.querySelectorAll('.dashboard-section').forEach(section => {
        section.style.display = 'none';
    });
    
    // Show the selected section
    const activeSection = document.getElementById(sectionId);
    if (activeSection) {
        activeSection.style.display = 'block';
    }
}

/**
 * Setup navigation between dashboard sections
 */
function setupSectionNavigation() {
    // Create section navigation tabs
    const dashboardContent = document.querySelector('.dashboard-content');
    const sectionNav = document.createElement('div');
    sectionNav.className = 'section-navigation';
    
    const sections = [
        { id: 'overview-section', title: '✅ Dashboard Overview', active: true },
        { id: 'control-center-section', title: '🔒 Control Center' },
        { id: 'customization-section', title: '🛠️ Customization Tools' },
        { id: 'learning-goals-section', title: '🧠 Learning Goals' },
        { id: 'report-cards-section', title: '🧾 Report Cards' },
        { id: 'security-section', title: '🔐 Security & Setup' }
    ];
    
    // Create tabs
    sections.forEach(section => {
        const tab = document.createElement('button');
        tab.className = `section-tab ${section.active ? 'active' : ''}`;
        tab.setAttribute('data-section', section.id);
        tab.textContent = section.title;
        
        tab.addEventListener('click', function() {
            // Update active tab
            document.querySelectorAll('.section-tab').forEach(t => {
                t.classList.remove('active');
            });
            tab.classList.add('active');
            
            // Show section
            showActiveSection(section.id);
            
            // Initialize charts if showing overview section
            if (section.id === 'overview-section') {
                initializeCharts();
            }
        });
        
        sectionNav.appendChild(tab);
    });
    
    // Insert navigation after child account selection
    const childAccountCard = document.querySelector('.child-accounts-card');
    dashboardContent.insertBefore(sectionNav, childAccountCard.nextSibling);
    
    // Add CSS for section navigation
    const style = document.createElement('style');
    style.textContent = `
        .section-navigation {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 20px;
            background-color: rgba(255, 255, 255, 0.7);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.05);
        }
        
        .section-tab {
            padding: 10px 15px;
            background-color: #f5f8ff;
            border: 1px solid #b0c4e8;
            border-radius: 8px;
            color: #5b87c7;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        
        .section-tab:hover {
            background-color: #e0e8ff;
        }
        
        .section-tab.active {
            background-color: #5b87c7;
            color: white;
            border-color: #4a6fa5;
        }
        
        @media (max-width: 768px) {
            .section-navigation {
                flex-direction: column;
                gap: 5px;
            }
            
            .section-tab {
                text-align: left;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Handle Weekly Report link in header
    document.getElementById('report-card-link').addEventListener('click', function(e) {
        e.preventDefault();
        
        // Update active tab
        document.querySelectorAll('.section-tab').forEach(t => {
            t.classList.remove('active');
            if (t.getAttribute('data-section') === 'report-cards-section') {
                t.classList.add('active');
            }
        });
        
        // Show report cards section
        showActiveSection('report-cards-section');
    });
}

/**
 * Setup child selection functionality
 */
function setupChildSelection() {
    // Handle child selection
    const childCards = document.querySelectorAll('.child-card');
    
    childCards.forEach(card => {
        card.addEventListener('click', function() {
            // Remove active class from all cards
            childCards.forEach(c => c.classList.remove('active-child'));
            
            // Add active class to selected card
            card.classList.add('active-child');
            
            // Get child ID
            const childId = card.getAttribute('data-child-id');
            
            // Set as active child
            setActiveChild(childId);
            
            // Load child data
            loadChildData(childId);
        });
        
        // Add CSS for active child card
        const style = document.createElement('style');
        style.textContent = `
            .child-card.active-child {
                border: 2px solid #5b87c7;
                background-color: #edf2ff;
            }
        `;
        document.head.appendChild(style);
    });
    
    // Handle view activity button
    const viewActivityButtons = document.querySelectorAll('.view-activity-btn');
    viewActivityButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent triggering the card click
            
            const childId = button.getAttribute('data-child-id');
            setActiveChild(childId);
            
            // Show overview section
            document.querySelectorAll('.section-tab').forEach(t => {
                t.classList.remove('active');
                if (t.getAttribute('data-section') === 'overview-section') {
                    t.classList.add('active');
                }
            });
            
            showActiveSection('overview-section');
            loadChildData(childId);
        });
    });
    
    // Handle edit profile button
    const editProfileButtons = document.querySelectorAll('.edit-profile-btn');
    editProfileButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Prevent triggering the card click
            
            // This would show a modal for editing child profile
            alert('Edit profile functionality will be implemented in a future update.');
        });
    });
    
    // Select first child by default if any exist
    if (childCards.length > 0) {
        childCards[0].classList.add('active-child');
        const childId = childCards[0].getAttribute('data-child-id');
        setActiveChild(childId);
    }
}

/**
 * Set active child in local storage
 */
function setActiveChild(childId) {
    localStorage.setItem('activeChildId', childId);
    
    // Update UI to show active child
    document.querySelectorAll(`.child-card`).forEach(card => {
        if (card.getAttribute('data-child-id') === childId) {
            card.classList.add('active-child');
        } else {
            card.classList.remove('active-child');
        }
    });
    
    // Update child name in report card
    const childName = document.querySelector(`.child-card[data-child-id="${childId}"] .child-info h3`).textContent;
    document.getElementById('report-child-name').textContent = childName;
}

/**
 * Load child data based on selected child
 */
function loadChildData(childId) {
    if (!childId) {
        childId = localStorage.getItem('activeChildId');
    }
    
    if (!childId) {
        // No child selected
        return;
    }
    
    // In a real implementation, this would fetch data from the server
    // For now, we'll just update with dummy data
    
    // Update activity summary
    document.getElementById('stories-read').textContent = Math.floor(Math.random() * 10);
    document.getElementById('games-played').textContent = Math.floor(Math.random() * 15);
    document.getElementById('stars-earned').textContent = Math.floor(Math.random() * 50);
    document.getElementById('badges-earned').textContent = Math.floor(Math.random() * 8);
    
    // Update report card data
    document.getElementById('report-stories-read').textContent = document.getElementById('stories-read').textContent;
    document.getElementById('report-time-spent').textContent = Math.floor(Math.random() * 120 + 30);
    document.getElementById('report-games-played').textContent = document.getElementById('games-played').textContent;
    document.getElementById('report-stars-earned').textContent = document.getElementById('stars-earned').textContent;
    
    // Initialize or refresh charts
    initializeCharts();
}

/**
 * Initialize slider behaviors
 */
function initializeSliders() {
    // Daily time limit slider
    const dailyTimeLimit = document.getElementById('daily-time-limit');
    const dailyTimeValue = document.getElementById('daily-time-value');
    
    if (dailyTimeLimit && dailyTimeValue) {
        dailyTimeLimit.addEventListener('input', function() {
            dailyTimeValue.textContent = `${dailyTimeLimit.value} mins`;
        });
    }
    
    // Weekly time limit slider
    const weeklyTimeLimit = document.getElementById('weekly-time-limit');
    const weeklyTimeValue = document.getElementById('weekly-time-value');
    
    if (weeklyTimeLimit && weeklyTimeValue) {
        weeklyTimeLimit.addEventListener('input', function() {
            const hours = Math.floor(weeklyTimeLimit.value / 60);
            const mins = weeklyTimeLimit.value % 60;
            
            if (hours === 0) {
                weeklyTimeValue.textContent = `${mins} mins`;
            } else if (mins === 0) {
                weeklyTimeValue.textContent = `${hours} hours`;
            } else {
                weeklyTimeValue.textContent = `${hours}h ${mins}m`;
            }
        });
    }
    
    // Reading speed slider
    const readingSpeed = document.getElementById('reading-speed');
    const readingSpeedValue = document.getElementById('reading-speed-value');
    
    if (readingSpeed && readingSpeedValue) {
        readingSpeed.addEventListener('input', function() {
            const speed = parseFloat(readingSpeed.value);
            
            if (speed < 0.9) {
                readingSpeedValue.textContent = `Slow (${speed.toFixed(1)}x)`;
            } else if (speed > 1.1) {
                readingSpeedValue.textContent = `Fast (${speed.toFixed(1)}x)`;
            } else {
                readingSpeedValue.textContent = `Normal (${speed.toFixed(1)}x)`;
            }
        });
    }
    
    // Sound effects volume slider
    const soundEffectsVolume = document.getElementById('sound-effects-volume');
    const soundEffectsVolumeValue = document.getElementById('sound-effects-volume-value');
    
    if (soundEffectsVolume && soundEffectsVolumeValue) {
        soundEffectsVolume.addEventListener('input', function() {
            soundEffectsVolumeValue.textContent = `${soundEffectsVolume.value}%`;
        });
    }
}

/**
 * Initialize charts for activity tracking
 */
function initializeCharts() {
    // Weekly activity chart
    const weeklyActivityCtx = document.getElementById('weekly-activity-chart');
    if (weeklyActivityCtx) {
        // Check if chart already exists and destroy it
        if (weeklyActivityCtx.chart) {
            weeklyActivityCtx.chart.destroy();
        }
        
        // Generate random data
        const storyData = Array.from({length: 7}, () => Math.floor(Math.random() * 3));
        const gameData = Array.from({length: 7}, () => Math.floor(Math.random() * 4));
        
        // Create new chart
        weeklyActivityCtx.chart = new Chart(weeklyActivityCtx, {
            type: 'bar',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [
                    {
                        label: 'Stories',
                        data: storyData,
                        backgroundColor: 'rgba(91, 135, 199, 0.6)',
                        borderColor: 'rgba(91, 135, 199, 1)',
                        borderWidth: 1
                    },
                    {
                        label: 'Games',
                        data: gameData,
                        backgroundColor: 'rgba(255, 159, 64, 0.6)',
                        borderColor: 'rgba(255, 159, 64, 1)',
                        borderWidth: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            stepSize: 1
                        }
                    }
                }
            }
        });
    }
    
    // Skills radar chart
    const skillsRadarCtx = document.getElementById('skills-radar-chart');
    if (skillsRadarCtx) {
        // Check if chart already exists and destroy it
        if (skillsRadarCtx.chart) {
            skillsRadarCtx.chart.destroy();
        }
        
        // Generate random data
        const skillsData = Array.from({length: 5}, () => Math.floor(Math.random() * 70 + 30));
        
        // Create new chart
        skillsRadarCtx.chart = new Chart(skillsRadarCtx, {
            type: 'radar',
            data: {
                labels: [
                    'Reading',
                    'Counting',
                    'Problem Solving',
                    'Memory',
                    'Creativity'
                ],
                datasets: [{
                    label: 'Skill Level',
                    data: skillsData,
                    fill: true,
                    backgroundColor: 'rgba(91, 135, 199, 0.2)',
                    borderColor: 'rgba(91, 135, 199, 1)',
                    pointBackgroundColor: 'rgba(91, 135, 199, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(91, 135, 199, 1)'
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    r: {
                        angleLines: {
                            display: true
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                }
            }
        });
    }
}

/**
 * Setup drag and drop for story queue
 */
function setupStoryQueueDragDrop() {
    const storyItems = document.querySelectorAll('.story-item');
    const storyList = document.getElementById('available-stories-list');
    const storyQueue = document.getElementById('story-queue-list');
    
    if (storyItems && storyList && storyQueue) {
        storyItems.forEach(item => {
            item.addEventListener('dragstart', function(e) {
                e.dataTransfer.setData('text/plain', item.getAttribute('data-story-id'));
                setTimeout(() => {
                    item.classList.add('dragging');
                }, 0);
            });
            
            item.addEventListener('dragend', function() {
                item.classList.remove('dragging');
            });
        });
        
        // Handle drops in the queue
        storyQueue.addEventListener('dragover', function(e) {
            e.preventDefault();
            storyQueue.classList.add('drag-over');
        });
        
        storyQueue.addEventListener('dragleave', function() {
            storyQueue.classList.remove('drag-over');
        });
        
        storyQueue.addEventListener('drop', function(e) {
            e.preventDefault();
            storyQueue.classList.remove('drag-over');
            
            // Get the story ID
            const storyId = e.dataTransfer.getData('text/plain');
            
            // Find the original story item
            const originalItem = document.querySelector(`.story-item[data-story-id="${storyId}"]`);
            
            // Check if this story is already in the queue
            const existingQueueItem = storyQueue.querySelector(`.story-item[data-story-id="${storyId}"]`);
            
            if (!existingQueueItem && originalItem) {
                // Clone the item
                const newItem = originalItem.cloneNode(true);
                
                // Add remove button
                const removeBtn = document.createElement('span');
                removeBtn.className = 'remove-queue-item';
                removeBtn.innerHTML = '&times;';
                removeBtn.addEventListener('click', function() {
                    newItem.remove();
                    updateEmptyQueueMessage();
                });
                
                newItem.appendChild(removeBtn);
                
                // Hide empty message if it exists
                const emptyMessage = storyQueue.querySelector('.empty-queue-message');
                if (emptyMessage) {
                    emptyMessage.style.display = 'none';
                }
                
                // Add to queue
                storyQueue.appendChild(newItem);
            }
        });
        
        // Add CSS for drag and drop
        const style = document.createElement('style');
        style.textContent = `
            .story-item.dragging {
                opacity: 0.5;
            }
            
            .story-queue.drag-over {
                background-color: #edf2ff;
                border: 2px dashed #5b87c7;
            }
            
            .remove-queue-item {
                float: right;
                color: #dc3545;
                font-weight: bold;
                cursor: pointer;
                padding: 0 5px;
            }
        `;
        document.head.appendChild(style);
        
        // Function to update empty queue message
        function updateEmptyQueueMessage() {
            const queueItems = storyQueue.querySelectorAll('.story-item');
            const emptyMessage = storyQueue.querySelector('.empty-queue-message');
            
            if (queueItems.length === 0 && emptyMessage) {
                emptyMessage.style.display = 'block';
            }
        }
    }
}

/**
 * Setup toggle behaviors
 */
function setupToggles() {
    // Goal type selector
    const goalType = document.getElementById('goal-type');
    const goalDescriptor = document.getElementById('goal-descriptor');
    const customGoalInput = document.querySelector('.custom-goal-input');
    
    if (goalType && goalDescriptor && customGoalInput) {
        goalType.addEventListener('change', function() {
            if (goalType.value === 'custom') {
                goalDescriptor.style.display = 'none';
                customGoalInput.style.display = 'flex';
            } else {
                // Update descriptors based on selected goal type
                updateGoalDescriptors(goalType.value);
                goalDescriptor.style.display = 'block';
                customGoalInput.style.display = 'none';
            }
        });
    }
    
    // Function to update goal descriptors based on goal type
    function updateGoalDescriptors(goalType) {
        const descriptorSelect = document.getElementById('goal-descriptor');
        
        if (descriptorSelect) {
            // Clear existing options
            descriptorSelect.innerHTML = '';
            
            // Add appropriate options based on goal type
            if (goalType === 'story') {
                addOption(descriptorSelect, 'any', 'Any Stories');
                addOption(descriptorSelect, 'new', 'New Stories');
                addOption(descriptorSelect, 'friendship', 'Friendship Stories');
                addOption(descriptorSelect, 'educational', 'Educational Stories');
            } else if (goalType === 'game') {
                addOption(descriptorSelect, 'any', 'Any Games');
                addOption(descriptorSelect, 'counting', 'Counting Games');
                addOption(descriptorSelect, 'matching', 'Matching Games');
                addOption(descriptorSelect, 'memory', 'Memory Games');
            } else if (goalType === 'badge') {
                addOption(descriptorSelect, 'any', 'Any Badges');
                addOption(descriptorSelect, 'story', 'Story Badges');
                addOption(descriptorSelect, 'game', 'Game Badges');
                addOption(descriptorSelect, 'achievement', 'Achievement Badges');
            }
        }
        
        function addOption(select, value, text) {
            const option = document.createElement('option');
            option.value = value;
            option.textContent = text;
            select.appendChild(option);
        }
    }
}

/**
 * Setup form handlers
 */
function setupFormHandlers() {
    // Add goal form
    const addGoalBtn = document.querySelector('.add-goal-btn');
    const addCustomGoalBtn = document.querySelector('.add-custom-goal-btn');
    const goalsList = document.getElementById('current-goals-list');
    
    if (addGoalBtn && goalsList) {
        addGoalBtn.addEventListener('click', function() {
            const goalType = document.getElementById('goal-type').value;
            const goalQuantity = document.getElementById('goal-quantity').value;
            const goalDescriptor = document.getElementById('goal-descriptor').value;
            
            // Create goal text
            let goalText = '';
            
            if (goalType === 'story') {
                goalText = `Read ${goalQuantity} ${goalDescriptor} stories`;
            } else if (goalType === 'game') {
                goalText = `Play ${goalQuantity} ${goalDescriptor} games`;
            } else if (goalType === 'badge') {
                goalText = `Earn ${goalQuantity} ${goalDescriptor} badges`;
            }
            
            addGoalItem(goalText, goalQuantity);
        });
    }
    
    if (addCustomGoalBtn && goalsList) {
        addCustomGoalBtn.addEventListener('click', function() {
            const customGoalText = document.getElementById('custom-goal-text').value;
            
            if (customGoalText.trim() !== '') {
                addGoalItem(customGoalText, 1);
                document.getElementById('custom-goal-text').value = '';
            }
        });
    }
    
    // Function to add a goal item to the list
    function addGoalItem(goalText, quantity) {
        // Create goal item
        const goalItem = document.createElement('div');
        goalItem.className = 'goal-item';
        
        // Generate random ID for checkboxes
        const goalId = 'goal-' + Math.floor(Math.random() * 1000);
        
        goalItem.innerHTML = `
            <div class="goal-checkbox">
                <input type="checkbox" id="${goalId}" disabled>
                <label for="${goalId}"></label>
            </div>
            <div class="goal-content">
                <span class="goal-text">${goalText}</span>
                <span class="goal-progress">0/${quantity} completed</span>
            </div>
            <button class="remove-goal-btn">×</button>
        `;
        
        // Add remove functionality
        goalItem.querySelector('.remove-goal-btn').addEventListener('click', function() {
            goalItem.remove();
        });
        
        // Add to goals list
        goalsList.appendChild(goalItem);
    }
    
    // Save buttons
    const saveButtons = document.querySelectorAll(
        '.save-time-limits-btn, ' +
        '.save-content-controls-btn, ' +
        '.save-story-queue-btn, ' +
        '.save-voice-settings-btn, ' +
        '.save-rewards-settings-btn, ' +
        '.save-notifications-btn, ' +
        '.save-security-settings-btn'
    );
    
    saveButtons.forEach(button => {
        button.addEventListener('click', function() {
            // Show saving indicator
            const originalText = button.textContent;
            button.textContent = 'Saving...';
            button.disabled = true;
            
            // Simulate saving
            setTimeout(() => {
                button.textContent = 'Saved!';
                
                setTimeout(() => {
                    button.textContent = originalText;
                    button.disabled = false;
                }, 1000);
            }, 1500);
        });
    });
    
    // QR Code generation
    const generateQrBtn = document.querySelector('.generate-qr-btn');
    
    if (generateQrBtn) {
        generateQrBtn.addEventListener('click', function() {
            const qrPlaceholder = document.querySelector('.qr-placeholder');
            
            if (qrPlaceholder) {
                qrPlaceholder.innerHTML = '<img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=ChildrensCastlePairingCode" alt="QR Code">';
            }
        });
    }
    
    // Refresh pairing code
    const refreshCodeBtn = document.querySelector('.refresh-code-btn');
    
    if (refreshCodeBtn) {
        refreshCodeBtn.addEventListener('click', function() {
            const codeDisplay = document.getElementById('pairing-code-display');
            
            if (codeDisplay) {
                // Generate random code
                const letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ';
                const numbers = '23456789';
                
                let code = '';
                
                for (let i = 0; i < 4; i++) {
                    code += letters.charAt(Math.floor(Math.random() * letters.length));
                }
                
                code += '-';
                
                for (let i = 0; i < 4; i++) {
                    code += numbers.charAt(Math.floor(Math.random() * numbers.length));
                }
                
                codeDisplay.textContent = code;
            }
        });
    }
    
    // Download report button
    const downloadReportBtn = document.querySelector('.download-report-btn');
    
    if (downloadReportBtn) {
        downloadReportBtn.addEventListener('click', function() {
            alert('Report download functionality will be implemented in a future update.');
        });
    }
    
    // Sync now button
    const syncNowBtn = document.querySelector('.sync-now-btn');
    
    if (syncNowBtn) {
        syncNowBtn.addEventListener('click', function() {
            const originalText = syncNowBtn.textContent;
            syncNowBtn.textContent = 'Syncing...';
            syncNowBtn.disabled = true;
            
            // Simulate syncing
            setTimeout(() => {
                syncNowBtn.textContent = 'Synced!';
                
                setTimeout(() => {
                    syncNowBtn.textContent = originalText;
                    syncNowBtn.disabled = false;
                }, 1000);
            }, 2000);
        });
    }
}

// Story content data structure
const stories = {
    little_fox: {
        title: "The Little Fox",
        text: "Once upon a time, there was a clever little fox with a bright orange coat. He lived in a cozy den at the edge of the forest. Every day, the little fox would explore the woods, making friends with rabbits, squirrels, and birds. One day, the little fox found a lost baby bird who had fallen from its nest. The kind fox carefully picked up the bird and helped it find its way home. The mother bird was so thankful that she sang the most beautiful song just for the little fox. From that day on, whenever the fox felt lonely, he would visit his bird friends who would sing cheerful songs to brighten his day.",
        image: "little_fox.svg",
        audio: "little_fox.mp3"
    },
    three_little_pigs: {
        title: "Three Little Pigs",
        text: "Once upon a time, there were three little pigs who decided to build their own houses. The first pig built a house of straw because it was quick and easy. The second pig built a house of sticks. The third pig worked hard to build a strong house of bricks. One day, a big bad wolf came along. He huffed and puffed and blew down the house of straw! The first pig ran to the second pig's house. The wolf huffed and puffed and blew down the house of sticks too! Both pigs ran to the third pig's brick house. The wolf huffed and puffed, but he could not blow down the strong brick house. The wolf tried to come down the chimney, but the pigs had a pot of hot soup waiting! The wolf ran away, and the three little pigs lived happily ever after in the brick house.",
        image: "three_little_pigs.svg",
        audio: "three_little_pigs.mp3"
    },
    brown_bear: {
        title: "Brown Bear",
        text: "Brown Bear, Brown Bear, what do you see? I see a red bird looking at me. Red Bird, Red Bird, what do you see? I see a yellow duck looking at me. Yellow Duck, Yellow Duck, what do you see? I see a blue horse looking at me. Blue Horse, Blue Horse, what do you see? I see a green frog looking at me. Green Frog, Green Frog, what do you see? I see a purple cat looking at me. Purple Cat, Purple Cat, what do you see? I see a white dog looking at me. White Dog, White Dog, what do you see? I see a black sheep looking at me. Black Sheep, Black Sheep, what do you see? I see a goldfish looking at me. Goldfish, Goldfish, what do you see? I see children looking at me!",
        image: "brown_bear.svg",
        audio: "brown_bear.mp3"
    },
    wild_things: {
        title: "Where the Wild Things Are",
        text: "Once there was a boy named Max who wore his wolf suit and made mischief of one kind and another. His mother called him 'WILD THING!' and Max said 'I'LL EAT YOU UP!' so he was sent to bed without eating anything. That very night in Max's room a forest grew and grew until his ceiling hung with vines and the walls became the world all around. And an ocean tumbled by with a private boat for Max, and he sailed off through night and day and in and out of weeks and almost over a year to where the wild things are. When he came to the place where the wild things are, they roared their terrible roars and gnashed their terrible teeth and rolled their terrible eyes and showed their terrible claws till Max said 'BE STILL!' and tamed them with the magic trick of staring into all their yellow eyes without blinking once. And they were frightened and called him the most wild thing of all and made him king of all wild things.",
        image: "wild_things.svg",
        audio: "wild_things.mp3"
    },
    black_sheep: {
        title: "Baa Baa Black Sheep",
        text: "Baa, baa, black sheep,\nHave you any wool?\nYes sir, yes sir,\nThree bags full.\n\nOne for the master,\nOne for the dame,\nAnd one for the little boy\nWho lives down the lane.\n\nBaa, baa, black sheep,\nHave you any wool?\nYes sir, yes sir,\nThree bags full.",
        image: "black_sheep.svg",
        audio: "black_sheep.mp3"
    },
    hickory_dickory: {
        title: "Hickory Dickory Dock",
        text: "Hickory dickory dock,\nThe mouse ran up the clock.\nThe clock struck one,\nThe mouse ran down,\nHickory dickory dock.\n\nHickory dickory dock,\nThe mouse ran up the clock.\nThe clock struck two,\nAnd down he flew,\nHickory dickory dock.\n\nHickory dickory dock,\nThe mouse ran up the clock.\nThe clock struck three,\nAnd he did flee,\nHickory dickory dock.",
        image: "hickory_dickory.svg",
        audio: "hickory_dickory.mp3"
    },
    bo_peep: {
        title: "Little Bo-Peep",
        text: "Little Bo-Peep has lost her sheep,\nAnd can't tell where to find them;\nLeave them alone, and they'll come home,\nBringing their tails behind them.\n\nLittle Bo-Peep fell fast asleep,\nAnd dreamt she heard them bleating;\nBut when she awoke, she found it a joke,\nFor they were still all fleeting.\n\nThen up she took her little crook,\nDetermined for to find them;\nShe found them indeed, but it made her heart bleed,\nFor they'd left their tails behind them.",
        image: "bo_peep.svg",
        audio: "bo_peep.mp3"
    },
    jack_jill: {
        title: "Jack and Jill",
        text: "Jack and Jill went up the hill\nTo fetch a pail of water.\nJack fell down and broke his crown,\nAnd Jill came tumbling after.\n\nUp Jack got, and home did trot,\nAs fast as he could caper,\nTo old Dame Dob, who patched his nob\nWith vinegar and brown paper.\n\nWhen Jill came in, how she did grin\nTo see Jack's paper plaster;\nMother vexed, did whip her next,\nFor laughing at Jack's disaster.",
        image: "jack_jill.svg",
        audio: "jack_jill.mp3"
    }
};

// DOM elements
document.addEventListener('DOMContentLoaded', function() {
    // Sections
    const sections = {
        modeSelection: document.getElementById('mode-selection'),
        storyMode: document.getElementById('story-mode'),
        gameMode: document.getElementById('game-mode'),
        badgesSection: document.getElementById('badges-section')
    };
    
    // Buttons
    const buttons = {
        storyModeBtn: document.getElementById('story-mode-btn'),
        gameModeBtn: document.getElementById('game-mode-btn'),
        rewardsBtn: document.getElementById('rewards-btn'),
        backToModesBtn: document.getElementById('back-to-modes-btn'),
        backToModesFromGameBtn: document.getElementById('back-to-modes-from-game-btn'),
        backToModesFromBadgesBtn: document.getElementById('back-to-modes-from-badges-btn'),
        playStoryBtn: document.getElementById('play-story-btn'),
        doneReadingBtn: document.getElementById('done-reading-btn')
    };
    
    // Story elements
    const storyElements = {
        storySelect: document.getElementById('story-select'),
        storyTitle: document.getElementById('story-title'),
        storyText: document.getElementById('story-text'),
        storyImage: document.getElementById('story-image'),
        storyAudio: document.getElementById('story-audio'),
        audioSource: document.getElementById('audio-source')
    };
    
    // Navigation between sections
    buttons.storyModeBtn?.addEventListener('click', () => showSection('story-mode'));
    buttons.gameModeBtn?.addEventListener('click', () => showSection('game-mode'));
    buttons.rewardsBtn?.addEventListener('click', () => showSection('badges-section'));
    buttons.backToModesBtn?.addEventListener('click', () => showSection('mode-selection'));
    buttons.backToModesFromGameBtn?.addEventListener('click', () => showSection('mode-selection'));
    buttons.backToModesFromBadgesBtn?.addEventListener('click', () => showSection('mode-selection'));
    
    // Story selection change
    storyElements.storySelect?.addEventListener('change', function() {
        updateStory(this.value);
    });
    
    // Play story button
    buttons.playStoryBtn?.addEventListener('click', () => playCurrentStory());
    
    // Done reading button
    buttons.doneReadingBtn?.addEventListener('click', () => completeStory());
    
    // Initialize with the first story
    if (storyElements.storySelect) {
        updateStory(storyElements.storySelect.value || 'little_fox');
    }
    
    // Functions
    window.showSection = function(sectionId) {
        // Hide all sections
        for (const key in sections) {
            if (sections[key]) {
                sections[key].classList.remove('active');
            }
        }
        
        // Show selected section
        const section = document.getElementById(sectionId);
        if (section) {
            section.classList.add('active');
        }
        
        // Pause any playing audio when changing sections
        if (storyElements.storyAudio) {
            storyElements.storyAudio.pause();
        }
    };
    
    function updateStory(storyId) {
        const story = stories[storyId];
        
        if (!story) {
            console.error('Story not found:', storyId);
            return;
        }
        
        // Update story content
        storyElements.storyTitle.textContent = story.title;
        storyElements.storyText.textContent = story.text;
        
        // Update image path
        const imagePath = `/static/images/${story.image}`;
        storyElements.storyImage.src = imagePath;
        storyElements.storyImage.alt = story.title;
        
        // Update audio path but don't autoplay
        const audioPath = `/static/audio/${story.audio}`;
        storyElements.audioSource.src = audioPath;
        storyElements.storyAudio.load(); // Reload the audio element with the new source
    }
    
    function playCurrentStory() {
        // Reset audio to beginning
        storyElements.storyAudio.currentTime = 0;
        
        // Play audio
        storyElements.storyAudio.play().catch(error => {
            console.error('Error playing audio:', error);
            alert('Sorry, there was a problem playing the story audio. Please try again.');
        });
    }
});

// Add touch event listeners for mobile interaction
document.addEventListener('DOMContentLoaded', function() {
    // Make buttons more responsive on touch devices
    const allButtons = document.querySelectorAll('button');
    
    allButtons.forEach(button => {
        button.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
        });
        
        button.addEventListener('touchend', function() {
            this.style.transform = '';
        });
    });
});

// Story completion function
function completeStory() {
    // Get current story ID
    const storySelect = document.getElementById('story-select');
    if (storySelect) {
        const storyId = storySelect.value;
        // Award badge through rewards system
        if (typeof awardStoryCompletionBadge === 'function') {
            awardStoryCompletionBadge(storyId);
        }
    }
}

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
    const modeSelectionSection = document.getElementById('mode-selection');
    const storyModeSection = document.getElementById('story-mode');
    const gameModeSection = document.getElementById('game-mode');
    
    // Buttons
    const storyModeBtn = document.getElementById('story-mode-btn');
    const gameModeBtn = document.getElementById('game-mode-btn');
    const backToModesBtn = document.getElementById('back-to-modes-btn');
    const backToModesFromGameBtn = document.getElementById('back-to-modes-from-game-btn');
    const playStoryBtn = document.getElementById('play-story-btn');
    
    // Story elements
    const storyDropdown = document.getElementById('story-dropdown');
    const storyTitle = document.getElementById('story-title');
    const storyText = document.getElementById('story-text');
    const storyImage = document.getElementById('story-image');
    const storyAudio = document.getElementById('story-audio');
    const audioSource = document.getElementById('audio-source');
    
    // Navigation between sections
    storyModeBtn.addEventListener('click', function() {
        showSection(storyModeSection);
    });
    
    gameModeBtn.addEventListener('click', function() {
        showSection(gameModeSection);
    });
    
    backToModesBtn.addEventListener('click', function() {
        showSection(modeSelectionSection);
    });
    
    backToModesFromGameBtn.addEventListener('click', function() {
        showSection(modeSelectionSection);
    });
    
    // Story selection change
    storyDropdown.addEventListener('change', function() {
        updateStory(this.value);
    });
    
    // Play story button
    playStoryBtn.addEventListener('click', function() {
        playCurrentStory();
    });
    
    // Initialize with the first story
    updateStory('little_fox');
    
    // Functions
    function showSection(section) {
        // Hide all sections
        modeSelectionSection.classList.remove('active');
        storyModeSection.classList.remove('active');
        gameModeSection.classList.remove('active');
        
        // Show selected section
        section.classList.add('active');
        
        // Pause any playing audio when changing sections
        storyAudio.pause();
    }
    
    function updateStory(storyId) {
        const story = stories[storyId];
        
        if (!story) {
            console.error('Story not found:', storyId);
            return;
        }
        
        // Update story content
        storyTitle.textContent = story.title;
        storyText.textContent = story.text;
        
        // Update image path
        const imagePath = `/static/images/${story.image}`;
        storyImage.src = imagePath;
        storyImage.alt = story.title;
        
        // Update audio path but don't autoplay
        const audioPath = `/static/audio/${story.audio}`;
        audioSource.src = audioPath;
        storyAudio.load(); // Reload the audio element with the new source
    }
    
    function playCurrentStory() {
        // Reset audio to beginning
        storyAudio.currentTime = 0;
        
        // Play audio
        storyAudio.play().catch(error => {
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

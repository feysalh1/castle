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
    },
    goldilocks: {
        title: "Goldilocks and the Three Bears",
        text: "Once upon a time, there were three bears who lived in a house in the forest. There was a big Papa Bear, a middle-sized Mama Bear, and a tiny Baby Bear. One morning, the three bears made porridge for breakfast, but it was too hot to eat. So they decided to go for a walk while their porridge cooled.\n\nWhile they were out, a little girl named Goldilocks was walking through the forest. She saw the bears' house and knocked on the door. When no one answered, she went inside.\n\nIn the kitchen, Goldilocks saw three bowls of porridge. She tasted the porridge in the big bowl. \"This porridge is too hot!\" she said. She tasted the porridge in the middle-sized bowl. \"This porridge is too cold!\" she said. Then she tasted the porridge in the tiny bowl. \"This porridge is just right!\" she said. And she ate it all up.\n\nNext, Goldilocks went into the living room. She sat in the big chair. \"This chair is too hard!\" she said. She sat in the middle-sized chair. \"This chair is too soft!\" she said. She sat in the tiny chair. \"This chair is just right!\" she said. But the tiny chair broke!\n\nGoldilocks was tired, so she went upstairs to the bedroom. She lay on the big bed. \"This bed is too high!\" she said. She lay on the middle-sized bed. \"This bed is too low!\" she said. She lay on the tiny bed. \"This bed is just right!\" she said. And she fell fast asleep.\n\nSoon, the three bears came home. \"Someone's been eating my porridge!\" growled Papa Bear. \"Someone's been eating my porridge!\" said Mama Bear. \"Someone's been eating my porridge, and it's all gone!\" cried Baby Bear.\n\n\"Someone's been sitting in my chair!\" growled Papa Bear. \"Someone's been sitting in my chair!\" said Mama Bear. \"Someone's been sitting in my chair, and it's broken!\" cried Baby Bear.\n\nThe three bears went upstairs. \"Someone's been sleeping in my bed!\" growled Papa Bear. \"Someone's been sleeping in my bed!\" said Mama Bear. \"Someone's been sleeping in my bed, and she's still here!\" cried Baby Bear.\n\nJust then, Goldilocks woke up. When she saw the three bears, she jumped out of bed, ran down the stairs, and out of the house. She never returned to the bears' house again. And the three bears never left their porridge unattended again.",
        image: "goldilocks.svg",
        audio: "goldilocks.mp3"
    },
    hungry_caterpillar: {
        title: "The Hungry Caterpillar",
        text: "In the light of the moon, a little egg lay on a leaf. One Sunday morning, the warm sun came up and - pop! - out of the egg came a tiny and very hungry caterpillar.\n\nHe started to look for some food. On Monday, he ate through one apple, but he was still hungry. On Tuesday, he ate through two pears, but he was still hungry. On Wednesday, he ate through three plums, but he was still hungry. On Thursday, he ate through four strawberries, but he was still hungry. On Friday, he ate through five oranges, but he was still hungry.\n\nOn Saturday, he ate through one piece of chocolate cake, one ice cream cone, one pickle, one slice of Swiss cheese, one slice of salami, one lollipop, one piece of cherry pie, one sausage, one cupcake, and one slice of watermelon. That night, he had a stomachache!\n\nThe next day was Sunday again. The caterpillar ate through one nice green leaf, and after that, he felt much better. Now he wasn't hungry anymore, and he wasn't a little caterpillar anymore. He was a big fat caterpillar.\n\nHe built a small house, called a cocoon, around himself. He stayed inside for more than two weeks. Then he nibbled a hole in the cocoon, pushed his way out, and... he had become a beautiful butterfly!",
        image: "hungry_caterpillar.svg",
        audio: "hungry_caterpillar.mp3"
    },
    five_monkeys: {
        title: "Five Little Monkeys",
        text: "Five little monkeys jumping on the bed.\nOne fell off and bumped his head.\nMama called the doctor and the doctor said,\n\"No more monkeys jumping on the bed!\"\n\nFour little monkeys jumping on the bed.\nOne fell off and bumped her head.\nMama called the doctor and the doctor said,\n\"No more monkeys jumping on the bed!\"\n\nThree little monkeys jumping on the bed.\nOne fell off and bumped his head.\nMama called the doctor and the doctor said,\n\"No more monkeys jumping on the bed!\"\n\nTwo little monkeys jumping on the bed.\nOne fell off and bumped her head.\nMama called the doctor and the doctor said,\n\"No more monkeys jumping on the bed!\"\n\nOne little monkey jumping on the bed.\nHe fell off and bumped his head.\nMama called the doctor and the doctor said,\n\"Put those monkeys straight to bed!\"",
        image: "five_monkeys.svg",
        audio: "five_monkeys.mp3"
    },
    rainbow_fish: {
        title: "The Rainbow Fish",
        text: "Far out in the sea, where the water is blue like a beautiful cornflower and clear as crystal, lived a fish. But he was no ordinary fish - he was the most beautiful fish in the entire ocean. His scales were every shade of rainbow, and they shimmered and sparkled when he moved.\n\nThe other fish called him Rainbow Fish. \"Come and play with us!\" they would invite. But Rainbow Fish would just glide past them, proud and silent, letting his scales shimmer.\n\nOne day, a little blue fish followed him. \"Rainbow Fish,\" he called, \"please give me one of your shiny scales. They're so beautiful, and you have so many.\"\n\n\"Give you one of my scales? Who do you think you are?\" snapped Rainbow Fish. \"Get away from me!\" Shocked, the little blue fish swam away.\n\nFrom then on, no one would play with Rainbow Fish anymore. They turned away when he swam by. What good were beautiful shiny scales if no one would admire them?\n\nRainbow Fish felt very lonely. So he went to see the wise octopus for advice. \"The waves have told me your story,\" said the octopus. \"You must share your scales with others. You might not be as beautiful, but you will discover how to be happy.\"\n\n\"But my scales are what make me special,\" said Rainbow Fish.\n\n\"You will see...\" whispered the octopus as she disappeared into a dark cloud of ink.\n\nRainbow Fish thought about what the octopus had said. Suddenly, he saw the little blue fish swimming by. \"Little blue fish,\" he called, \"here, take one of my shiny scales.\" Carefully, Rainbow Fish pulled out one of his smallest scales and gave it to the little blue fish.\n\n\"Thank you!\" bubbled the little blue fish, wiggling with delight. He tucked the shiny scale among his blue ones, and swam off.\n\nA moment later, Rainbow Fish was surrounded by other fish. Everyone wanted a shiny scale! And Rainbow Fish shared his scales, one here, one there, until he had only one shiny scale left. And now, when he swam through the ocean, he was surrounded by his new friends. They all played together, and Rainbow Fish was very happy.\n\n\"Come when you are ready,\" called one of his new friends, and for the first time, Rainbow Fish smiled. \"I'm coming,\" he said happily, and he swam off to join his friends.",
        image: "rainbow_fish.svg",
        audio: "rainbow_fish.mp3"
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
        // Show transition animation based on section
        if (window.loadingAnimations) {
            // Determine which mode we're transitioning to
            let mode = 'default';
            if (sectionId === 'story-mode') {
                mode = 'story';
            } else if (sectionId === 'game-mode') {
                mode = 'game';
            }
            
            // Show character transition
            window.loadingAnimations.showTransition(mode);
        }
        
        // Delay section change slightly to allow for animations
        setTimeout(() => {
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
            
            // Play a sound effect for section change
            playClickSound();
        }, 300); // Short delay to allow transition animation to start
    };
    
    function updateStory(storyId) {
        // Show quick loading animation when changing stories
        if (window.loadingAnimations) {
            window.loadingAnimations.showQuickLoading();
        }
        
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
        
        // Fade in the story content
        storyElements.storyText.style.opacity = 0;
        storyElements.storyImage.style.opacity = 0;
        
        // After a short delay, fade the content back in
        setTimeout(() => {
            storyElements.storyText.style.opacity = 1;
            storyElements.storyImage.style.opacity = 1;
            
            // Play a gentle sound effect for story change
            playClickSound();
        }, 500);
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

// Improve click responsiveness
document.addEventListener('DOMContentLoaded', function() {
    // Add click sound effect
    function playClickSound() {
        // Create a quick click sound using Web Audio API
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        const oscillator = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        
        oscillator.type = 'sine';
        oscillator.frequency.value = 800;
        gainNode.gain.value = 0.1;
        
        oscillator.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        oscillator.start();
        oscillator.stop(audioCtx.currentTime + 0.05);
    }
    
    // Add click sound to all buttons
    const allButtons = document.querySelectorAll('button');
    allButtons.forEach(button => {
        button.addEventListener('click', function() {
            playClickSound();
        });
    });
    
    // Improve story selection responsiveness
    const storySelect = document.getElementById('story-select');
    if (storySelect) {
        storySelect.addEventListener('change', function() {
            playClickSound();
            // Force immediate update instead of waiting
            updateStory(this.value);
        });
    }
});

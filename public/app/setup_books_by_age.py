#!/usr/bin/env python3
"""
Setup script to categorize books by age groups and add new books.
This script creates age groups and categorizes existing books,
as well as adding new books for different age groups.
"""

import os
import json
from datetime import datetime
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

# Define age groups with appropriate descriptions
AGE_GROUPS = [
    {
        "name": "Toddlers",
        "min_age": 1,
        "max_age": 3,
        "description": "Simple stories with colorful illustrations and repetitive text for very young children."
    },
    {
        "name": "Preschool",
        "min_age": 3,
        "max_age": 5,
        "description": "Engaging stories with basic vocabulary, vivid illustrations, and themes of friendship and discovery."
    },
    {
        "name": "Early Readers",
        "min_age": 5,
        "max_age": 7,
        "description": "Stories with simple sentences and familiar scenarios to help beginning readers build confidence."
    },
    {
        "name": "Growing Readers",
        "min_age": 7,
        "max_age": 9,
        "description": "More complex plots and vocabulary with chapters, helping children transition to longer books."
    },
    {
        "name": "Confident Readers",
        "min_age": 9,
        "max_age": 11,
        "description": "Chapter books with detailed narratives, complex characters, and themes that encourage critical thinking."
    }
]

# Define existing books categorization
EXISTING_BOOKS = [
    {
        "title": "Brown Bear, Brown Bear, What Do You See?",
        "file_name": "brown_bear.txt",
        "author": "Bill Martin Jr.",
        "description": "A beloved children's classic featuring colorful animals and repetitive text.",
        "age_group": "Toddlers",
        "difficulty_level": "easy",
        "themes": ["animals", "colors", "repetition"],
        "reading_time_minutes": 3
    },
    {
        "title": "The Very Hungry Caterpillar",
        "file_name": "hungry_caterpillar.txt",
        "author": "Eric Carle",
        "description": "A caterpillar eats its way through different foods before becoming a butterfly.",
        "age_group": "Toddlers",
        "difficulty_level": "easy",
        "themes": ["animals", "growth", "nature", "counting", "days of the week"],
        "reading_time_minutes": 5
    },
    {
        "title": "Baa, Baa, Black Sheep",
        "file_name": "black_sheep.txt",
        "author": "Traditional",
        "description": "A classic nursery rhyme about a black sheep with three bags of wool.",
        "age_group": "Toddlers",
        "difficulty_level": "easy",
        "themes": ["animals", "nursery rhymes", "sharing"],
        "reading_time_minutes": 2
    },
    {
        "title": "Little Bo-Peep",
        "file_name": "bo_peep.txt",
        "author": "Traditional",
        "description": "A classic nursery rhyme about a shepherdess who lost her sheep.",
        "age_group": "Toddlers",
        "difficulty_level": "easy",
        "themes": ["animals", "nursery rhymes", "problem solving"],
        "reading_time_minutes": 2
    },
    {
        "title": "Hickory Dickory Dock",
        "file_name": "hickory_dickory.txt",
        "author": "Traditional",
        "description": "A classic nursery rhyme about a mouse running up a clock.",
        "age_group": "Toddlers",
        "difficulty_level": "easy",
        "themes": ["animals", "nursery rhymes", "time"],
        "reading_time_minutes": 2
    },
    {
        "title": "Jack and Jill",
        "file_name": "jack_jill.txt",
        "author": "Traditional",
        "description": "A classic nursery rhyme about two children who went up a hill.",
        "age_group": "Preschool",
        "difficulty_level": "easy",
        "themes": ["nursery rhymes", "friendship", "adventure"],
        "reading_time_minutes": 2
    },
    {
        "title": "Five Little Monkeys",
        "file_name": "five_monkeys.txt",
        "author": "Traditional",
        "description": "Five monkeys jumping on the bed, falling off and bumping their heads.",
        "age_group": "Preschool",
        "difficulty_level": "easy",
        "themes": ["animals", "counting", "humor", "repetition"],
        "reading_time_minutes": 3
    },
    {
        "title": "What Does The Fox Say?",
        "file_name": "little_fox.txt",
        "author": "Ylvis",
        "description": "A fun story based on the popular song about animal sounds.",
        "age_group": "Preschool",
        "difficulty_level": "easy",
        "themes": ["animals", "sounds", "humor", "music"],
        "reading_time_minutes": 3
    },
    {
        "title": "The Three Little Pigs",
        "file_name": "three_little_pigs.txt",
        "author": "Traditional",
        "description": "Three pigs build houses of different materials as a wolf tries to blow them down.",
        "age_group": "Early Readers",
        "difficulty_level": "medium",
        "themes": ["animals", "perseverance", "problem solving", "fairy tales"],
        "reading_time_minutes": 6
    },
    {
        "title": "Where the Wild Things Are",
        "file_name": "wild_things.txt",
        "author": "Maurice Sendak",
        "description": "Max sails to an island of wild creatures where he becomes king.",
        "age_group": "Early Readers",
        "difficulty_level": "medium",
        "themes": ["imagination", "adventure", "emotions", "family"],
        "reading_time_minutes": 5
    },
    {
        "title": "Goldilocks and the Three Bears",
        "file_name": "goldilocks.txt",
        "author": "Traditional",
        "description": "A girl enters the home of three bears and tries their food, chairs, and beds.",
        "age_group": "Early Readers",
        "difficulty_level": "medium",
        "themes": ["animals", "fairy tales", "choices", "respect"],
        "reading_time_minutes": 7
    },
    {
        "title": "The Rainbow Fish",
        "file_name": "rainbow_fish.txt",
        "author": "Marcus Pfister",
        "description": "A fish learns the importance of sharing his beautiful scales with others.",
        "age_group": "Growing Readers",
        "difficulty_level": "medium",
        "themes": ["animals", "sharing", "friendship", "self-esteem"],
        "reading_time_minutes": 8
    }
]

# Define new books to create
NEW_BOOKS = [
    # Toddlers (1-3 years)
    {
        "title": "Goodnight Moon",
        "file_name": "goodnight_moon.txt",
        "author": "Margaret Wise Brown",
        "description": "A little bunny says goodnight to everything in his bedroom as he prepares for sleep.",
        "age_group": "Toddlers",
        "difficulty_level": "easy",
        "themes": ["bedtime", "routine", "objects", "comfort"],
        "reading_time_minutes": 3,
        "content": """In the great green room
There was a telephone
And a red balloon
And a picture of-
The cow jumping over the moon

And there were three little bears sitting on chairs
And two little kittens
And a pair of mittens
And a little toy house
And a young mouse
And a comb and a brush and a bowl full of mush
And a quiet old lady who was whispering "hush"

Goodnight room
Goodnight moon
Goodnight cow jumping over the moon
Goodnight light
And the red balloon
Goodnight bears
Goodnight chairs
Goodnight kittens
And goodnight mittens
Goodnight clocks
And goodnight socks
Goodnight little house
And goodnight mouse
Goodnight comb
And goodnight brush
Goodnight nobody
Goodnight mush
And goodnight to the old lady whispering "hush"
Goodnight stars
Goodnight air
Goodnight noises everywhere"""
    },
    {
        "title": "Peek-a-Boo Forest",
        "file_name": "peek_a_boo_forest.txt",
        "author": "Children's Castle",
        "description": "A game of peek-a-boo with forest animals hiding behind trees and bushes.",
        "age_group": "Toddlers",
        "difficulty_level": "easy",
        "themes": ["animals", "forest", "games", "interactive"],
        "reading_time_minutes": 3,
        "content": """Peek-a-boo Forest

Who's hiding behind the tall oak tree?
Peek-a-boo! I see a brown bear looking at me!

Who's hiding behind the leafy bush?
Peek-a-boo! It's a little fox, so soft and plush!

Who's hiding behind the hollow log?
Peek-a-boo! It's a spotted frog ready to hop!

Who's hiding behind the berry patch?
Peek-a-boo! It's a bunny rabbit with a twitchy nose to match!

Who's hiding behind the pine tree tall?
Peek-a-boo! It's a hooting owl, watching over all!

Who's hiding behind the flower bed?
Peek-a-boo! It's a buzzing bee with a yellow head!

Who's hiding behind the mushroom red?
Peek-a-boo! It's a tiny mouse getting ready for bed!

All the forest friends come out to play,
Waving goodbye as we end our day.
Peek-a-boo! Peek-a-boo!
The forest friends say goodbye to you!"""
    },
    
    # Preschool (3-5 years)
    {
        "title": "The Color Monster",
        "file_name": "color_monster.txt",
        "author": "Anna Llenas",
        "description": "A monster learns to identify and understand different emotions through colors.",
        "age_group": "Preschool",
        "difficulty_level": "easy",
        "themes": ["emotions", "colors", "self-awareness", "feelings"],
        "reading_time_minutes": 5,
        "content": """The Color Monster

The Color Monster woke up feeling very confused today. His emotions were all mixed up!
"What's the matter?" asked his friend.
"I feel all jumbled up inside. My emotions are in a tangle!"

"Let me help you sort them out," she said.
"When you feel HAPPY, you shine bright like the sun. Everything feels light and bubbly inside.
Your color is YELLOW, like the sunshine that makes you smile.

When you feel SAD, you want to hide away and be alone.
Everything feels heavy and blue. Tears might fall like rain.
Your color is BLUE, like a rainy day that makes you feel down.

When you feel ANGRY, you burn hot like fire inside!
You want to stomp and shout and let it all out.
Your color is RED, like a flame that needs to burn bright.

When you feel AFRAID, you get small and want to run away.
Your heart beats fast and you feel like monsters might be near.
Your color is BLACK, like the shadows that make you scared.

When you feel CALM, you breathe slow and deep.
Everything feels peaceful and right with the world.
Your color is GREEN, like leaves swaying gently in the breeze.

When you feel LOVED, your heart feels full and warm.
You want to hug everyone and share that warmth.
Your color is PINK, like a big heartfelt hug."

The Color Monster put each feeling in its own jar.
Now he understood them all!
"How do you feel today?" his friend asked.
"Today I feel... HAPPY!" said the Color Monster with a big yellow smile."""
    },
    {
        "title": "Dinosaur Dance",
        "file_name": "dinosaur_dance.txt",
        "author": "Children's Castle",
        "description": "Different dinosaurs show off their dance moves at a prehistoric party.",
        "age_group": "Preschool",
        "difficulty_level": "easy",
        "themes": ["dinosaurs", "dancing", "music", "movement"],
        "reading_time_minutes": 4,
        "content": """Dinosaur Dance

The music starts, it's time to play,
At the dinosaur dance party today!

Tyrannosaurus Rex does the STOMP!
Big feet pounding, STOMP! STOMP! STOMP!
His arms are short but his legs are strong,
He stomps to the beat all day long!

Triceratops does the NOD!
Swinging horns from side to side, NOD! NOD! NOD!
Three horns moving with the beat,
The Triceratops dance can't be beat!

Stegosaurus does the WIGGLE!
Tail plates swaying, WIGGLE! WIGGLE! WIGGLE!
Spiky tail moving to and fro,
Stegosaurus puts on quite a show!

Pterodactyl does the FLAP!
Wings spread wide, FLAP! FLAP! FLAP!
Soaring high above the ground,
Making whooshing, flapping sounds!

Brachiosaurus does the STRETCH!
Long neck reaching, STRETCH! STRETCH! STRETCH!
Taller than the tallest trees,
Swaying gently in the breeze!

Velociraptor does the SPIN!
Twirling fast, SPIN! SPIN! SPIN!
Quick and clever on its toes,
Round and round the raptor goes!

All the dinosaurs dance together,
Stomping, nodding, with feather and leather.
The dinosaur dance is so much fun,
Let's do it again when the song is done!"""
    },
    
    # Early Readers (5-7 years)
    {
        "title": "Space Explorer Sam",
        "file_name": "space_explorer_sam.txt",
        "author": "Children's Castle",
        "description": "Sam goes on an adventure through the solar system, learning about planets along the way.",
        "age_group": "Early Readers",
        "difficulty_level": "medium",
        "themes": ["space", "adventure", "science", "exploration"],
        "reading_time_minutes": 6,
        "content": """Space Explorer Sam

Sam built a rocket ship in the backyard. It was shiny and silver with a red door.
"Today," said Sam, "I'm going to explore space!"

Sam put on a space helmet and climbed inside the rocket.
"3... 2... 1... BLAST OFF!" The rocket zoomed up into the sky!

First, Sam visited the Moon. It was gray and dusty.
"The Moon has no air," said Sam. "And look at all these craters!"
Sam bounced around in the low gravity. "Boing! Boing! Boing!"

Next, Sam flew to Mercury. "Wow, it's so hot here!" said Sam.
Mercury was closest to the Sun, so it was very, very hot.
"Too hot for me!" Sam quickly jumped back in the rocket.

Then Sam visited Venus. It was covered in thick clouds.
"Venus has poisonous air," said Sam. "I'll stay in my rocket for this planet!"

Sam flew to Mars next. It was red and rocky.
"Mars has tall mountains and deep valleys," said Sam.
Sam picked up a red rock to take home as a souvenir.

After Mars, Sam saw Jupiter. It was ENORMOUS!
"Jupiter is the biggest planet," said Sam. "Look at that giant red spot! It's actually a big storm."

Next was Saturn with its beautiful rings.
"The rings are made of ice and rock," said Sam. "They sparkle like diamonds!"

Sam zoomed past Uranus, which was tilted on its side.
"Uranus looks like it's rolling around the Sun," laughed Sam.

The last planet was Neptune, dark blue and windy.
"Neptune has the fastest winds in the whole solar system," said Sam, as the rocket wobbled in the strong breeze.

Beyond Neptune, Sam saw tiny Pluto.
"You're a dwarf planet now," Sam told Pluto, "but you're still special!"

Then Sam's rocket turned around and headed for home.
"Earth is the most beautiful planet of all," said Sam, looking at the blue oceans and green lands.

Sam's rocket landed gently in the backyard.
"What an adventure!" said Sam. "Tomorrow, I'll explore the deep sea!"

But that's another story..."""
    },
    {
        "title": "The Magic Paintbrush",
        "file_name": "magic_paintbrush.txt",
        "author": "Children's Castle",
        "description": "A girl discovers a paintbrush that brings whatever she paints to life.",
        "age_group": "Early Readers",
        "difficulty_level": "medium",
        "themes": ["magic", "creativity", "art", "responsibility"],
        "reading_time_minutes": 7,
        "content": """The Magic Paintbrush

Mia loved to paint. Every day after school, she would sit at her desk and paint pictures of flowers, animals, and landscapes.

One day, while walking home from school, Mia saw something glittering in the grass. It was a paintbrush with a golden handle! Mia picked it up and took it home.

That evening, Mia decided to try her new paintbrush. She dipped it in blue paint and painted a small blue bird on her paper. Suddenly, the bird flapped its wings and flew off the page! It circled around Mia's room, chirping happily.

"It's magic!" gasped Mia. She could hardly believe her eyes!

Excited, Mia painted a butterfly with purple wings. Just like the bird, the butterfly came to life and fluttered around the room.

The next day, Mia painted a bowl of fruit when she felt hungry. The apples, bananas, and oranges popped off the page, and she enjoyed a delicious snack.

Soon, Mia was using her magic paintbrush for everything. She painted new toys, candy, and even a small puppy that followed her everywhere.

One day, Mia's friend Leo came to visit. "I wish I had a new bike," he sighed. "Mine is too small now."

"I can help!" said Mia. She painted a shiny red bicycle, and it appeared right in front of them.

"Wow!" exclaimed Leo. "How did you do that?"

Mia showed Leo her magic paintbrush. "It makes everything I paint come to life!"

Leo's eyes widened. "Could you paint me a video game console? And maybe some ice cream? Oh, and a skateboard too!"

Mia hesitated. "I don't know, Leo. Maybe we shouldn't use the paintbrush for too many things."

But Leo insisted, and soon Mia was painting all sorts of things for him and other friends who had heard about her magic brush.

That night, Mia's room was so full of painted objects that she could barely move. Some of the animals she had painted were making noise, and the toys were everywhere.

"This is too much," Mia realized. "I need to be more careful with what I paint."

The next day, Mia decided to use her paintbrush differently. She painted a beautiful garden for the community park. She painted warm clothes for children who needed them. She painted food for the local animal shelter.

When people asked her to paint toys or treats, Mia would say, "The magic paintbrush should be used to help others, not just to get things we want."

From then on, Mia used her magic paintbrush wisely. And though she still occasionally painted a butterfly just to watch it fly, she discovered that using her gift to help others made her much happier than painting things just for herself.

As for the painted puppy? He stayed with Mia forever, a reminder of the day she found a truly magical paintbrush and learned the importance of using its power responsibly."""
    },
    
    # Growing Readers (7-9 years)
    {
        "title": "The Time Traveling Twins",
        "file_name": "time_traveling_twins.txt",
        "author": "Children's Castle",
        "description": "Twins discover a magical watch that lets them travel through time and witness historical events.",
        "age_group": "Growing Readers",
        "difficulty_level": "medium",
        "themes": ["time travel", "history", "adventure", "siblings"],
        "reading_time_minutes": 8,
        "content": """The Time Traveling Twins

Chapter 1: The Strange Watch

Jack and Emma were twins, but they couldn't be more different. Jack loved science and facts. Emma loved art and stories. But they both loved adventures.

One rainy Saturday, while exploring their grandmother's attic, they found an old wooden box tucked behind some dusty books.

"What do you think is inside?" Emma asked, her eyes wide with excitement.

Jack carefully opened the box. Inside was a strange-looking pocket watch with unusual symbols instead of numbers and three small buttons on the side.

"Cool! It must be really old," Jack said, examining it closely.

Suddenly, Emma pressed the middle button. The watch began to glow with a blue light, and the hands spun rapidly.

"What did you do?" Jack gasped.

Before Emma could answer, a swirl of golden light surrounded them both. The attic disappeared, and the twins felt like they were falling through the air.

Chapter 2: Ancient Egypt

With a thud, Jack and Emma landed on hot, sandy ground. The bright sun made them squint after the darkness of the attic.

"Where are we?" Emma whispered, looking around in awe.

They were standing near a river, and in the distance, they could see people working on an enormous triangular structure.

"That's... that's a pyramid being built!" Jack exclaimed. "Emma, I think we've traveled back in time. We're in Ancient Egypt!"

"The watch!" Emma remembered. "It must be a time machine!"

They watched as workers pulled massive stone blocks up ramps. Nearby, artists painted colorful hieroglyphics on papyrus.

A young boy about their age approached them, looking curiously at their modern clothes.

"Hello," Jack said nervously.

The boy tilted his head, not understanding.

Emma smiled and pointed to the pyramid, then made drawing motions. The boy grinned and led them to where artists were working. He handed Emma a brush with pigment and showed her how to paint hieroglyphics.

After spending hours learning about Ancient Egyptian life, Jack looked at the watch.

"I think if we press this button again, we might go somewhere else," he said.

Emma nodded excitedly. "Let's see where else we can go!"

Jack pressed the button. The golden light surrounded them once more.

Chapter 3: The Middle Ages

This time, they landed in a grassy field near a massive stone castle. People in medieval clothing hurried past them, and knights on horseback trotted by.

"We're in the Middle Ages!" Jack gasped. "Maybe the 12th or 13th century."

They wandered through a village market, marveling at the blacksmiths, bakers, and weavers at work. Music played as a juggler entertained the crowd.

"Look!" Emma pointed to a group of children playing a game with sticks and a leather ball.

The children waved them over, and soon Jack and Emma were learning a medieval game, laughing as they tried to hit the ball with the sticks.

Later, they watched a tournament where knights competed in jousting matches, the colorful banners fluttering in the breeze.

"This is amazing," Emma whispered. "It's like our history books come to life."

"Ready for another journey?" Jack asked, his finger hovering over the watch button.

"Absolutely!" Emma nodded.

Chapter 4: The First Flight

The golden light faded, and the twins found themselves standing on a windy beach. Nearby, two men were working on what looked like a giant kite with propellers.

"No way," Jack breathed. "That's Orville and Wilbur Wright! We're at Kitty Hawk, North Carolina in 1903!"

"Are we about to see the first airplane flight?" Emma asked excitedly.

They watched as the Wright brothers prepared their flying machine. The crowd was small, just a few people gathered to witness what would become a historic moment.

When the plane lifted off the ground and flew for 12 seconds before landing, everyone cheered. Jack and Emma jumped up and down, knowing they were witnessing one of history's most important events.

A photographer was setting up his camera to document the flight.

"Excuse me," he said to Jack and Emma. "Would you children like to be in a photograph with the Wright brothers and their flying machine?"

"Yes please!" they answered together.

After the photo was taken, Jack whispered, "Do you realize that we're now part of history? That photograph will exist in the future—our present!"

Emma grinned. "I wonder if we'll find it in a history book when we get home."

Chapter 5: The Return

As the sun began to set at Kitty Hawk, Jack examined the watch more carefully.

"I think this third button might take us home," he said.

"I'm ready," Emma said. "This has been the best adventure ever, but I miss home."

Jack pressed the third button. The golden light appeared once more, swirling around them.

They landed back in their grandmother's attic, exactly where they had been before their adventure began. According to the regular clock on the wall, only five minutes had passed.

"Did that really happen?" Emma wondered.

Jack carefully placed the watch back in its box. "Look at your hands," he said.

Emma looked down. Her fingers still had traces of Egyptian paint on them, and a small piece of straw from the medieval village was stuck to her sleeve.

Just then, their grandmother called up to the attic. "Children! Come down for lunch and tell me what treasures you've found up there!"

The twins looked at each other and smiled.

"You wouldn't believe us if we told you," Jack called back.

"But we'll definitely be exploring the attic again very soon," Emma added, her eyes twinkling with the promise of new adventures through time.

THE END"""
    },
    {
        "title": "The Secret Garden Club",
        "file_name": "secret_garden_club.txt",
        "author": "Children's Castle",
        "description": "A group of friends transform an abandoned lot into a beautiful community garden while learning about plants and teamwork.",
        "age_group": "Growing Readers",
        "difficulty_level": "medium",
        "themes": ["nature", "friendship", "community", "gardening"],
        "reading_time_minutes": 8,
        "content": """The Secret Garden Club

Chapter 1: The Empty Lot

On Maple Street, between the bakery and the bookstore, there was an empty lot. Most people walked right past it without a second glance. Weeds grew tall, old cans and paper littered the ground, and a broken fence sagged around it.

But Lily Chen saw something different when she looked at the empty lot. She saw possibilities.

"We could turn this into something beautiful," she told her best friend, Marcus, one day after school.

Marcus raised an eyebrow. "It's just a garbage dump. What could we possibly do with it?"

"A garden," Lily said, her eyes bright with excitement. "We could plant flowers and vegetables. Maybe even fruit trees!"

Marcus kicked at an empty soda can. "That would take forever. And who would help us?"

"We'll find people," Lily said confidently. "We'll start a club—a secret garden club!"

Chapter 2: Gathering the Team

The next day at school, Lily and Marcus passed notes to five other kids: Zoe, who lived in the apartment above the bakery; twins Elijah and Elena, who knew everything about bugs; Sophie, whose grandmother had the most beautiful garden in town; and Jackson, who was always willing to help.

The note said: "Secret meeting. Empty lot on Maple Street. 3:30 PM. Tell no one. It's about a mission to transform our neighborhood."

At 3:30, all seven children gathered at the empty lot. Lily explained her vision for a community garden.

"But why keep it a secret?" asked Sophie.

"Because," Lily grinned, "I want it to be a surprise. Imagine how amazing it will be when people walk by one day and see a beautiful garden instead of this mess!"

"I'm in," said Jackson. "My dad has some gardening tools we can borrow."

"My grandmother can teach us what to plant," offered Sophie.

"We know which bugs are good for gardens and which ones aren't," Elijah and Elena said together.

"I can bring snacks from the bakery," said Zoe.

Marcus sighed, but he was smiling. "I guess I'm in too. Someone has to keep you all organized."

And so, the Secret Garden Club was born.

Chapter 3: Getting Started

For the next few weeks, the club met every day after school. First, they cleaned up the trash and pulled the weeds. It was hard work, and they filled dozens of garbage bags.

"I found something!" called Elena one afternoon. Partially buried in the soil was an old sign that read "Rose's Place."

"Who's Rose?" asked Jackson.

No one knew, but they decided to name their garden "Rose Garden" in honor of the mysterious sign.

Sophie's grandmother, without knowing exactly what they were doing, taught them about which plants would grow well in their area. The twins researched companion planting—which plants grow better together.

Marcus made detailed maps of where everything would go: vegetables in the sunny spots, shade-loving plants under the tree in the corner, flowers along the edges to attract butterflies and bees.

Jackson's father, thinking his son had suddenly developed an interest in gardening, happily lent them shovels, rakes, and other tools.

Chapter 4: Challenges

Not everything went smoothly. One day, they arrived to find that someone had knocked down the pile of rocks they were using to outline the garden beds.

"Maybe it was the wind," suggested Zoe, but they all knew it wasn't.

A few days later, they spotted some older kids throwing rocks at their newly hung bird feeder.

"Hey, stop that!" Jackson called out.

"What do you kids think you're doing here anyway?" asked one of the older boys.

"We're making a garden," Lily said proudly.

The older kids laughed. "A garden? In this dump? Good luck with that!" They walked away, still laughing.

Then came the hardest challenge: rain. It rained for a week straight, and they couldn't work in the garden. When they finally returned, many of the seeds they had planted had washed away.

"Maybe this was a stupid idea," Marcus said, kicking at a puddle.

But Lily wouldn't give up. "We'll just start again. We'll plant more seeds. We'll build little barriers to protect them from rain."

"I don't know..." Elijah sighed.

"Actually," Elena said, studying the ground, "look at these." She pointed to tiny green sprouts poking through the mud. "Some of our seeds survived. They're growing!"

That was all the encouragement they needed.

Chapter 5: The Garden Grows

As spring turned to summer, the garden began to flourish. Radishes and lettuce were the first vegetables ready to harvest. Zoe's mother, who owned the bakery, was surprised when her daughter brought home fresh lettuce.

"Where did you get this?" she asked.

"It's a secret," Zoe replied with a smile.

The sunflowers Jackson planted grew taller than any of them. Sophie's herb garden filled the air with wonderful smells. The twins built insect houses to attract helpful bugs.

People walking by started to notice. They would stop and look through the mended fence at the unexpected oasis.

"What are you kids doing in there?" a woman asked one day.

"We're the Secret Garden Club," Lily told her. "But it won't be a secret much longer."

Chapter 6: The Mysterious Gardener

One morning, the club arrived to find that someone had been in their garden. A new bench made of polished wood sat under the shady tree. A bird bath stood in the center of the flower section. And most mysteriously, a rose bush had been planted near the entrance—not just any roses, but ones with petals that faded from yellow in the center to deep red at the tips.

"Who could have done this?" Sophie wondered.

"There's a note," said Marcus, pointing to a small envelope attached to the bench.

The note read: "To the Secret Garden Club—thank you for bringing Rose's Place back to life. Keep growing beautiful things. —R"

"R for Rose!" Zoe exclaimed. "She must be a real person!"

They never discovered exactly who Rose was, though Sophie's grandmother later told them stories about an old flower shop that once stood on that lot, owned by a woman who gave free bouquets to anyone who seemed sad.

Chapter 7: Garden Festival

By the end of summer, the Secret Garden Club decided it was time to reveal their work to the neighborhood. They made invitations for a "Garden Festival" and delivered them to every house and business nearby.

On festival day, they hung colorful streamers from the sunflowers. Zoe's mother brought pastries from the bakery. Sophie's grandmother taught a short class on herb gardening. The twins gave a tour explaining all the plants and beneficial insects. Jackson built a small stage where Elena played her violin. Marcus handed out maps of the garden with the names of all the plants.

And Lily stood proudly at the gate, welcoming everyone to Rose Garden.

Among the visitors were the older kids who had once laughed at their efforts. "This is actually pretty cool," one admitted. "Could we... maybe help sometimes?"

Even more surprising was an elderly woman who arrived last, walking slowly with a cane. She looked around with tears in her eyes.

"Are you Rose?" Lily asked hesitantly.

The woman smiled. "No, dear. But I knew her. Rose was my aunt. Her flower shop stood right here when I was your age. She would have loved what you've done with this place."

As the sun began to set on their successful festival, the seven members of the Secret Garden Club sat together on Rose's bench, tired but happy.

"So," Marcus said, looking at Lily, "what's our next project?"

Lily grinned. "I was thinking maybe a little free library to go with our garden. Or a birdhouse building workshop. Or—"

"One thing at a time!" everyone laughed.

But they all knew that with friendship, hard work, and imagination, they could make anything grow.

THE END"""
    },
    
    # Confident Readers (9-11 years)
    {
        "title": "The Mystery of Blackwood Manor",
        "file_name": "blackwood_manor.txt",
        "author": "Children's Castle",
        "description": "Four friends investigate strange occurrences at an old mansion and uncover a century-old secret.",
        "age_group": "Confident Readers",
        "difficulty_level": "hard",
        "themes": ["mystery", "friendship", "history", "problem-solving"],
        "reading_time_minutes": 12,
        "content": """The Mystery of Blackwood Manor

Chapter 1: The Old Mansion

Blackwood Manor stood on the hill overlooking Riverdale, its dark windows like watchful eyes. For as long as anyone could remember, the mansion had been abandoned, its gardens overgrown, its gates rusted shut. Stories about the house had circulated for generations—tales of strange lights, eerie music, and the ghost of old Mr. Blackwood himself, who had disappeared under mysterious circumstances exactly one hundred years ago.

Twelve-year-old Olivia Chen had heard all these stories. As the editor of the Riverdale Middle School newspaper, she had a keen interest in local history—and potential headline-worthy investigations. Blackwood Manor had always fascinated her, but until recently, the property had been strictly off-limits, surrounded by a tall fence with "NO TRESPASSING" signs.

That changed when the town council announced the mansion would be demolished to make way for a shopping center. Suddenly, the fence came down, and workers began assessing the property.

"This is our chance," Olivia told her three best friends as they sat at their usual lunch table. "We have to investigate Blackwood Manor before it's gone forever."

"You want to go inside a haunted house?" Miguel asked, his sandwich halfway to his mouth.

"It's not haunted," said Zack, the group's resident skeptic. "Those are just stories people made up."

"Either way, I'm in," declared Ava, whose passion for photography was matched only by her love of adventure. "Think of the pictures I could take inside a century-old mansion!"

"So we're agreed?" Olivia looked around the table. "Saturday morning, we meet at the oak tree near the manor's gate."

Reluctantly, Miguel and Zack nodded.

Little did they know that their exploration would uncover secrets that had been buried for a hundred years—secrets someone was still desperate to keep hidden.

Chapter 2: Into the Manor

Saturday morning dawned bright and clear. Olivia arrived at the oak tree first, notebook in hand, followed closely by Ava with her camera.

"I can't believe we're actually doing this," Miguel said as he joined them, carrying a backpack. "I brought flashlights, water, and snacks."

"And I brought logic and reason," added Zack, the last to arrive. "Remember, old houses make strange noises. It's just the wood settling."

The four friends approached the manor's main gate, which hung partially open. Construction equipment sat idle in the driveway—the demolition wasn't scheduled to begin until the following month.

"Look," Olivia pointed to a sign that read: "PROPERTY ASSESSMENT IN PROGRESS. AUTHORIZED PERSONNEL ONLY."

"Well, we're not exactly authorized," Zack whispered.

"We're just... junior historians," Olivia replied with a grin. "Documenting the manor before it's lost forever."

They slipped through the gate and approached the mansion. Up close, Blackwood Manor was even more impressive—three stories of Gothic architecture with towers, gables, and intricate stonework. Vines crawled up the walls, and the once-grand entrance was partially blocked by fallen debris.

"The side door might be easier," suggested Miguel, pointing to a smaller entrance partially hidden by overgrown bushes.

The door was locked, but the window beside it had a broken pane. Carefully, Ava reached through, found the latch, and pushed the window open.

"After you," she said to Zack with a smirk.

One by one, they climbed through the window into what appeared to be a butler's pantry. Dust covered every surface, and cobwebs stretched from ceiling to floor.

"This place hasn't been touched in decades," whispered Olivia, running her finger through the thick dust on a countertop.

"Let's stay together," Miguel suggested, switching on his flashlight despite the daylight streaming through the dirty windows.

They moved into the kitchen, where ancient cast-iron stoves and rusty utensils told of elaborate meals prepared long ago. From there, they entered a grand hallway with a sweeping staircase leading to the upper floors.

"This place must have been amazing in its day," Ava said, snapping photos of the ornate chandelier hanging precariously above them.

"Let's check out the main rooms first," Olivia suggested, leading them toward what appeared to be a library.

Rows of bookshelves still held leather-bound volumes, now warped and moldy from years of neglect. A massive desk dominated the center of the room, and portraits of stern-looking men and women—the Blackwood family, presumably—hung on the walls.

As they explored, a sudden thud from upstairs made them freeze.

"What was that?" Miguel whispered.

"Just the house settling," Zack said automatically, though he didn't sound convinced.

"Or maybe we're not alone," Ava suggested, her camera poised as if ready to capture whatever—or whoever—might appear.

"Only one way to find out," said Olivia, heading back toward the staircase.

Chapter 3: Strange Discoveries

The grand staircase creaked ominously as the four friends ascended to the second floor. Here, long corridors stretched in both directions, lined with doors leading to countless rooms.

"Where do we start?" asked Miguel.

"Let's try to find the master bedroom," Olivia suggested. "That might tell us more about Mr. Blackwood himself."

They tried several doors. One led to a child's nursery, frozen in time with antique toys still scattered across the floor. Another revealed a music room with a grand piano, its keys yellowed with age.

"Listen," Zack said suddenly, holding up his hand.

From somewhere deep within the house came the faint sound of music—a simple, melancholy melody.

"That's impossible," he continued. "There's no electricity here. How could there be music?"

"Maybe someone's playing one of the instruments," Ava suggested, though her voice trembled slightly.

They followed the sound to the end of the corridor, where a narrow door stood slightly ajar. Beyond it, a spiral staircase led up to what must have been one of the manor's towers.

The music was louder here, drifting down from above.

"Should we go up?" Miguel asked.

Before anyone could answer, the music stopped abruptly. A moment later, they heard footsteps—quick and light—moving across the floor above them.

"Hello?" Olivia called out. "Is someone there?"

Silence.

"We should check it out," Ava said, already starting up the stairs, her camera ready.

The tower room was circular, with windows on all sides offering spectacular views of Riverdale and the surrounding countryside. A dust-covered music box sat open on a small table, but no one was there.

"The music must have come from this," Zack said, examining the antique music box. "But who wound it up?"

"And where did they go?" added Miguel, looking around the empty room with no other exits.

Olivia approached the table and noticed a leather-bound journal beside the music box. Carefully, she opened it, revealing elegant handwriting that filled page after page.

"It's a diary," she said, excitement creeping into her voice. "Dated 1923, belonging to... Eleanor Blackwood."

"Who's Eleanor Blackwood?" asked Ava, joining her at the table.

"Mr. Blackwood's daughter, I think," Olivia replied, carefully turning the brittle pages. "Look at this entry: 'Father has been working in the cellar for weeks now. He won't tell anyone what he's doing down there, not even Mother. I'm worried about him. The strange noises continue at night, and sometimes I see lights from the cellar windows when everyone is supposed to be asleep.'"

"Sounds like old Mr. Blackwood had a secret," Miguel said, peering over Olivia's shoulder.

"Listen to this," Olivia continued, turning to the last entry. "'Father and I argued today. I told him I would tell Mother about what he's been hiding in the cellar if he didn't stop. He looked frightened, then angry. Said I didn't understand the importance of his work. I fear what he might do next, which is why I've—'" Olivia paused, frowning. "The entry stops mid-sentence."

"And right after that, according to the stories, Mr. Blackwood disappeared," Zack said thoughtfully.

"Do you think Eleanor might have had something to do with it?" Ava suggested, snapping a photo of the diary.

"I think we need to check out that cellar," Olivia decided, carefully placing the diary in her bag. "If Mr. Blackwood was hiding something down there, it might explain what happened to him."

As they turned to leave the tower room, a cold draft swept through, and the door slammed shut with a bang.

Miguel jumped. "Okay, that was definitely not the house settling."

Zack tried the door handle. "It's locked," he said, his voice rising slightly in panic. "How can it be locked? There's no key hole on this side."

"There has to be another way out," Olivia said, trying to stay calm. "Maybe one of these panels opens to a secret passage or something."

They began searching the circular room, pressing panels, tapping on the walls, looking for any hidden mechanism.

"I found something!" Ava exclaimed after several minutes. She was kneeling beside the table with the music box. "There's a small lever underneath."

She pulled it, and a section of the wooden floor slid open, revealing another set of stairs, these descending into darkness.

"Secret stairs," Miguel whispered. "Cool but creepy."

"Where do you think they lead?" asked Zack.

"Only one way to find out," Olivia replied, taking Miguel's flashlight and shining it down the dark passage. "Let's go."

Chapter 4: The Secret Below

The hidden staircase descended in a tight spiral, forcing them to proceed single-file with only Miguel's flashlight to guide them. The air grew colder and damper as they went deeper.

"I think we're heading for the cellar," Olivia whispered, in the lead with the flashlight.

"The cellar that Eleanor's father was doing something secret in," Ava reminded them, her camera occasionally flashing as she documented their descent.

"Maybe this isn't such a good idea," Miguel suggested from behind her. "If Mr. Blackwood was hiding something dangerous..."

"It was a hundred years ago," Zack pointed out, bringing up the rear. "Whatever it was, it's probably long gone by now."

The stairs finally ended at a small wooden door. Olivia tried the handle—it turned easily. Taking a deep breath, she pushed the door open.

What lay beyond was not at all what they had expected.

Instead of a dusty, cobweb-filled cellar, they entered what appeared to be a fully equipped scientific laboratory, with workbenches, glass containers, and strange apparatus that none of them recognized. Most surprising of all, the room was clean and well-maintained, in stark contrast to the abandoned state of the rest of the manor.

"This doesn't make sense," Zack said, staring around in disbelief. "This equipment looks modern. Someone's been using this place."

"Recently, too," Ava added, touching one of the workbenches. "No dust."

Olivia moved deeper into the laboratory, her flashlight revealing more surprises. Glass cases lined one wall, containing what appeared to be geological specimens—crystals and rocks of various colors and formations. In the center of the room stood a large machine with dials, gauges, and a glass chamber at its heart.

"What is all this?" Miguel wondered aloud.

"I think," Olivia said slowly, examining a journal open on one of the workbenches, "this is what Mr. Blackwood was working on. And someone has continued his research."

The journal contained complex equations, diagrams, and notes written in a cramped hand. The most recent entry was dated just three days prior.

"According to this," Olivia continued, flipping through the pages, "Blackwood discovered some kind of crystal with unusual properties. He believed it could... this is going to sound crazy... manipulate time."

"Time travel?" Ava asked incredulously.

"Not exactly. More like... slowing time down or speeding it up in a localized area."

"That's impossible," Zack stated flatly.

"Maybe now," Olivia replied, "but the journal says Blackwood was decades ahead of his time. The modern notes suggest someone found his research and has been trying to complete it."

"But who?" Miguel asked. "And why keep it secret all these years?"

Before anyone could answer, they heard a door opening somewhere in the laboratory, followed by footsteps.

"Hide!" Olivia hissed, snapping off the flashlight.

They ducked behind a large piece of equipment just as a figure entered the room and switched on the lights. To their shock, they recognized Mayor Wilson, Riverdale's longtime mayor and the main proponent of the plan to demolish Blackwood Manor.

The mayor moved purposefully through the laboratory, checking instruments and making notes. He seemed completely at home among the strange equipment.

"What's the mayor doing here?" Miguel whispered.

"Shh!" the others warned.

Mayor Wilson approached the central machine, removed a small box from his pocket, and carefully extracted what appeared to be a crystal—glowing faintly with an inner blue light. He placed it in the glass chamber of the machine and began adjusting dials.

The machine hummed to life, the crystal's glow intensifying until it illuminated the entire room with pulsing blue light. The air seemed to thicken, and Olivia felt a strange sensation, as if time itself was stretching around them.

Then Ava's camera, set to automatic, flashed.

Mayor Wilson whirled around. "Who's there?" he demanded.

The four friends remained frozen in their hiding place.

"I know someone's there," the mayor continued. "Come out now."

After a moment's hesitation, Olivia stood up. The others reluctantly followed.

"Children?" Mayor Wilson seemed genuinely surprised. "How did you get in here?"

"Through the manor," Olivia replied. "We found the secret passage from the tower."

The mayor's expression darkened. "You shouldn't be here. This area is restricted for a reason."

"Because you're continuing Mr. Blackwood's experiments?" Olivia asked boldly.

Mayor Wilson stared at her, then sighed. "You're the Chen girl, aren't you? The one who's always asking questions for that school newspaper."

Olivia nodded.

"Well, you've certainly found a bigger story than you bargained for," he said, switching off the machine. The crystal's glow faded, and the strange feeling in the air dissipated.

Chapter 5: The Truth Revealed

"I suppose you deserve an explanation," Mayor Wilson said, gesturing for them to sit on lab stools while he leaned against a workbench.

"Franklin Blackwood was my great-grandfather," he began. "He was a brilliant scientist and inventor, decades ahead of his time. In the 1920s, he discovered a unique crystal formation in the caves beneath this property. These crystals exhibited properties that defied the physics of his day—they could influence the flow of time in a localized field."

"That's scientifically impossible," Zack interjected.

"With our current understanding of physics, yes," the mayor agreed. "But there are still many mysteries in our universe. Franklin believed these crystals could revolutionize everything from medicine to energy production. Imagine being able to slow the progression of disease, or accelerate plant growth to end food shortages."

"So what happened to him?" Olivia asked. "The stories say he disappeared."

Mayor Wilson's expression grew somber. "Eleanor happened. My great-aunt. She found out about his work and threatened to expose it. She didn't understand the potential benefits—she only saw the danger if such power fell into the wrong hands. They argued, and during their confrontation, there was an accident with an early version of this machine."

He gestured to the device in the center of the room.

"The accident created what Franklin called a 'time bubble'—a field where time moved at a different rate than the outside world. Franklin was caught in it. To everyone else, he seemed to vanish instantly. But from his perspective, time slowed to near standstill. He experienced mere minutes while years passed outside the bubble."

"Are you saying... he's still alive?" Miguel asked incredulously.

"No," the mayor shook his head. "The bubble collapsed after about thirty years. By then, the manor had been abandoned, the family fortune lost in the Depression. When Franklin 'returned' to normal time, he was a man out of time, his family gone or aged, his work forgotten. He lived out his remaining years in seclusion in this cellar, continuing his research in secret."

"And you found his research," Olivia guessed.

"As a boy, I discovered the secret passage just as you did. My great-grandfather was still alive then, very old. He taught me about his work before he died, made me promise to protect it until the world was ready for such knowledge."

"But you're planning to demolish the manor," Ava pointed out. "Why now?"

"Because after decades of research, I've finally stabilized the crystal's energy output," the mayor explained. "I can now safely move the laboratory to a secure facility. The demolition plan was the perfect cover to complete the transfer without drawing attention."

"So what happens now?" Zack asked, voicing what they were all thinking.

Mayor Wilson studied them thoughtfully. "That depends. I've dedicated my life to protecting this secret, ensuring this technology doesn't fall into the wrong hands until it can be properly understood and regulated."

"We could help," Olivia suggested quickly. "Instead of a story about ghosts at Blackwood Manor, I could write about the historic preservation of an important scientific landmark."

"A campaign to save the manor instead of demolishing it," Ava added excitedly.

"The public doesn't need to know about the crystals," Miguel said. "Just that there's historical value worth preserving."

Mayor Wilson looked surprised. "You'd help keep the true secret?"

"Some discoveries do need protection until the world is ready," Olivia admitted. "But that doesn't mean the manor has to be destroyed. It's part of our town's history."

"And think of the educational opportunities," Zack added. "The upper floors could be a museum while the laboratory remains secure."

Mayor Wilson considered this for a long moment, then smiled. "You know, you remind me of my great-grandfather. He always said that with great discoveries come great responsibilities—and that the best guardians are often those who understand both the potential and the risk."

"Does that mean...?" Olivia began.

"It means I think we can work together to save Blackwood Manor, preserve its history, and protect its secrets until the time is right."

Chapter 6: A New Beginning

Three months later, Olivia stood at the podium on the freshly restored front steps of Blackwood Manor. Behind her, the once-abandoned mansion gleamed with new paint and repairs, its windows no longer dark and foreboding but sparkling in the sunlight.

"And so," she concluded, reading from her prepared speech, "it is with great pride that we officially open the Blackwood Historical Museum and Science Center, dedicated to preserving our town's unique heritage and inspiring future generations of scientists and historians."

Applause erupted from the gathered crowd as Mayor Wilson stepped forward to cut the ceremonial ribbon stretched across the manor's entrance.

Olivia rejoined her friends, who were waiting at the side of the steps.

"Nice speech," Zack said with a grin.

"Very diplomatic," Ava agreed, snapping photos of the celebration. "Not a word about time-altering crystals or hidden laboratories."

"Sometimes the whole truth has to wait," Olivia replied, watching as visitors began to stream into the manor for the first time in decades.

The upper floors had indeed been transformed into a museum celebrating the history of Riverdale and the Blackwood family's contributions to the community. Special exhibits highlighted Franklin Blackwood's documented inventions and scientific theories—those that had been made public during his lifetime.

The cellar laboratory remained sealed off, accessible only through the hidden passage that had been carefully secured. Mayor Wilson had assembled a small team of trusted scientists who were now working under strict oversight to understand and harness the crystals' unique properties safely.

"You know what I keep thinking about?" Miguel said as they followed the crowd inside. "Eleanor Blackwood. She was right to be concerned about her father's work, but wrong to assume it could only be dangerous."

"That's the thing about discovery," Olivia replied. "It's never the knowledge itself that's good or bad—it's what we choose to do with it."

As part of the agreement with Mayor Wilson, the four friends had become junior docents at the museum, helping to guide visitors while keeping an eye on anything unusual. They were also the only young people in town who knew what really lay beneath the manor.

"Oh, I almost forgot," Ava said, pulling an envelope from her bag. "This came for us today."

Inside was a single photograph—the one they had taken in the laboratory on the day of their discovery, showing the four of them with Mayor Wilson and the crystal machine. On the back was written a simple message: "The Blackwood Legacy Guardians—may you always use wisdom in your quest for knowledge."

Olivia smiled as she looked up at the manor that had once been the source of ghost stories and was now a place of learning and inspiration.

Some mysteries were meant to be solved. Others were meant to be protected until the right time. The true mystery, she had come to realize, was knowing the difference.

THE END"""
    },
    {
        "title": "Code Breakers: The Digital Defenders",
        "file_name": "code_breakers.txt",
        "author": "Children's Castle",
        "description": "A group of tech-savvy kids use their coding skills to solve a cybersecurity threat at their school.",
        "age_group": "Confident Readers",
        "difficulty_level": "hard",
        "themes": ["technology", "teamwork", "problem-solving", "ethics"],
        "reading_time_minutes": 12,
        "content": """Code Breakers: The Digital Defenders

Chapter 1: The Glitch

"Something weird is happening to the school network," Amir said, staring at his laptop screen with a frown. "Look at this."

Maddie and Tyler leaned over to see what their friend was pointing at. The three sixth-graders were huddled at their usual table in the back corner of Westfield Middle School's library during lunch period.

"I don't see anything unusual," Maddie said, adjusting her glasses. As the school's unofficial tech genius, she rarely missed digital anomalies.

"Wait for it," Amir replied. "Watch when I try to access the homework portal."

He clicked on the link, and for a split second before the page loaded, strange symbols flashed across the screen—lines of code that shouldn't be visible to users.

"There!" Amir exclaimed. "Did you see it?"

"I saw it," Tyler confirmed. Unlike his friends, he wasn't a natural with computers, but he had sharp eyes. "What was that?"

"Some kind of script is running in the background," Maddie said, her voice dropping to a whisper. "And it's not supposed to be there."

Amir nodded. "I first noticed it yesterday during computer lab. Ms. Chen was showing us how to access the new digital library, and I saw the same thing happen on the main screen."

"Could it be a virus?" Tyler asked.

"Maybe," Maddie replied, "or malware of some kind. But school networks have protection against that stuff."

"Unless someone bypassed the security," Amir suggested.

The bell rang, signaling the end of lunch period.

"We need to investigate this," Maddie decided, closing her laptop. "Meet at my house after school. My mom's got that coding workshop tonight, so we'll have the place to ourselves."

As they gathered their things, none of them noticed Principal Garcia watching them from across the library, a concerned expression on his face.

Chapter 2: The Discovery

Maddie's bedroom looked like a cross between a computer repair shop and a science lab. Disassembled electronics covered her desk, while diagrams of circuit boards and coding flowcharts papered the walls. Her bookshelf held textbooks with titles like "Advanced Python for Teenagers" and "The Ethics of AI."

"Ok, I've been monitoring the school network all afternoon," Maddie announced as Amir and Tyler settled onto beanbag chairs. Her fingers flew across her keyboard. "The glitch appears every 15 minutes exactly, which means it's on a timer."

"Can you capture the code?" Amir asked.

"Already did." Maddie turned her screen so they could see. "It's sophisticated—definitely not a student prank."

Tyler squinted at the screen. Though he was the least tech-savvy of the trio, his logical mind often spotted patterns others missed. "That section looks like it's collecting data. See how it's creating arrays?"

Amir nodded. "Good catch. It's gathering information and sending it... somewhere."

"But what information?" Maddie wondered aloud. She typed rapidly, her expression growing more troubled. "Oh no."

"What?" both boys asked simultaneously.

"It's accessing student records. Grades, attendance, personal information—everything in the school database."

"Someone's stealing student data?" Tyler's eyes widened. "We need to tell Principal Garcia right away!"

"Wait," Amir cautioned. "We can't just accuse someone of hacking without proof. And we're not supposed to be poking around the school network like this anyway."

"Amir's right," Maddie agreed. "We need more information. Let me trace where the data is being sent."

After several minutes of intense concentration, Maddie sat back in her chair. "This is weird. The data is being forwarded to an address within the school network itself."

"So the hacker is inside the school?" Tyler asked.

"Looks that way. But there's something else..." Maddie leaned forward again, typing rapidly. "The code has another component. It's not just collecting data—it's changing it."

"Changing grades?" Amir guessed.

"No, nothing that obvious. It's making small adjustments to attendance records, lunch account balances, things most people wouldn't notice."

"But why?" Tyler wondered.

Before anyone could speculate further, Maddie's phone buzzed with a text message. She glanced at it and frowned.

"It's Principal Garcia. He wants to see the three of us in his office tomorrow morning before classes start."

The three friends exchanged worried glances.

"How does he know we're looking into this?" Amir asked.

"I don't think he does," Maddie replied, but she didn't sound convinced. "Maybe it's about something else."

"Either way," Tyler said, "we need to decide what to tell him."

Chapter 3: Unexpected Allies

The next morning, the three friends gathered outside Principal Garcia's office, each nervous for different reasons.

"Maybe he just wants to talk about the upcoming STEM fair," Amir suggested hopefully.

"Or maybe someone saw us hacking the school network and we're about to be expelled," Tyler countered, always ready to imagine the worst-case scenario.

"We weren't hacking; we were investigating a security breach," Maddie corrected. "Big difference."

Before they could debate further, the office door opened, and Principal Garcia gestured them inside. To their surprise, Ms. Chen, the computer science teacher, was already seated in the office.

"Please, sit down," Principal Garcia said, his expression unreadable. "I believe you three have discovered something unusual about our school network."

The friends exchanged startled glances.

"It's okay," Ms. Chen assured them with a small smile. "You're not in trouble. In fact, we need your help."

Principal Garcia nodded. "Ms. Chen noticed the same anomalies you did, Maddie. She's been monitoring the situation for the past week."

"Then you know someone's stealing student data," Amir blurted out.

"And making changes to school records," Tyler added.

"Yes," Ms. Chen confirmed. "But we don't know who's behind it or exactly what they're planning. The coding is extremely sophisticated."

"Which is why we're coming to you," Principal Garcia continued. "Officially, I should call in the district IT team, but that would take days, and whoever is doing this would have time to cover their tracks."

"You want us to find the hacker?" Maddie asked incredulously.

"I want you to help Ms. Chen find the hacker," the principal clarified. "You three have exceptional skills, and you've already made progress on your own."

"Isn't that dangerous?" Tyler asked. "What if the hacker realizes we're onto them?"

"That's why we need to be careful," Ms. Chen said. "I've set up a secure system in my classroom where you can investigate without being detected. But we need to move quickly."

"Why us?" Amir asked, still suspicious. "We're just kids."

Principal Garcia's expression grew serious. "Because sometimes the best way to catch someone who thinks like a student is to work with students. And because I've seen what you three can do when you put your minds together."

The friends looked at each other, a mix of excitement and apprehension on their faces.

"So," Ms. Chen asked, "are you in?"

Maddie spoke for all of them. "We're in."

Chapter 4: The Investigation

Ms. Chen's classroom after school hours had been transformed into a command center. Extra monitors and a dedicated server had been set up, isolated from the main school network.

"This way, we can observe without being observed," Ms. Chen explained as the three friends settled in. "I've created a digital sandbox where we can safely analyze the malware."

For the next two hours, they worked methodically through the code, mapping its functions and tracking its behavior. Maddie focused on reverse-engineering the program, while Amir analyzed the data transfer patterns. Tyler, with his talent for seeing the big picture, kept notes and looked for overall patterns.

"I think I've got something," Amir said eventually. "The data isn't just being collected—it's being compared."

"Compared to what?" Ms. Chen asked, looking over his shoulder.

"Historical records. It's looking for discrepancies between current data and past data."

Maddie's eyes widened. "It's an audit program! Someone's checking for inconsistencies in the school's records."

"But who would do that, and why?" Tyler wondered.

As if on cue, the classroom door opened, and a tall, thin man in a gray suit stepped in. The three students recognized him immediately—Mr. Peterson, the district financial auditor who had been working in the school office for the past month.

"That would be me," he said calmly. "And I think it's time we talked."

Ms. Chen stepped protectively in front of the students. "Mr. Peterson, what is the meaning of this?"

Mr. Peterson held up his hands placatingly. "I'm not here to cause trouble. In fact, I'm impressed with how quickly these young people identified my program. That's no small feat."

"You're the one who planted the malware?" Maddie asked, both horrified and fascinated.

"I prefer to call it an integrity verification tool," Mr. Peterson replied. "And yes, I implemented it as part of a covert audit."

"Covert?" Ms. Chen's voice was sharp. "You had no authorization to access our systems like this."

"Actually, I did," Mr. Peterson countered. "From the superintendent." He pulled an official-looking document from his briefcase. "There have been concerns about financial irregularities in several district schools. I was tasked with investigating discreetly."

Principal Garcia, who had entered behind Mr. Peterson, examined the document and nodded grimly. "It appears to be legitimate. But this kind of backdoor investigation is highly irregular."

"Sometimes irregular methods are necessary when you don't know who to trust," Mr. Peterson said. "My program was designed to identify unusual patterns in financial records without alerting potential perpetrators."

"And did you find anything?" Amir asked boldly.

Mr. Peterson hesitated, glancing at Principal Garcia. "Yes, but not what I expected. It appears someone has been siphoning small amounts from various school accounts over the past year. The individual transactions are too small to notice, but they add up."

"Who?" Ms. Chen and the students asked almost in unison.

"That's the problem," Mr. Peterson admitted. "I can track the discrepancies, but I can't identify who's making the changes. They're hiding their tracks too well."

Tyler, who had been unusually quiet, suddenly spoke up. "Could it be someone using Mr. Peterson's own program against him?"

All eyes turned to the boy.

"What do you mean?" Maddie asked.

"Well," Tyler explained, fidgeting slightly under the attention, "if someone discovered Mr. Peterson's program, they might have figured out how to use it to make their own changes while hiding inside his code."

Mr. Peterson looked startled. "That's... actually possible. My program does create a sort of digital blind spot in the system's security monitoring."

"A parasite program," Maddie breathed. "Brilliant and terrifying."

"Can you find it?" Principal Garcia asked.

Maddie exchanged glances with her friends, then nodded. "We can try. But we'll need full access to Mr. Peterson's code."

"And we'll need to set a trap," Amir added.

Chapter 5: Digital Defenders

The plan was simple but risky. They would create a fake financial transaction—a particularly tempting one—and monitor who took the bait.

"It's like leaving cheese out for a mouse," Tyler explained as they set up the trap the next day.

"Except this mouse is smart enough to hide inside someone else's programming," Amir reminded him.

Maddie had spent half the night analyzing Mr. Peterson's code and had eventually found the parasite program nested within it—a clever piece of programming that activated only when Mr. Peterson's program ran its data collection routine.

"Whoever wrote this knows what they're doing," she told the others as they finalized their preparations. "They're using Mr. Peterson's security clearance to make their changes, so the system thinks the actions are authorized."

"Do you think it's a student?" Ms. Chen asked, looking troubled.

"The code is too sophisticated for most students," Maddie admitted. "It would have to be someone with advanced programming skills and access to the financial systems."

"Like a teacher or administrator," Principal Garcia said grimly.

"Or an outside hacker who found a way in," Mr. Peterson suggested. "That's why we need to catch them in the act."

The trap was set: a fake notification about a special district fund for technology purchases, accessible through a specific link. Anyone who clicked the link would be traceable.

"Now we wait," Amir said.

They didn't have to wait long. Less than an hour after setting the trap, their monitoring system alerted them.

"Someone's accessed the link!" Maddie exclaimed. "Tracing the connection now."

Her fingers flew across the keyboard. "It's coming from... the administrative office wing. Room 118."

"That's the records room," Principal Garcia said. "It should be empty right now."

The group moved quickly and quietly down the hallway. Principal Garcia used his master key to unlock the records room door and pushed it open.

Seated at the computer inside was a familiar face: Mrs. Blackwell, the school secretary who had worked at Westfield for over fifteen years.

She looked up in shock. "Principal Garcia! I was just... organizing the digital archives."

"At the computer that's accessing our fake fund?" Maddie asked, pointing to her tablet where the trace was clearly visible.

Mrs. Blackwell's expression hardened. "I don't know what you're talking about."

"I think you do," Mr. Peterson said, stepping forward. "We've identified your parasite program hidden in my audit software. Quite ingenious, actually."

For a moment, Mrs. Blackwell seemed to consider denying everything. Then her shoulders slumped. "How did you find it? I was so careful."

"These students found it," Ms. Chen said, pride evident in her voice. "They noticed anomalies in the system that no one else did."

Mrs. Blackwell looked at Maddie, Amir, and Tyler with a mix of respect and resignation. "Outsmarted by middle schoolers. I suppose there's a certain irony there."

"Why did you do it?" Principal Garcia asked, his voice reflecting more sadness than anger.

"It started small," Mrs. Blackwell explained. "The district kept cutting our supply budget, but still expected us to have everything students needed. So I... reallocated funds. A little from the athletics account, a bit from the lunch fund surplus. Nothing that would hurt anyone."

"But it escalated," Mr. Peterson guessed.

Mrs. Blackwell nodded. "Once I started, it was hard to stop. And then I needed to cover my tracks, which meant more sophisticated methods."

"You have a background in programming," Ms. Chen realized.

"I worked in IT before becoming a school secretary," Mrs. Blackwell confirmed. "I never thought I'd use those skills like this."

As Principal Garcia called the superintendent to report what had happened, Tyler turned to his friends.

"I feel kind of bad for her," he whispered. "She thought she was helping the school."

"By stealing," Amir pointed out. "Even if her intentions were good, her methods were wrong."

Maddie nodded. "That's why ethical coding is so important. The skills we have can be used to build or to break. It's up to us to choose how to use them."

Chapter 6: A New Code

One month later, Westfield Middle School held a special assembly. Principal Garcia stood at the podium addressing the student body.

"Today, I'm pleased to announce the formation of a new club at Westfield: The Digital Defenders. This group will help maintain our school's cyber security and promote ethical technology use among students."

He gestured to Maddie, Amir, and Tyler, who joined him on stage to enthusiastic applause from their classmates.

"These three students recently helped uncover a security breach in our school's network. While I can't share all the details, their skills, dedication, and ethical approach were instrumental in resolving the situation."

What Principal Garcia didn't mention was that Mrs. Blackwell had been placed on administrative leave pending an investigation. The money she had diverted—nearly $15,000 over three years—would have resulted in criminal charges, but a deal had been worked out: she would repay the funds and help the district improve its digital security protocols.

After the assembly, as students filed out of the auditorium, Ms. Chen approached the three friends.

"I have something for you," she said, handing each of them a small box.

Inside were silver pins shaped like shields with binary code etched across them.

"Official Digital Defenders badges," Ms. Chen explained. "And these aren't just for show. The district has approved a small stipend for your club to continue monitoring school systems and teaching other students about cyber security."

"We're getting paid?" Tyler asked incredulously.

"Consider it a consulting fee," Ms. Chen said with a smile. "But with great power comes great responsibility. The skills you have are valuable, and how you choose to use them matters."

Maddie looked at the badge in her hand. "We won't let you down."

"I know you won't," Ms. Chen replied. "Oh, and one more thing. The state technology conference has invited you three to present your experience—with certain details omitted, of course."

As Ms. Chen walked away, the three friends looked at each other with matching grins.

"From lunch table hackers to official cyber security consultants," Amir said. "Not bad for sixth graders."

"Digital Defenders," Maddie repeated, liking the sound of it. "It's a good name."

"It's more than a name," Tyler added thoughtfully. "It's a promise. To use what we know to protect, not to exploit."

"A code to live by," Maddie agreed.

And as they walked together down the hall, their new badges catching the light, they knew this was just the beginning of their journey as the Code Breakers, the Digital Defenders of Westfield Middle School.

THE END"""
    }
]

def setup_age_groups():
    """Create age groups in the database"""
    print("Setting up age groups...")
    existing_groups = [group.name for group in AgeGroup.query.all()]
    
    for group_data in AGE_GROUPS:
        if group_data["name"] not in existing_groups:
            group = AgeGroup(
                name=group_data["name"],
                min_age=group_data["min_age"],
                max_age=group_data["max_age"],
                description=group_data["description"]
            )
            db.session.add(group)
            print(f"Added age group: {group_data['name']}")
    
    db.session.commit()

def categorize_existing_books():
    """Categorize existing books in the database"""
    print("Categorizing existing books...")
    existing_books = [book.file_name for book in Book.query.all()]
    
    for book_data in EXISTING_BOOKS:
        if book_data["file_name"] not in existing_books:
            # Get age group
            age_group = AgeGroup.query.filter_by(name=book_data["age_group"]).first()
            if not age_group:
                print(f"Age group {book_data['age_group']} not found. Skipping {book_data['title']}")
                continue
            
            # Create book
            book = Book(
                title=book_data["title"],
                file_name=book_data["file_name"],
                author=book_data["author"],
                description=book_data["description"],
                age_group_id=age_group.id,
                difficulty_level=book_data["difficulty_level"],
                themes=json.dumps(book_data["themes"]),
                reading_time_minutes=book_data["reading_time_minutes"]
            )
            db.session.add(book)
            print(f"Added existing book: {book_data['title']}")
    
    db.session.commit()

def create_new_books():
    """Create new books in the database and save their content to files"""
    print("Creating new books...")
    for book_data in NEW_BOOKS:
        # Check if book already exists
        existing_book = Book.query.filter_by(file_name=book_data["file_name"]).first()
        if existing_book:
            print(f"Book {book_data['title']} already exists. Skipping.")
            continue
        
        # Get age group
        age_group = AgeGroup.query.filter_by(name=book_data["age_group"]).first()
        if not age_group:
            print(f"Age group {book_data['age_group']} not found. Skipping {book_data['title']}")
            continue
        
        # Save book content to file
        try:
            with open(book_data["file_name"], "w") as f:
                f.write(book_data["content"])
            print(f"Created file: {book_data['file_name']}")
            
            # Create book record in database
            book = Book(
                title=book_data["title"],
                file_name=book_data["file_name"],
                author=book_data["author"],
                description=book_data["description"],
                age_group_id=age_group.id,
                difficulty_level=book_data["difficulty_level"],
                themes=json.dumps(book_data["themes"]),
                reading_time_minutes=book_data["reading_time_minutes"]
            )
            db.session.add(book)
            print(f"Added new book: {book_data['title']}")
        except Exception as e:
            print(f"Error creating book {book_data['title']}: {str(e)}")
    
    db.session.commit()

def main():
    """Main function to run the script"""
    with app.app_context():
        print("Starting setup of books by age groups...")
        
        # Setup age groups
        setup_age_groups()
        
        # Categorize existing books
        categorize_existing_books()
        
        # Create new books
        create_new_books()
        
        print("Setup complete!")

if __name__ == "__main__":
    main()
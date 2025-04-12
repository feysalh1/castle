import os
import json
from gtts import gTTS

# Stories from our app with the text content
stories = {
    "little_fox": {
        "title": "The Little Fox",
        "text": "Once upon a time, there was a clever little fox with a bright orange coat. He lived in a cozy den at the edge of the forest. Every day, the little fox would explore the woods, making friends with rabbits, squirrels, and birds. One day, the little fox found a lost baby bird who had fallen from its nest. The kind fox carefully picked up the bird and helped it find its way home. The mother bird was so thankful that she sang the most beautiful song just for the little fox. From that day on, whenever the fox felt lonely, he would visit his bird friends who would sing cheerful songs to brighten his day.",
        "filename": "little_fox.mp3"
    },
    "three_little_pigs": {
        "title": "Three Little Pigs",
        "text": "Once upon a time, there were three little pigs who decided to build their own houses. The first pig built a house of straw because it was quick and easy. The second pig built a house of sticks. The third pig worked hard to build a strong house of bricks. One day, a big bad wolf came along. He huffed and puffed and blew down the house of straw! The first pig ran to the second pig's house. The wolf huffed and puffed and blew down the house of sticks too! Both pigs ran to the third pig's brick house. The wolf huffed and puffed, but he could not blow down the strong brick house. The wolf tried to come down the chimney, but the pigs had a pot of hot soup waiting! The wolf ran away, and the three little pigs lived happily ever after in the brick house.",
        "filename": "three_little_pigs.mp3"
    },
    "brown_bear": {
        "title": "Brown Bear",
        "text": "Brown Bear, Brown Bear, what do you see? I see a red bird looking at me. Red Bird, Red Bird, what do you see? I see a yellow duck looking at me. Yellow Duck, Yellow Duck, what do you see? I see a blue horse looking at me. Blue Horse, Blue Horse, what do you see? I see a green frog looking at me. Green Frog, Green Frog, what do you see? I see a purple cat looking at me. Purple Cat, Purple Cat, what do you see? I see a white dog looking at me. White Dog, White Dog, what do you see? I see a black sheep looking at me. Black Sheep, Black Sheep, what do you see? I see a goldfish looking at me. Goldfish, Goldfish, what do you see? I see children looking at me!",
        "filename": "brown_bear.mp3"
    },
    "wild_things": {
        "title": "Where the Wild Things Are",
        "text": "Once there was a boy named Max who wore his wolf suit and made mischief of one kind and another. His mother called him 'WILD THING!' and Max said 'I'LL EAT YOU UP!' so he was sent to bed without eating anything. That very night in Max's room a forest grew and grew until his ceiling hung with vines and the walls became the world all around. And an ocean tumbled by with a private boat for Max, and he sailed off through night and day and in and out of weeks and almost over a year to where the wild things are. When he came to the place where the wild things are, they roared their terrible roars and gnashed their terrible teeth and rolled their terrible eyes and showed their terrible claws till Max said 'BE STILL!' and tamed them with the magic trick of staring into all their yellow eyes without blinking once. And they were frightened and called him the most wild thing of all and made him king of all wild things.",
        "filename": "wild_things.mp3" 
    },
    "black_sheep": {
        "title": "Baa Baa Black Sheep",
        "text": "Baa, baa, black sheep, Have you any wool? Yes sir, yes sir, Three bags full. One for the master, One for the dame, And one for the little boy Who lives down the lane. Baa, baa, black sheep, Have you any wool? Yes sir, yes sir, Three bags full.",
        "filename": "black_sheep.mp3"
    },
    "hickory_dickory": {
        "title": "Hickory Dickory Dock",
        "text": "Hickory dickory dock, The mouse ran up the clock. The clock struck one, The mouse ran down, Hickory dickory dock. Hickory dickory dock, The mouse ran up the clock. The clock struck two, And down he flew, Hickory dickory dock. Hickory dickory dock, The mouse ran up the clock. The clock struck three, And he did flee, Hickory dickory dock.",
        "filename": "hickory_dickory.mp3"
    },
    "bo_peep": {
        "title": "Little Bo-Peep",
        "text": "Little Bo-Peep has lost her sheep, And can't tell where to find them; Leave them alone, and they'll come home, Bringing their tails behind them. Little Bo-Peep fell fast asleep, And dreamt she heard them bleating; But when she awoke, she found it a joke, For they were still all fleeting. Then up she took her little crook, Determined for to find them; She found them indeed, but it made her heart bleed, For they'd left their tails behind them.",
        "filename": "bo_peep.mp3"
    },
    "jack_jill": {
        "title": "Jack and Jill",
        "text": "Jack and Jill went up the hill To fetch a pail of water. Jack fell down and broke his crown, And Jill came tumbling after. Up Jack got, and home did trot, As fast as he could caper, To old Dame Dob, who patched his nob With vinegar and brown paper. When Jill came in, how she did grin To see Jack's paper plaster; Mother vexed, did whip her next, For laughing at Jack's disaster.",
        "filename": "jack_jill.mp3"
    }
}

def generate_natural_voice_audio():
    """Generate more natural-sounding voice audio using Google Text-to-Speech"""
    results = {}
    
    # Make sure the audio directory exists
    os.makedirs("static/audio", exist_ok=True)
    
    # Process each story
    for story_id, story in stories.items():
        print(f"\n{'='*50}")
        print(f"Processing: {story['title']}")
        print(f"{'='*50}")
        
        output_path = os.path.join("static/audio", story["filename"])
        
        # Generate the audio with Google Text-to-Speech
        try:
            print(f"Generating natural voice audio for {story['title']}...")
            
            # Create gTTS object with slow=True for more child-friendly pace
            # Using 'com.au' TLD often gives a warmer, more engaging English voice
            tts = gTTS(text=story["text"], lang='en', tld='com.au', slow=False)
            
            # Save the audio directly as MP3
            tts.save(output_path)
            
            if os.path.exists(output_path):
                print(f"✓ Successfully generated natural voice audio for: {story['title']}")
                results[story_id] = {
                    "title": story["title"],
                    "status": "Generated",
                    "path": output_path
                }
            else:
                print(f"✗ Failed to generate audio for: {story['title']}")
                results[story_id] = {
                    "title": story["title"],
                    "status": "Failed",
                    "path": None
                }
                
        except Exception as e:
            print(f"✗ Error generating audio for {story['title']}: {e}")
            results[story_id] = {
                "title": story["title"],
                "status": "Error",
                "error": str(e)
            }
    
    # Write results to a JSON file
    with open('natural_voice_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    # Print summary
    print("\nNatural Voice Audio Generation Summary:")
    for story_id, info in results.items():
        status_icon = "✓" if info['status'] == 'Generated' else "✗"
        print(f"{status_icon} {info['title']}: {info['status']}")
    
    return results

def generate_single_story_audio(story_id):
    """Generate audio for a single story"""
    if story_id not in stories:
        print(f"Error: Story '{story_id}' not found!")
        return
    
    story = stories[story_id]
    print(f"\n{'='*50}")
    print(f"Processing: {story['title']}")
    print(f"{'='*50}")
    
    output_path = os.path.join("static/audio", story["filename"])
    
    # Generate the audio with Google Text-to-Speech
    try:
        print(f"Generating natural voice audio for {story['title']}...")
        
        # Create gTTS object with slow=True for more child-friendly pace
        # Using 'com.au' TLD often gives a warmer, more engaging English voice
        tts = gTTS(text=story["text"], lang='en', tld='com.au', slow=False)
        
        # Save the audio directly as MP3
        tts.save(output_path)
        
        if os.path.exists(output_path):
            print(f"✓ Successfully generated natural voice audio for: {story['title']}")
            return {
                "title": story["title"],
                "status": "Generated",
                "path": output_path
            }
        else:
            print(f"✗ Failed to generate audio for: {story['title']}")
            return {
                "title": story["title"],
                "status": "Failed",
                "path": None
            }
            
    except Exception as e:
        print(f"✗ Error generating audio for {story['title']}: {e}")
        return {
            "title": story["title"],
            "status": "Error",
            "error": str(e)
        }

if __name__ == "__main__":
    import sys
    
    # Make sure the audio directory exists
    os.makedirs("static/audio", exist_ok=True)
    
    # If a story ID is provided, generate just that one
    if len(sys.argv) > 1:
        story_id = sys.argv[1]
        if story_id in stories:
            print(f"Generating audio for: {stories[story_id]['title']}")
            result = generate_single_story_audio(story_id)
            print(f"Result: {result['status']}")
        else:
            print(f"Error: Unknown story ID '{story_id}'")
            print(f"Available stories: {', '.join(stories.keys())}")
    else:
        # Generate all stories if no specific story is requested
        print("Starting natural voice audio generation...")
        print("Available stories:")
        for idx, (story_id, story) in enumerate(stories.items(), 1):
            print(f"{idx}. {story_id}: {story['title']}")
        
        print("\nRun with a specific story ID to generate just one story.")
        print("Example: python generate_natural_voice.py little_fox")
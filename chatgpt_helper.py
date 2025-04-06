"""
ChatGPT integration for Children's Castle application.
This module provides helper functions to interact with OpenAI's GPT models.
"""

import os
import json
import logging
from openai import OpenAI

# Initialize OpenAI client
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    logging.warning("OpenAI API key not found in environment variables.")

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_kid_friendly_response(prompt, child_age=4, max_tokens=200):
    """
    Generate a kid-friendly response using GPT-4o
    
    Args:
        prompt (str): The child's question or prompt
        child_age (int): Age of the child to tailor response appropriately
        max_tokens (int): Maximum length of the response
        
    Returns:
        str: Kid-friendly response
    """
    try:
        # Build the system message with age-appropriate instructions
        system_message = f"""
        You are a friendly assistant named Castle Buddy for a {child_age}-year-old child named Menira.
        The child is using an app called "Children's Castle" and can ask you questions about anything.
        
        Follow these guidelines:
        - Use simple, clear language appropriate for a {child_age}-year-old
        - Keep responses brief (2-3 sentences) and engaging
        - Be enthusiastic, warm, and encouraging
        - Include occasional positive reinforcement
        - Answer only with facts appropriate for children
        - If you don't know, say "I'm not sure, but let's imagine..."
        - Never use complex words, sarcasm, or abstract concepts
        - Avoid any frightening, violent, or mature content
        - Don't discuss online safety, adult topics, or scary subjects
        - Always be supportive and kind
        - Include a simple follow-up question to engage the child further
        - If asked about science, animals, nature, space, or other educational topics, 
          provide simple, factual, and engaging information
        - Encourage curiosity and further learning
        - If the child seems confused or frustrated, offer reassurance
        - Remember to keep math simple and use visual examples when possible
        """
        
        # Handle common question types with special responses
        if prompt.lower().startswith("what is") or prompt.lower().startswith("who is") or prompt.lower().startswith("how does"):
            instruction = f"""
            The child is asking a knowledge question. Answer with:
            1. A simple, direct answer in 1-2 short sentences
            2. A fun fact related to the topic
            3. A follow-up question to encourage more conversation
            Keep everything at a {child_age}-year-old's understanding level.
            """
            system_message += instruction
        
        elif "why" in prompt.lower():
            instruction = f"""
            This is a 'why' question. Children love to understand causes and connections.
            Explain the concept using:
            1. A very simple cause-and-effect explanation
            2. A relatable example from their everyday life
            3. A gentle encouragement of their curiosity
            Make sure to avoid complex concepts that would confuse a {child_age}-year-old.
            """
            system_message += instruction
            
        elif any(word in prompt.lower() for word in ["dinosaur", "dinosaurs"]):
            instruction = f"""
            The child is asking about dinosaurs, a favorite topic! Keep facts age-appropriate and easy to visualize.
            Focus on interesting, memorable facts about dinosaur appearance, habits, or size.
            Compare dinosaur sizes to familiar objects like houses, cars, or elephants.
            Avoid scary aspects like violent hunting or extinction details if the child is under 7.
            """
            system_message += instruction
            
        elif any(word in prompt.lower() for word in ["space", "planet", "star", "rocket", "moon", "astronaut"]):
            instruction = f"""
            The child is asking about space! Focus on amazing, awe-inspiring facts about space
            that are easy for a {child_age}-year-old to grasp. Use comparisons to familiar objects
            when discussing sizes or distances. Make the universe sound wondrous rather than scary.
            """
            system_message += instruction
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating kid-friendly response: {e}")
        return "I'm having a little nap right now. Can we talk later? You can ask me again in a few minutes, and I'll try my best to answer your question!"

def generate_interactive_story(story_prompt, child_age=4, include_questions=True):
    """
    Generate an interactive story with optional questions for the child
    
    Args:
        story_prompt (str): Basic prompt for the story (e.g., "a story about a brave fox")
        child_age (int): Age of the child to tailor content appropriately
        include_questions (bool): Whether to include interactive questions
        
    Returns:
        dict: Story content with pages and optional questions
    """
    try:
        # Build the system message with age-appropriate instructions
        system_message = f"""
        You are a creative storyteller for a {child_age}-year-old child.
        Create a short, engaging, and educational story based on the child's prompt.
        
        Follow these guidelines:
        - Create a story with a title and 3-5 pages
        - Use simple, clear language appropriate for a {child_age}-year-old
        - Include a gentle moral or lesson
        - Keep the story positive, friendly, and engaging
        - Include a main character the child can relate to
        - If requested, add a simple question at the end of some pages to engage the child
        
        Return the story as a JSON object with this structure:
        {{
            "title": "Story Title",
            "pages": [
                {{
                    "content": "Page 1 text...",
                    "question": "Optional question for the child?"
                }},
                {{
                    "content": "Page 2 text...",
                    "question": null
                }},
                ...
            ]
        }}
        """
        
        # Create the user prompt with the story request
        user_prompt = f"Please create a short children's story about {story_prompt}."
        if include_questions:
            user_prompt += " Include some simple questions to make it interactive."
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=1200,
            temperature=0.8,
            response_format={"type": "json_object"}
        )
        
        # Parse the JSON response
        story_content = json.loads(response.choices[0].message.content)
        
        # Ensure the story has the expected structure
        if "title" not in story_content or "pages" not in story_content:
            raise ValueError("Story response is missing required structure")
        
        return story_content
    except Exception as e:
        logging.error(f"Error generating interactive story: {e}")
        # Return a simple backup story
        return {
            "title": "The Adventure of the Curious Child",
            "pages": [
                {
                    "content": "Once upon a time, there was a curious child who loved to explore the castle.",
                    "question": "What do you think the child found in the castle?"
                },
                {
                    "content": "The child found magical friends who taught them about kindness and friendship.",
                    "question": None
                },
                {
                    "content": "Together, they had wonderful adventures and learned important lessons. The End!",
                    "question": "What was your favorite part of the story?"
                }
            ]
        }

def answer_story_question(story_context, question, child_age=4):
    """
    Generate an encouraging response to a child's answer to a story question
    
    Args:
        story_context (str): The current story context/page
        question (str): The question asked
        child_age (int): Age of the child
        
    Returns:
        str: Encouraging response to the child's answer
    """
    try:
        # Build the system message with age-appropriate instructions
        system_message = f"""
        You are responding to a {child_age}-year-old child's answer to a story question.
        
        Follow these guidelines:
        - Be enthusiastic, warm, and very encouraging
        - Use simple language appropriate for a {child_age}-year-old
        - Acknowledge their answer positively regardless of what they said
        - Extend their thinking with a follow-up comment
        - Keep responses brief (1-2 sentences)
        - Never criticize or correct their answer
        - Be supportive, friendly, and kind
        """
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Story context: {story_context}\nQuestion asked: {question}\nPlease provide an encouraging response to whatever the child answered."}
            ],
            max_tokens=100,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating answer response: {e}")
        return "That's a wonderful answer! You're so creative and smart!"

def generate_learning_tip(topic, child_age=4):
    """
    Generate a short learning tip on a specific topic for parents
    
    Args:
        topic (str): The learning topic (e.g., "reading", "numbers")
        child_age (int): Age of the child
        
    Returns:
        str: A short learning tip for parents
    """
    try:
        # Build the system message with age-appropriate instructions
        system_message = f"""
        You are an expert in early childhood education providing tips to parents of a {child_age}-year-old child.
        
        Follow these guidelines:
        - Provide practical, evidence-based advice
        - Keep tips concise (2-3 sentences)
        - Focus on activities that are developmentally appropriate
        - Suggest activities that are easy to implement at home
        - Emphasize play-based and enjoyable learning
        - Include why the activity helps development
        """
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": f"Please provide a short, practical learning tip for parents about helping their {child_age}-year-old child learn about {topic}."}
            ],
            max_tokens=150,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating learning tip: {e}")
        return f"Try incorporating {topic} into everyday activities through play. Children learn best when they're having fun and don't even realize they're learning!"
        
def generate_parent_advice(question, child_age=4):
    """
    Generate a helpful response to a parent's question about their child, the app, or parenting
    
    Args:
        question (str): The parent's question
        child_age (int): Age of the child
        
    Returns:
        str: A helpful response for the parent
    """
    try:
        # Build the system message for the parent assistant
        system_message = f"""
        You are a helpful assistant for parents using the Children's Castle app.
        
        Follow these guidelines:
        - Provide helpful, supportive answers to parents' questions
        - Be empathetic and understanding
        - Focus on practical advice that's easy to implement
        - Keep answers concise but thorough (3-5 sentences)
        - Reference Children's Castle app features when relevant
        - Offer evidence-based parenting advice
        - Tailor advice to a parent with a {child_age}-year-old child
        - Never judge parenting styles or choices
        - Be encouraging and positive
        """
        
        # Preprocess the question to add context and improve responses
        enhanced_question = f"As a parent of a {child_age}-year-old using the Children's Castle app, I'd like advice about: {question}"
        
        # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
        # do not change this unless explicitly requested by the user
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": enhanced_question}
            ],
            max_tokens=250,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating parent advice: {e}")
        return "I recommend focusing on your child's interests and building learning opportunities around them. The Children's Castle app offers personalized recommendations based on your child's engagement patterns that you can find in the Activity Summaries section."
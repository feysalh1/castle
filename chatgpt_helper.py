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

def generate_kid_friendly_response(prompt, child_age=4, max_tokens=150):
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
        You are a friendly assistant for a {child_age}-year-old child named Menira.
        The child is using an app called "Children's Castle" and can ask you questions.
        
        Follow these guidelines:
        - Use simple, clear language appropriate for a {child_age}-year-old
        - Keep responses brief and engaging
        - Be enthusiastic, warm, and encouraging
        - Include occasional positive reinforcement
        - Answer only with facts appropriate for children
        - If you don't know, say "I'm not sure, but let's imagine..."
        - Never use complex words, sarcasm, or abstract concepts
        - Avoid any frightening, violent, or mature content
        - Don't discuss online safety, adult topics, or scary subjects
        - Always be supportive and kind
        """
        
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
        return "I'm having a little nap right now. Can we talk later?"

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
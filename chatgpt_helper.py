"""
ChatGPT integration for Children's Castle application.
This module provides helper functions to interact with OpenAI's GPT models.
"""
import json
import os
import logging
from openai import OpenAI

# Initialize OpenAI client with API key from environment variables
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
        # Create system message to ensure kid-friendly responses
        system_message = f"""
        You are a kind, friendly assistant for a {child_age}-year-old child named Menira.
        Always respond in a way that's:
        - Easy to understand for a {child_age}-year-old
        - Educational but fun
        - Positive and encouraging
        - Safe and appropriate for children
        - Brief (2-3 sentences maximum)
        - Never scary or using complex words
        
        If asked about a topic that's not appropriate for children, 
        gently redirect to a child-friendly topic.
        """
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o", # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Error generating kid-friendly response: {e}")
        return "I'm sorry, I'm having trouble thinking right now. Let's try again later!"

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
        # Create system message for story generation
        system_message = f"""
        You are a children's storyteller creating an interactive story for a {child_age}-year-old child.
        Create a short story that is:
        - Engaging and imaginative
        - Appropriate for a {child_age}-year-old
        - Educational but fun
        - 3-5 paragraphs total
        - Divided into 3 pages (sections)
        
        If include_questions is True, add one simple question at the end of each page
        that encourages the child to think about the story.
        
        Return the story in JSON format with this structure:
        {{
            "title": "Story title",
            "pages": [
                {{
                    "content": "Page 1 content...",
                    "question": "Question about page 1?" (only if include_questions is True)
                }},
                // more pages...
            ]
        }}
        """
        
        # Format the user prompt
        user_prompt = f"Generate a kid-friendly story about {story_prompt}. " + \
                     f"include_questions={include_questions}"
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o", # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.8
        )
        
        # Parse the JSON response
        story_data = json.loads(response.choices[0].message.content)
        return story_data
    
    except Exception as e:
        logger.error(f"Error generating interactive story: {e}")
        return {
            "title": "Story Adventure",
            "pages": [
                {
                    "content": "I'm having trouble creating a story right now. Let's try again later!"
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
        # Create system message for encouraging responses
        system_message = f"""
        You are a supportive storyteller for a {child_age}-year-old child.
        Based on the story context and question, provide an encouraging response
        to whatever answer the child gives.
        
        Your response should:
        - Be positive and supportive
        - Validate the child's thinking
        - Add a small educational insight if possible
        - Be brief (1-2 sentences)
        - Use simple language appropriate for a {child_age}-year-old
        """
        
        # Format the user prompt with context
        user_prompt = f"""
        Story context: {story_context}
        
        Question asked: {question}
        
        The child has given an answer. Provide an encouraging response:
        """
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o", # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=100,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Error generating answer to story question: {e}")
        return "That's wonderful thinking! You're doing great!"

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
        # Create system message for parent tips
        system_message = f"""
        You are an early childhood education expert providing brief tips to parents
        of a {child_age}-year-old child.
        
        Create a helpful tip that is:
        - Practical and actionable
        - Based on child development research
        - Specific to the requested topic
        - Brief (2-3 sentences maximum)
        - Encouraging to parents
        """
        
        # Format the user prompt
        user_prompt = f"Provide a quick tip for parents to help their {child_age}-year-old child learn about {topic}."
        
        # Call the OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o", # the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=120,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        logger.error(f"Error generating learning tip: {e}")
        return "Engage your child in everyday conversations about this topic, asking open-ended questions and building on their responses."
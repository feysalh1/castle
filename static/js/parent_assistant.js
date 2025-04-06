/**
 * Parent AI Assistant Chat Functionality
 * Handles the chat interface for parents to ask questions about their child's learning journey
 */

document.addEventListener('DOMContentLoaded', function() {
    // Get the chat UI elements
    const chatBox = document.getElementById('chat-box');
    const chatMessages = document.querySelector('.chat-messages');
    const parentQuestion = document.getElementById('parent-question');
    const sendQuestionBtn = document.getElementById('send-question');
    const exampleQuestions = document.querySelectorAll('.example-question');
    
    // Function to add a message to the chat
    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        messageDiv.textContent = text;
        chatMessages.appendChild(messageDiv);
        
        // Scroll to the bottom of the chat
        chatBox.scrollTop = chatBox.scrollHeight;
    }
    
    // Function to send a question to the AI assistant
    function sendQuestion(question) {
        // Add the user's question to the chat
        addMessage(question, 'user');
        
        // Show loading indicator
        const loadingMessage = document.createElement('div');
        loadingMessage.className = 'message assistant';
        loadingMessage.innerHTML = '<i>Thinking...</i>';
        chatMessages.appendChild(loadingMessage);
        
        // Send the question to the backend
        fetch('/api/parent/tip', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                question: question,
                child_age: 4 // Default age, can be dynamically set based on child's profile
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Remove the loading indicator
            chatMessages.removeChild(loadingMessage);
            
            // Add the AI response to the chat
            addMessage(data.response, 'assistant');
        })
        .catch(error => {
            // Remove the loading indicator
            chatMessages.removeChild(loadingMessage);
            
            console.error('Error:', error);
            addMessage('Sorry, there was an error processing your request. Please try again.', 'system');
        });
    }
    
    // Event listener for the send button
    sendQuestionBtn.addEventListener('click', function() {
        const question = parentQuestion.value.trim();
        if (question) {
            sendQuestion(question);
            parentQuestion.value = ''; // Clear the input field
            parentQuestion.focus();
        }
    });
    
    // Event listener for the Enter key in the input field
    parentQuestion.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const question = parentQuestion.value.trim();
            if (question) {
                sendQuestion(question);
                parentQuestion.value = ''; // Clear the input field
            }
        }
    });
    
    // Event listeners for example questions
    exampleQuestions.forEach(question => {
        question.addEventListener('click', function(e) {
            e.preventDefault();
            const questionText = this.textContent;
            parentQuestion.value = questionText;
            sendQuestion(questionText);
            parentQuestion.value = ''; // Clear the input field
        });
    });
});

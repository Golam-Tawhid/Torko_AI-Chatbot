import os
import requests
from datetime import datetime
import uuid
import logging
from .models import Message
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

class ChatService:
    def __init__(self):
        self.model = "gemini-2.0-flash"  # Using Gemini model
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"
        logger.debug("ChatService initialized")

    def process_message(self, message, session_id):
        try:
            # Save user message
            user_message = Message(message, 'user', session_id)
            Message.save(user_message)

            # Get chat history for context
            history = Message.get_by_session(session_id)
            context = self._format_context(history)

            # Get AI response
            response = self._get_ai_response(context, message)

            # Save AI response
            ai_message = Message(response, 'assistant', session_id)
            Message.save(ai_message)

            return {
                'response': response,
                'session_id': session_id
            }
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            raise

    def get_chat_history(self, session_id):
        try:
            messages = Message.get_by_session(session_id)
            return [{
                'content': msg['content'],
                'sender': msg['sender'],
                'timestamp': msg['timestamp']
            } for msg in messages]
        except Exception as e:
            logger.error(f"Error getting chat history: {str(e)}")
            raise

    def create_session(self):
        try:
            session_id = str(uuid.uuid4())
            logger.debug(f"Generated new session ID: {session_id}")
            return session_id
        except Exception as e:
            logger.error(f"Error creating session: {str(e)}")
            raise

    def _format_context(self, history):
        try:
            formatted_history = []
            for msg in history:
                role = 'user' if msg['sender'] == 'user' else 'assistant'
                formatted_history.append({
                    'role': role,
                    'content': msg['content']
                })
            return formatted_history
        except Exception as e:
            logger.error(f"Error formatting context: {str(e)}")
            raise

    def _get_ai_response(self, context, message):
        try:
            # Format the conversation for Gemini API
            conversation_text = "You are a helpful assistant.\n\n"
            for msg in context:
                role = "User" if msg['role'] == 'user' else "Assistant"
                conversation_text += f"{role}: {msg['content']}\n"
            conversation_text += f"User: {message}\nAssistant:"
            
            # Prepare the request payload for Gemini API
            payload = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": conversation_text
                            }
                        ]
                    }
                ]
            }
            
            headers = {
                'Content-Type': 'application/json',
                'X-goog-api-key': self.api_key
            }
            
            # Make the API call
            response = requests.post(self.api_url, json=payload, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            if 'candidates' in data and len(data['candidates']) > 0:
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return "I apologize, but I couldn't generate a response at this time."
                
        except Exception as e:
            logger.error(f"Error getting AI response: {str(e)}")
            # Fallback response for quota/API issues
            if "quota" in str(e).lower() or "insufficient_quota" in str(e):
                return f"I'm a chatbot assistant. You said: '{message}'. I would normally provide an AI-generated response, but there's currently an API quota issue. Please check your API key and try again."
            else:
                return f"I apologize, but I'm experiencing technical difficulties. Your message was: '{message}'. Please try again later."

chat_service = ChatService() 
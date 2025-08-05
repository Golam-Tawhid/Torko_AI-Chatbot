import os
import requests
from datetime import datetime
import uuid
import logging
import time
import random
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
        self.last_request_time = 0
        self.min_request_interval = 1.0  # Minimum 1 second between requests
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
        # Rate limiting - ensure minimum interval between requests
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last_request
            logger.debug(f"Rate limiting: sleeping for {sleep_time:.2f} seconds")
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
        
        max_retries = 3
        base_delay = 1  # Base delay in seconds
        
        for attempt in range(max_retries):
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
                
                # Make the API call with timeout
                response = requests.post(
                    self.api_url, 
                    json=payload, 
                    headers=headers,
                    timeout=30  # 30 second timeout
                )
                response.raise_for_status()
                
                data = response.json()
                if 'candidates' in data and len(data['candidates']) > 0:
                    ai_response = data['candidates'][0]['content']['parts'][0]['text']
                    
                    # Check if the AI is returning error messages indicating service issues
                    error_indicators = [
                        "experiencing difficulties",
                        "cannot respond to your request at this time",
                        "i apologize for the inconvenience",
                        "service unavailable",
                        "temporarily unavailable",
                        "technical difficulties"
                    ]
                    
                    if any(indicator in ai_response.lower() for indicator in error_indicators):
                        logger.warning(f"AI service returned error message: {ai_response}")
                        # Treat this as a service error and use fallback
                        if attempt < max_retries - 1:
                            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                            logger.info(f"AI service error detected, retrying in {delay:.2f} seconds...")
                            time.sleep(delay)
                            continue
                        else:
                            # Last attempt, use fallback
                            return self._get_fallback_response(message)
                    
                    return ai_response
                else:
                    logger.warning("No candidates in API response")
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        logger.info(f"No candidates in response, retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        continue
                    else:
                        return self._get_fallback_response(message)
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"API request error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                
                # Check if it's a retriable error
                if hasattr(e, 'response') and e.response is not None:
                    status_code = e.response.status_code
                    if status_code in [429, 500, 502, 503, 504]:  # Retriable errors
                        if attempt < max_retries - 1:  # Don't sleep on last attempt
                            # Exponential backoff with jitter
                            delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                            logger.info(f"Retrying in {delay:.2f} seconds...")
                            time.sleep(delay)
                            continue
                    else:
                        # Non-retriable error, break immediately
                        break
                else:
                    # Connection error, retry
                    if attempt < max_retries - 1:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        logger.info(f"Retrying in {delay:.2f} seconds...")
                        time.sleep(delay)
                        continue
                
            except Exception as e:
                logger.error(f"Unexpected error (attempt {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.info(f"Retrying in {delay:.2f} seconds...")
                    time.sleep(delay)
                    continue
        
        # All retries failed, return fallback response
        logger.error("All retry attempts failed for AI response")
        return self._get_fallback_response(message)

    def _get_fallback_response(self, message):
        """Generate a fallback response when AI service is unavailable"""
        message_lower = message.lower()
        
        # Simple keyword-based responses for common queries
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'greetings']):
            return "Hello! I'm experiencing some connectivity issues with my AI service, but I'm here to help. Please try your question again in a moment."
        
        elif any(word in message_lower for word in ['what', 'explain', 'define', 'how', 'why', 'when', 'where']):
            return f"I understand you're looking for an explanation or information about something. I'm currently experiencing connectivity issues with my AI service. Your question was: '{message}'. Please try again in a moment for a detailed and comprehensive response!"
        
        elif any(word in message_lower for word in ['help', 'support', 'assist']):
            return "I'm here to help! I'm currently experiencing some technical difficulties with my AI service, but I should be back to full functionality soon. Please try your question again in a moment."
        
        else:
            return f"I received your message: '{message}'. I'm currently experiencing connectivity issues with my AI service, but I should be able to provide a proper response if you try again in a moment. Thank you for your patience!"

chat_service = ChatService() 
from flask import Blueprint, request, jsonify
from .services import chat_service
from .models import Message
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/chat', methods=['POST'])
def chat():
    try:
        logger.debug("Received chat request")
        data = request.json
        logger.debug(f"Request data: {data}")
        
        message = data.get('message')
        session_id = data.get('session_id')
        
        if not message:
            logger.warning("No message provided in request")
            return jsonify({'error': 'Message is required'}), 400
        
        logger.debug(f"Processing message: {message} for session: {session_id}")
        response = chat_service.process_message(message, session_id)
        logger.debug(f"Response: {response}")
        return jsonify(response)
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/history', methods=['GET'])
def get_history():
    session_id = request.args.get('session_id')
    try:
        history = chat_service.get_chat_history(session_id)
        return jsonify(history)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@chat_bp.route('/session', methods=['POST'])
def create_session():
    try:
        logger.debug("Creating new session")
        session_id = chat_service.create_session()
        logger.debug(f"Session created with ID: {session_id}")
        return jsonify({'session_id': session_id})
    except Exception as e:
        logger.error(f"Error creating session: {str(e)}")
        return jsonify({'error': str(e)}), 500 
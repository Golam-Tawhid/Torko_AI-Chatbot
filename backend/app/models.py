from datetime import datetime
from .database import get_db

class Message:
    def __init__(self, content, sender, session_id):
        self.content = content
        self.sender = sender
        self.session_id = session_id
        self.timestamp = datetime.utcnow()

    def to_dict(self):
        return {
            'content': self.content,
            'sender': self.sender,
            'session_id': self.session_id,
            'timestamp': self.timestamp
        }

    @staticmethod
    def save(message):
        db = get_db()
        db.messages.insert_one(message.to_dict())

    @staticmethod
    def get_by_session(session_id):
        db = get_db()
        messages = db.messages.find({'session_id': session_id}).sort('timestamp', 1)
        return [msg for msg in messages] 
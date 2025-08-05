from flask import Flask, send_from_directory, send_file
from flask_cors import CORS
from .routes import chat_bp
from .database import init_db
import os

def create_app():
    app = Flask(__name__, static_folder='../../frontend/build')
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["*"],  # Allow all origins for production
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Initialize database
    init_db()
    
    # Register blueprints
    app.register_blueprint(chat_bp, url_prefix='/api')
    
    # Serve React static files
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react_app(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')
    
    return app 
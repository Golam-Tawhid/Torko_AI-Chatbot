from pymongo import MongoClient
from datetime import datetime
import os
import logging
from dotenv import load_dotenv
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

client = None
db = None

def init_db():
    global client, db
    try:
        mongodb_uri = os.getenv('MONGODB_URI')
        logger.debug(f"Connecting to MongoDB at: {mongodb_uri}")
        
        # Parse the URI to get the database name
        parsed_uri = urlparse(mongodb_uri)
        db_name = parsed_uri.path[1:] if parsed_uri.path else 'chatbot'
        
        # Configure connection settings
        if mongodb_uri.startswith('mongodb+srv://'):
            # Cloud MongoDB settings
            client = MongoClient(
                mongodb_uri,
                tls=True,
                tlsAllowInvalidCertificates=True,
                retryWrites=True,
                w='majority',
                serverSelectionTimeoutMS=30000,
                connectTimeoutMS=30000,
                socketTimeoutMS=30000
            )
        else:
            # Local MongoDB settings
            client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,
                connectTimeoutMS=5000,
                socketTimeoutMS=5000
            )
        
        # Test the connection
        client.server_info()
        db = client[db_name]
        logger.debug(f"Successfully connected to MongoDB database: {db_name}")
    except Exception as e:
        logger.error(f"Error connecting to MongoDB: {str(e)}")
        raise

def get_db():
    if db is None:
        init_db()
    return db

def close_db():
    if client is not None:
        try:
            client.close()
            logger.debug("MongoDB connection closed")
        except Exception as e:
            logger.error(f"Error closing MongoDB connection: {str(e)}")
            raise 
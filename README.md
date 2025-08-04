# Torko - AI-Powered Chatbot 🚀

A beautifully designed, modern chatbot implementation using React, Flask, MongoDB, and Google Gemini AI with stunning animations, dark theme support, and enhanced user experience.

## ✨ Features

### 🎨 Enhanced UI/UX

- **Modern Glass Morphism Design**: Beautiful glassmorphism effects with backdrop blur
- **Dynamic Gradient Backgrounds**: Animated gradient backgrounds with floating particles
- **Dark/Light Theme Toggle**: Seamless theme switching with persistent preferences
- **Smooth Animations**: Elegant slide-in animations for messages and UI components
- **Loading Screen**: Professional loading screen with animated branding
- **Interactive Hover Effects**: Engaging animations throughout the interface

### 💬 Chat Experience

- **Real-time chat interface** with typing indicators
- **AI-powered responses** using Google Gemini 2.0 Flash model
- **Persistent chat history** with MongoDB storage
- **User session management** with unique session IDs
- **Message avatars** with emoji representations
- **Auto-scroll** to new messages with smooth animation
- **Markdown support** for rich text formatting in responses

### ⌨️ Keyboard Shortcuts

- **Ctrl/Cmd + /**: Toggle keyboard shortcuts panel
- **Enter**: Send message
- **Ctrl/Cmd + K**: Focus input field
- **Escape**: Close modals/panels

### 🎵 Audio Feedback

- **Message sent/received sounds** with Web Audio API
- **Error notification sounds** for better UX
- **Configurable audio preferences**

## 🛠️ Tech Stack

- **Frontend**: React 19.1.0 with modern hooks and effects
- **Backend**: Flask 3.0.2 with CORS support
- **Database**: MongoDB with PyMongo 4.6.1
- **AI**: Google Gemini 2.0 Flash model
- **Styling**: Modern CSS with animations and glassmorphism
- **Additional**: React Markdown, Web Audio API, UUID sessions

## 📁 Project Structure

```
Torko(AI-Chatbot)/
├── frontend/                    # React frontend application
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Chat.js        # Main chat interface
│   │   │   ├── Chat.css       # Chat styling
│   │   │   ├── ThemeToggle.js # Dark/light theme switcher
│   │   │   ├── KeyboardShortcuts.js # Keyboard shortcuts panel
│   │   │   └── LoadingScreen.js # Animated loading screen
│   │   ├── utils/
│   │   │   └── soundManager.js # Audio feedback system
│   │   ├── App.js             # Main application component
│   │   └── App.css            # Global styles and animations
│   ├── package.json           # Frontend dependencies
│   ├── FEATURES.md           # Detailed feature documentation
│   └── README.md             # Create React App documentation
├── backend/                   # Flask backend application
│   ├── app/
│   │   ├── __init__.py       # Flask app factory
│   │   ├── routes.py         # API endpoints
│   │   ├── services.py       # Business logic and AI integration
│   │   ├── models.py         # Data models
│   │   └── database.py       # MongoDB connection and configuration
│   ├── run.py               # Application entry point
│   └── .env                 # Environment variables (not in git)
├── requirements.txt         # Python dependencies
└── README.md               # Project documentation
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8+ with pip
- Node.js 16+ with npm
- MongoDB (local or cloud instance)
- Google Gemini API key

### Backend Setup

1. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install Python dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
   Create a `.env` file in the backend directory with:

```env
MONGODB_URI=mongodb://localhost:27017/chatbot
GEMINI_API_KEY=your_gemini_api_key_here
FLASK_ENV=development
FLASK_APP=run.py
```

4. **Start the backend server:**

```bash
cd backend
python run.py
```

The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies:**

```bash
cd frontend
npm install
```

2. **Start the development server:**

```bash
npm start
```

The frontend will run on `http://localhost:3000`

### 🗄️ Database Setup

- **Local MongoDB**: Install MongoDB locally and ensure it's running on port 27017
- **MongoDB Atlas**: Use a cloud MongoDB URI in your `.env` file
- The application will automatically create the required collections

## 🔧 Environment Variables

| Variable         | Description                            | Example                             |
| ---------------- | -------------------------------------- | ----------------------------------- |
| `MONGODB_URI`    | MongoDB connection string              | `mongodb://localhost:27017/chatbot` |
| `GEMINI_API_KEY` | Google Gemini API key for AI responses | `AIzaSy...`                         |
| `FLASK_ENV`      | Flask environment setting              | `development`                       |
| `FLASK_APP`      | Flask application entry point          | `run.py`                            |

## 🌐 API Endpoints

| Method | Endpoint       | Description                          | Parameters                 |
| ------ | -------------- | ------------------------------------ | -------------------------- |
| `POST` | `/api/chat`    | Send message and receive AI response | `message`, `session_id`    |
| `GET`  | `/api/history` | Retrieve chat history for session    | `session_id` (query param) |
| `POST` | `/api/session` | Create a new chat session            | None                       |

### Example API Usage

```javascript
// Create a new session
const sessionResponse = await fetch("http://localhost:5000/api/session", {
  method: "POST",
});
const { session_id } = await sessionResponse.json();

// Send a message
const chatResponse = await fetch("http://localhost:5000/api/chat", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    message: "Hello, Torko!",
    session_id: session_id,
  }),
});
const { response } = await chatResponse.json();
```

## 🎨 Features Showcase

### Frontend Components

- **Chat.js**: Main chat interface with real-time messaging
- **ThemeToggle.js**: Dark/light theme switcher with smooth transitions
- **KeyboardShortcuts.js**: Helpful keyboard shortcuts panel
- **LoadingScreen.js**: Beautiful animated loading experience
- **soundManager.js**: Audio feedback system using Web Audio API

### Backend Services

- **ChatService**: Handles message processing and AI integration
- **Message Model**: MongoDB document structure for chat messages
- **Database**: MongoDB connection with cloud and local support
- **Routes**: RESTful API endpoints with CORS configuration

## 🔍 Dependencies

### Frontend (React)

```json
{
  "react": "^19.1.0",
  "react-dom": "^19.1.0",
  "react-markdown": "^10.1.0",
  "react-scripts": "5.0.1"
}
```

### Backend (Flask)

```txt
flask==3.0.2
flask-cors==4.0.0
pymongo==4.6.1
python-dotenv==1.0.1
requests==2.31.0
gunicorn==21.2.0
```

## 🚀 Getting Started

1. **Clone the repository**
2. **Set up the backend** (follow Backend Setup above)
3. **Set up the frontend** (follow Frontend Setup above)
4. **Get your Gemini API key** from [Google AI Studio](https://makersuite.google.com/app/apikey)
5. **Configure your environment variables**
6. **Start both servers** and enjoy chatting with Torko!

## 🎯 Usage Tips

- Use **Ctrl/Cmd + /** to see all keyboard shortcuts
- Toggle between **dark and light themes** using the switch in the top-right
- Enable **audio feedback** for a more immersive experience
- Chat history is **automatically saved** and restored per session

## 🐛 Troubleshooting

### Common Issues

1. **Backend not starting**: Check that MongoDB is running and environment variables are set
2. **Frontend compilation errors**: Ensure Node.js version is 16+ and dependencies are installed
3. **AI responses not working**: Verify your Gemini API key is valid and has quota remaining
4. **CORS errors**: Ensure backend is running on port 5000 and frontend on port 3000

### Development Notes

- The app uses **Google Gemini 2.0 Flash** model for AI responses
- **Session-based chat history** allows multiple concurrent conversations
- **Glassmorphism design** requires modern browsers with backdrop-filter support
- **Audio features** may require user interaction to enable in some browsers

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📞 Support

For support and questions:

- Check the `/frontend/FEATURES.md` for detailed frontend architecture and design documentation
- Review the troubleshooting section above
- Open an issue on GitHub

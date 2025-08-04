import React, { useState, useEffect, useRef, useCallback } from "react";
import ReactMarkdown from "react-markdown";
import LoadingScreen from "./LoadingScreen";
import soundManager from "../utils/soundManager";
import "./Chat.css";

const Chat = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sessionId, setSessionId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const [isInitializing, setIsInitializing] = useState(true);
  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  const scrollToBottom = useCallback(() => {
    // Only scroll if element exists and avoid unnecessary operations
    const messagesContainer = messagesEndRef.current?.parentElement;
    if (messagesContainer) {
      const { scrollTop, scrollHeight, clientHeight } = messagesContainer;
      // Only scroll if not already at bottom
      if (scrollHeight - scrollTop - clientHeight > 5) {
        messagesContainer.scrollTop = scrollHeight;
      }
    }
  }, []);

  useEffect(() => {
    // Show loading screen for 2 seconds then create session
    setTimeout(() => {
      createNewSession();
      setTimeout(() => {
        setIsInitializing(false);
      }, 1000);
    }, 2000);
  }, []);

  useEffect(() => {
    scrollToBottom();
  }, [messages, scrollToBottom]);

  useEffect(() => {
    const handleGlobalKeyDown = (event) => {
      // Focus input with Ctrl/Cmd + K
      if ((event.ctrlKey || event.metaKey) && event.key === "k") {
        event.preventDefault();
        inputRef.current?.focus();
      }

      // Clear chat with Ctrl/Cmd + L (future feature)
      if ((event.ctrlKey || event.metaKey) && event.key === "l") {
        event.preventDefault();
        // setMessages([]); // Uncomment to enable clear chat
        console.log("Clear chat shortcut pressed");
      }
    };

    document.addEventListener("keydown", handleGlobalKeyDown);
    return () => document.removeEventListener("keydown", handleGlobalKeyDown);
  }, []);

  const createNewSession = async () => {
    try {
      console.log("Creating new session...");
      const response = await fetch("http://localhost:5000/api/session", {
        method: "POST",
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      console.log("Session created:", data);
      setSessionId(data.session_id);
    } catch (error) {
      console.error("Error creating session:", error);
      setError("Failed to create chat session. Please try again.");
    }
  };

  const handleInputKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      sendMessage(event);
    }
  };

  const sendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || !sessionId) {
      console.log("No input or session ID");
      return;
    }

    const userMessage = {
      id: Date.now() + Math.random(), // Add unique ID
      content: input,
      sender: "user",
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);
    setIsTyping(true);
    setError(null);

    // Play send sound
    soundManager.playMessageSent();

    try {
      console.log("Sending message:", input);
      const response = await fetch("http://localhost:5000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: input,
          session_id: sessionId,
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Received response:", data);

      // Simulate typing delay for better UX
      setTimeout(() => {
        const botMessage = {
          id: Date.now() + Math.random(), // Add unique ID
          content: data.response,
          sender: "assistant",
          timestamp: new Date().toISOString(),
        };

        setMessages((prev) => [...prev, botMessage]);
        setIsTyping(false);

        // Play receive sound
        soundManager.playMessageReceived();
      }, 1000);
    } catch (error) {
      console.error("Error sending message:", error);
      setError("Failed to send message. Please try again.");
      setIsTyping(false);

      // Play error sound
      soundManager.playError();
    } finally {
      setIsLoading(false);
    }
  };

  const TypingIndicator = React.memo(() => (
    <div className="message bot-message typing-indicator">
      <div className="message-content">
        <div className="typing-dots">
          <span></span>
          <span></span>
          <span></span>
        </div>
        <span className="typing-text">Torko is thinking...</span>
      </div>
    </div>
  ));

  const MessageBubble = React.memo(({ message }) => (
    <div
      className={`message ${
        message.sender === "user" ? "user-message" : "bot-message"
      }`}
    >
      {message.sender === "assistant" && (
        <div className="bot-avatar">
          <span>🤖</span>
        </div>
      )}
      <div className="message-content">
        {message.sender === "user" ? (
          message.content
        ) : (
          <ReactMarkdown>{message.content}</ReactMarkdown>
        )}
      </div>
      <div className="message-timestamp">
        {new Date(message.timestamp).toLocaleTimeString()}
      </div>
      {message.sender === "user" && (
        <div className="user-avatar">
          <span>👤</span>
        </div>
      )}
    </div>
  ));

  return (
    <>
      {isInitializing && <LoadingScreen />}
      <div className="chat-container">
        {error && (
          <div className="error-message">
            <span>⚠️</span>
            {error}
            <button onClick={() => setError(null)} className="error-close">
              ×
            </button>
          </div>
        )}

        <div className="messages-container">
          <div className="welcome-message">
            <div className="welcome-icon">👋</div>
            <h3>Hello! I'm Torko</h3>
            <p>How can I help you today?</p>
          </div>

          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}

          {isTyping && <TypingIndicator />}
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendMessage} className="input-form">
          <div className="input-container">
            <input
              ref={inputRef}
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleInputKeyDown}
              placeholder="Type your message..."
              disabled={isLoading}
              className="chat-input"
            />
            <button
              type="submit"
              disabled={isLoading || !input.trim()}
              className="send-button"
            >
              {isLoading ? (
                <div className="loading-spinner"></div>
              ) : (
                <span>🚀</span>
              )}
            </button>
          </div>
        </form>
      </div>
    </>
  );
};

export default Chat;

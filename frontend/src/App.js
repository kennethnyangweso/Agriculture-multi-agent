import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// Configure API base URL - change this to your deployed backend URL later
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Message component
function Message({ message, isUser }) {
  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-avatar">
        {isUser ? '👤' : '🌾'}
      </div>
      <div className="message-content">
        <div className="message-text">
          {message}
        </div>
      </div>
    </div>
  );
}

function App() {
  const [messages, setMessages] = useState([
    {
      text: "👋 **Hello!** I'm your AI agricultural assistant for Kenya.\n\nI can help you with:\n- 🌾 Crop diseases and treatments\n- 🐄 Livestock health and management\n- 🐔 Poultry care and disease control\n- 📈 Farming advice and market info\n\n**Ask me anything about agriculture!**",
      isUser: false
    }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setMessages(prev => [...prev, { text: userMessage, isUser: true }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/query`, {
        question: userMessage,
        language: 'auto'
      });

      if (response.data.success) {
        setMessages(prev => [...prev, {
          text: response.data.answer,
          isUser: false
        }]);
      } else {
        setMessages(prev => [...prev, {
          text: `❌ Sorry, I couldn't process your question: ${response.data.error || 'Unknown error'}`,
          isUser: false
        }]);
      }
    } catch (error) {
      console.error('Error:', error);
      setMessages(prev => [...prev, {
        text: '❌ Sorry, I encountered an error. Please try again later.',
        isUser: false
      }]);
    }

    setIsLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const formatMessage = (text) => {
    return text.split('\n').map((line, i) => (
      <React.Fragment key={i}>
        {line}
        <br />
      </React.Fragment>
    ));
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-content">
          <div className="header-logo">
            <span className="logo-icon">🌾</span>
            <h1>Agriculture <span>Multi-Agent</span></h1>
          </div>
          <div className="header-status">
            <span className="status-dot"></span>
            <span>AI Assistant</span>
          </div>
        </div>
      </header>

      {/* Main Chat Area */}
      <div className="chat-container">
        <div className="chat-messages">
          {messages.map((msg, index) => (
            <div key={index} className={`message-wrapper ${msg.isUser ? 'user-wrapper' : 'bot-wrapper'}`}>
              <div className={`message ${msg.isUser ? 'user-message' : 'bot-message'}`}>
                {!msg.isUser && (
                  <div className="bot-avatar">
                    <span>🌾</span>
                  </div>
                )}
                <div className="message-content">
                  <div className="message-text">
                    {msg.text.split('\n').map((line, i) => (
                      <React.Fragment key={i}>
                        {line}
                        <br />
                      </React.Fragment>
                    ))}
                  </div>
                </div>
                {msg.isUser && (
                  <div className="user-avatar">
                    <span>👤</span>
                  </div>
                )}
              </div>
            </div>
          ))}
          
          {isLoading && (
            <div className="message-wrapper bot-wrapper">
              <div className="message bot-message">
                <div className="bot-avatar">
                  <span>🌾</span>
                </div>
                <div className="message-content">
                  <div className="message-text">
                    <span className="typing-indicator">
                      <span></span>
                      <span></span>
                      <span></span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="chat-input-container">
          <div className="chat-input-wrapper">
            <textarea
              className="chat-input"
              placeholder="Ask me anything about agriculture..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              rows="2"
              disabled={isLoading}
            />
            <button 
              className="send-button"
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
            >
              {isLoading ? '⏳' : '📤'}
            </button>
          </div>
          <div className="chat-footer">
            <span>🌍 Available in English & Swahili</span>
            <span>Press Enter to send</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;

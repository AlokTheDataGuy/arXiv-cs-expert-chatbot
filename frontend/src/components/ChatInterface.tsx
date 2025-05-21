import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { FaPaperPlane, FaRobot, FaLightbulb } from 'react-icons/fa';
import MessageBubble from './MessageBubble';
import type { Message } from '../types/types';

const API_URL = 'http://localhost:8000';

// Example queries that users can click on
const EXAMPLE_QUERIES = [
  "Explain neural networks and their applications",
  "What is the difference between TCP and UDP protocols?",
  "How does blockchain technology work?",
  "Explain Big O notation with examples",
];

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when messages change
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setInput(e.target.value);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_URL}/chat`, {
        query: input,
      });

      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: response.data.response,
        timestamp: new Date(),
        image: response.data.image ? `${API_URL}/images/${response.data.image}` : undefined,
        sources: response.data.sources,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'bot',
        content: 'Sorry, I encountered an error processing your request. Please try again later.',
        timestamp: new Date(),
        isError: true,
      };

      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // Function to handle example query click
  const handleExampleClick = (query: string) => {
    setInput(query);
  };

  return (
    <div className="chat-interface">
      <div className="chat-container">
        {messages.length === 0 && (
          <div className="chat-welcome-header">
            <h2>Welcome to arXiv CS Expert Chatbot</h2>
            <p>
             Your AI research assistant for computer science—explaining concepts, answering complex questions, and summarizing arXiv papers in context-aware conversations.
            </p>
            <div className="chat-welcome-examples">
              {EXAMPLE_QUERIES.map((query, index) => (
                <div
                  key={index}
                  className="example-tag"
                  onClick={() => handleExampleClick(query)}
                >
                  <FaLightbulb style={{ marginRight: '6px', fontSize: '0.8rem' }} /> {query}
                </div>
              ))}
            </div>
          </div>
        )}
        <div className="messages-container">
          {messages.map((message) => (
            <MessageBubble key={message.id} message={message} />
          ))}
          {isLoading && (
            <div className="message bot">
              <div className="message-avatar">
                <FaRobot size={20} />
              </div>
              <div className="message-content loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
        <form className="input-container" onSubmit={handleSubmit}>
          <input
            type="text"
            value={input}
            onChange={handleInputChange}
            placeholder="Ask me about computer science..."
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !input.trim()}>
            <FaPaperPlane />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface;

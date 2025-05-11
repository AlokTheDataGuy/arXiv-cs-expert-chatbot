import React from 'react';
import { FaRobot, FaUser, FaExternalLinkAlt, FaBook } from 'react-icons/fa';
import ReactMarkdown from 'react-markdown';
import type { Message } from '../types';
import './MessageBubble.css';

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const { role, content, image, isError, sources } = message;

  return (
    <div className={`message ${role} ${isError ? 'error' : ''}`}>
      <div className="message-avatar" aria-label={role === 'bot' ? 'Bot' : 'User'}>
        {role === 'bot' ? <FaRobot size={20} /> : <FaUser size={20} />}
      </div>
      <div className="message-content">
        <ReactMarkdown>{content}</ReactMarkdown>

        {image && (
          <div className="message-image">
            <img src={image} alt="Generated visualization" />
          </div>
        )}

        {sources && sources.length > 0 && (
          <div className="message-sources">
            <div className="sources-header">
              <FaBook /> <span>Sources</span>
            </div>
            <div className="sources-list">
              {sources.map((source) => (
                <a
                  key={source.id}
                  href={source.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="source-tag"
                >
                  {source.title}
                  <FaExternalLinkAlt size={12} />
                </a>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;

import React from 'react';
import './Header.css';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-content">
        <h1 className="header-title">arXiv CS Expert Chatbot</h1>
        <p className="header-subtitle">
          Your AI assistant for computer science concepts and research
        </p>
      </div>
    </header>
  );
};

export default Header;

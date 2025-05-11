import React, { useState } from 'react';
import axios from 'axios';
import { FaImage, FaSpinner } from 'react-icons/fa';
import './Visualization.css';

const Visualization: React.FC = () => {
  const [concept, setConcept] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [image, setImage] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  const handleVisualize = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!concept.trim()) {
      setError('Please enter a concept to visualize');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    setImage(null);
    setMessage(null);
    
    try {
      const response = await axios.post('http://localhost:8000/visualize', {
        concept: concept.trim()
      });
      
      setImage(`http://localhost:8000/images/${response.data.image}`);
      setMessage(response.data.message);
    } catch (err) {
      console.error('Error generating visualization:', err);
      setError('Error generating visualization. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="visualization">
      <div className="visualization-container">
        <h2>Visualize Computer Science Concepts</h2>
        <p>Generate diagrams to visualize computer science concepts</p>
        
        <form className="visualization-form" onSubmit={handleVisualize}>
          <div className="visualization-input-container">
            <input
              type="text"
              value={concept}
              onChange={(e) => setConcept(e.target.value)}
              placeholder="Enter a concept to visualize (e.g., binary tree, neural network)"
              disabled={isLoading}
            />
            <button type="submit" disabled={isLoading}>
              {isLoading ? <FaSpinner className="spinner" /> : <FaImage />}
              {isLoading ? 'Generating...' : 'Generate Visualization'}
            </button>
          </div>
        </form>
        
        {error && <div className="error-message">{error}</div>}
        
        {image && (
          <div className="visualization-result">
            <h3>Visualization Result</h3>
            {message && <p className="success-message">{message}</p>}
            <div className="visualization-image">
              <img src={image} alt={`Visualization of ${concept}`} />
            </div>
          </div>
        )}
        
        <div className="visualization-examples">
          <h3>Example Concepts to Visualize</h3>
          <ul>
            <li>Binary Tree</li>
            <li>Neural Network</li>
            <li>Sorting Algorithm</li>
            <li>Hash Table</li>
            <li>TCP/IP Protocol</li>
            <li>Blockchain</li>
          </ul>
        </div>
      </div>
    </div>
  );
};

export default Visualization;

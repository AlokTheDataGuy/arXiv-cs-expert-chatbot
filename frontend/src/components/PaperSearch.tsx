import React, { useState } from 'react';
import axios from 'axios';
import { FaSearch, FaSpinner } from 'react-icons/fa';
import './PaperSearch.css';

interface Paper {
  id: string;
  title: string;
  authors: string[];
  abstract: string;
  published: string;
}

const PaperSearch: React.FC = () => {
  const [query, setQuery] = useState('');
  const [maxResults, setMaxResults] = useState(10);
  const [papers, setPapers] = useState<Paper[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a search query');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      const response = await axios.post('http://localhost:8000/search', {
        query,
        max_results: maxResults
      });
      
      setPapers(response.data);
      
      if (response.data.length === 0) {
        setError('No papers found matching your query');
      }
    } catch (err) {
      console.error('Error searching papers:', err);
      setError('Error searching papers. Please try again later.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="paper-search">
      <div className="search-container">
        <h2>Search arXiv Papers</h2>
        <p>Search for computer science papers on arXiv</p>
        
        <form className="search-form" onSubmit={handleSearch}>
          <div className="search-input-container">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter search query (e.g., neural networks, quantum computing)"
              disabled={isLoading}
            />
            <select
              value={maxResults}
              onChange={(e) => setMaxResults(Number(e.target.value))}
              disabled={isLoading}
            >
              <option value={5}>5 results</option>
              <option value={10}>10 results</option>
              <option value={20}>20 results</option>
              <option value={50}>50 results</option>
            </select>
            <button type="submit" disabled={isLoading}>
              {isLoading ? <FaSpinner className="spinner" /> : <FaSearch />}
              {isLoading ? 'Searching...' : 'Search'}
            </button>
          </div>
        </form>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="results-container">
          {papers.length > 0 && (
            <>
              <h3>Search Results ({papers.length})</h3>
              <div className="papers-list">
                {papers.map((paper) => (
                  <div key={paper.id} className="paper-card">
                    <h4 className="paper-title">{paper.title}</h4>
                    <div className="paper-meta">
                      <span className="paper-id">ID: {paper.id}</span>
                      <span className="paper-date">Published: {paper.published}</span>
                    </div>
                    <div className="paper-authors">
                      Authors: {paper.authors.join(', ')}
                    </div>
                    <p className="paper-abstract">{paper.abstract}</p>
                  </div>
                ))}
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default PaperSearch;

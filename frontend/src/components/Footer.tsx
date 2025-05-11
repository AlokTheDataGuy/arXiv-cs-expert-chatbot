import './Footer.css';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="footer-content">
        <p>© {new Date().getFullYear()} arXiv CS Expert Chatbot | Built with free and open-source tools</p>
        <div className="footer-links">
          <a href="https://arxiv.org/" target="_blank" rel="noopener noreferrer">
            arXiv
          </a>
          <a href="https://ollama.com/" target="_blank" rel="noopener noreferrer">
            Ollama
          </a>
          <a href="https://react.dev/" target="_blank" rel="noopener noreferrer">
            React
          </a>
          <a href="https://fastapi.tiangolo.com/" target="_blank" rel="noopener noreferrer">
            FastAPI
          </a>
        </div>
      </div>
    </footer>
  );
};

export default Footer;


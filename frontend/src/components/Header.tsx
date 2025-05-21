import React from 'react';
import { NavLink } from 'react-router-dom';
import { FaComments, FaSearch, FaProjectDiagram } from 'react-icons/fa';

const Header: React.FC = () => {
  return (
    <header className="header">
      <div className="header-container">
        <div className="header-content">
          <h1 className="header-title">
            <span>arXiv</span> <span>CS Expert</span>
          </h1>
        </div>

        <nav className="header-navigation">
          <ul className="nav-links">
            <li>
              <NavLink
                to="/chat"
                className={({ isActive }) => isActive ? 'active' : ''}
              >
                <FaComments className="nav-icon" /> Chat
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/search"
                className={({ isActive }) => isActive ? 'active' : ''}
              >
                <FaSearch className="nav-icon" /> Paper Search
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/visualize"
                className={({ isActive }) => isActive ? 'active' : ''}
              >
                <FaProjectDiagram className="nav-icon" /> Visualization
              </NavLink>
            </li>
          </ul>
        </nav>
      </div>
    </header>
  );
};

export default Header;

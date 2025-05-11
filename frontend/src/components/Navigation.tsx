import React from 'react';
import { NavLink } from 'react-router-dom';
import './Navigation.css';

const Navigation: React.FC = () => {
  return (
    <nav className="navigation">
      <ul className="nav-links">
        <li>
          <NavLink 
            to="/chat" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Chat
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/search" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Paper Search
          </NavLink>
        </li>
        <li>
          <NavLink 
            to="/visualize" 
            className={({ isActive }) => isActive ? 'active' : ''}
          >
            Visualization
          </NavLink>
        </li>
      </ul>
    </nav>
  );
};

export default Navigation;

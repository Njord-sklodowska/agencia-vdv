import React, { useState } from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';
import '../../styles/layout.css';

const Layout = ({ children }) => {
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <div className="d-flex flex-column vh-100">
      <Navbar onToggleSidebar={toggleSidebar} />
      <div className="d-flex flex-grow-1 overflow-hidden">
        <Sidebar isCollapsed={isCollapsed} />
        <main className="main-content overflow-auto">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;

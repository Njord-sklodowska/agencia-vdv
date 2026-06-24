import React from 'react';
import { useAuth } from '../../context/AuthContext';

const Navbar = ({ onToggleSidebar }) => {
  const { user, logout } = useAuth();

  return (
    <nav className="navbar navbar-custom px-3 d-flex align-items-center justify-content-between">
      <div className="d-flex align-items-center gap-3">
        <button className="btn p-0 navbar-toggle" onClick={onToggleSidebar}>
          <i className="bi bi-list fs-4"></i>
        </button>
        <a className="navbar-brand d-flex align-items-center gap-2 mb-0" href="#">
          <i className="bi bi-car-front-fill"></i> Agencia VDV
        </a>
      </div>

      <div className="d-flex align-items-center gap-3">
        <div className="position-relative">
          <i className="bi bi-bell nav-icon" style={{ cursor: 'pointer' }}></i>
          <span className="position-absolute top-0 start-100 translate-middle badge rounded-pill navbar-badge-notif">
            3
          </span>
        </div>

        <div className="user-pill">
          <div className="avatar">
            {user?.username ? user.username.substring(0, 2).toUpperCase() : 'AD'}
          </div>
          <div className="lh-sm">
            <p className="navbar-user-name">
              {user?.first_name ? `${user.first_name} ${user.last_name}` : user?.username || 'Administrador'}
            </p>
            <p className="sub">{user?.rol_nombre || user?.rol || 'Admin'}</p>
          </div>
          <i className="bi bi-chevron-down navbar-chevron"></i>
        </div>

        <button className="btn btn-logout btn-sm" onClick={logout}>
          <i className="bi bi-box-arrow-right me-1"></i> Salir
        </button>
      </div>
    </nav>
  );
};

export default Navbar;

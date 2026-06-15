import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ isCollapsed }) => {
  const menuItems = [
    {
      group: 'Principal',
      items: [
        { path: '/dashboard', label: 'Dashboard', icon: 'bi-speedometer2' },
      ]
    },
    {
      group: 'Gestión',
      items: [
        { path: '/clientes', label: 'Clientes', icon: 'bi-people' },
        { path: '/inventario', label: 'Inventario', icon: 'bi-car-front' },
        { path: '/ventas', label: 'Ventas', icon: 'bi-cart-check' },
      ]
    },
    {
      group: 'Administración',
      items: [
        { path: '/cobranzas', label: 'Cobranzas', icon: 'bi-cash-stack' },
        { path: '/documentacion', label: 'Documentos', icon: 'bi-file-earmark-text' },
        { path: '/reportes', label: 'Reportes', icon: 'bi-graph-up' },
      ]
    },
    {
      group: 'Sistema',
      items: [
        { path: '/admin/usuarios', label: 'Usuarios', icon: 'bi-person-gear' },
        { path: '/admin/parametros', label: 'Configuración', icon: 'bi-gear' },
      ]
    }
  ];

  return (
    <aside className={`sidebar-container ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="pt-3">
        {menuItems.map((section, idx) => (
          <React.Fragment key={idx}>
            <div className="section-label">{section.group}</div>
            {section.items.map((item) => (
              <NavLink 
                key={item.path} 
                to={item.path} 
                className={({ isActive }) => `nav-link-custom ${isActive ? 'active' : ''}`}
                title={isCollapsed ? item.label : ''}
              >
                <i className={`bi ${item.icon}`}></i>
                <span className="nav-link-text">{item.label}</span>
              </NavLink>
            ))}
          </React.Fragment>
        ))}
      </div>
    </aside>
  );
};

export default Sidebar;

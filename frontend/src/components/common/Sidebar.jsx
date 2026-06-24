import React, { useState, useEffect } from 'react';
import { NavLink, useLocation } from 'react-router-dom';

const Sidebar = ({ isCollapsed }) => {
  const [openMenus, setOpenMenus] = useState({});
  const location = useLocation();

  useEffect(() => {
    const activeGroup = menuItems.find(section =>
      section.items.some(item => {
        if (item.path && location.pathname.startsWith(item.path)) return true;
        if (item.children) return item.children.some(c => location.pathname.startsWith(c.path));
        return false;
      })
    );
    if (activeGroup) {
      const parentWithChildren = activeGroup.items.find(item =>
        item.children && item.children.some(c => location.pathname.startsWith(c.path))
      );
      if (parentWithChildren) {
        setOpenMenus(prev => ({ ...prev, [parentWithChildren.label]: true }));
      }
    }
  }, [location.pathname]);

  const toggleMenu = (menuLabel) => {
    setOpenMenus(prev => ({
      ...prev,
      [menuLabel]: !prev[menuLabel]
    }));
  };

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
        { path: '/gestion/sucursales', label: 'Sucursales', icon: 'bi-building-check' },
        {
          label: 'Inventario',
          icon: 'bi-car-front',
          children: [
            { path: '/inventario', label: 'Stock de Vehículos', icon: 'bi-list-ul' },
            { path: '/inventario/usados', label: 'Vehículos Usados', icon: 'bi-car-front-fill' },
            { path: '/inventario/traslados', label: 'Traslados', icon: 'bi-truck' },
            { path: '/inventario/talleres', label: 'Talleres', icon: 'bi-wrench' },
          ]
        },
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
        { path: '/admin/auditoria', label: 'Auditoría', icon: 'bi-shield-check' },
      ]
    }
  ];

  return (
    <aside className={`sidebar-container ${isCollapsed ? 'collapsed' : ''}`}>
      <div className="pt-3">
        {menuItems.map((section, idx) => (
          <React.Fragment key={idx}>
            <div className="sidebar-section-label">
              {section.group}
            </div>

            {section.items.map((item) => {
              if (item.children) {
                const isOpen = openMenus[item.label];
                return (
                  <div key={item.label} style={{ marginBottom: '2px' }}>
                    <button
                      className={`sidebar-nav-item ${isOpen ? 'active' : ''}`}
                      onClick={() => toggleMenu(item.label)}
                      title={isCollapsed ? item.label : ''}
                    >
                      <div className="d-flex align-items-center" style={{ gap: '12px', justifyContent: isCollapsed ? 'center' : 'flex-start', width: '100%' }}>
                        <i className={`bi ${item.icon} sidebar-nav-icon`}></i>
                        {!isCollapsed && <span className="sidebar-nav-text">{item.label}</span>}
                      </div>
                      {!isCollapsed && (
                        <i className={`bi bi-chevron-${isOpen ? 'up' : 'down'}`} style={{ fontSize: '11px', opacity: 0.5 }}></i>
                      )}
                    </button>

                    {!isCollapsed && isOpen && (
                      <div className="sidebar-submenu">
                        {item.children.map(child => (
                          <NavLink
                            key={child.path}
                            to={child.path}
                            className={({ isActive }) => `sidebar-submenu-item ${isActive ? 'active' : ''}`}
                          >
                            <i className={`bi ${child.icon} sidebar-submenu-icon`}></i>
                            <span>{child.label}</span>
                          </NavLink>
                        ))}
                      </div>
                    )}
                  </div>
                );
              }

              return (
                <NavLink
                  key={item.path}
                  to={item.path}
                  className={({ isActive }) => `sidebar-nav-item ${isActive ? 'active' : ''}`}
                  title={isCollapsed ? item.label : ''}
                >
                  <i className={`bi ${item.icon} sidebar-nav-icon`}></i>
                  {!isCollapsed && <span className="sidebar-nav-text">{item.label}</span>}
                </NavLink>
              );
            })}
          </React.Fragment>
        ))}
      </div>
    </aside>
  );
};

export default Sidebar;

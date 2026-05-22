import React from 'react'
import { Outlet, Link, useLocation } from 'react-router-dom'
import { Package, Users, ShoppingCart, LogOut, Square, MapPin } from 'lucide-react'

function DashboardLayout() {
  const location = useLocation()

  // Limpiamos la ruta para que no importe si viene con "/" o no
  const currentPath = location.pathname.replace(/^\/|\/$/g, '')

  // El menú se muestra ancho (260px) SOLO en la raíz, sino se encoge a 75px
  const mostrarMenuAncho = currentPath === '' || currentPath === 'dashboard'

  // Función corregida y blindada para activar los colores del icono
  const activeClass = (targetPath) => {
    return currentPath === targetPath
      ? 'nav-link text-white bg-success d-flex justify-content-center align-items-center rounded shadow-sm p-3' 
      : 'nav-link text-white-50 d-flex justify-content-center align-items-center rounded hover-sidebar p-3'
  }

  return (
    <div className="d-flex" style={{ minHeight: '100vh', width: '100vw', overflowX: 'hidden' }}>
      
      {/* MENÚ LATERAL (SIDEBAR) */}
      <div 
        className="bg-dark d-flex flex-column justify-content-between p-2" 
        style={{ 
          width: mostrarMenuAncho ? '260px' : '75px', 
          transition: 'width 0.2s ease-in-out',
          backgroundColor: '#1a202c', // Un gris oscuro más moderno estilo ERP
          minWidth: mostrarMenuAncho ? '260px' : '75px'
        }}
      >
        <div>
          {/* Identificador superior */}
          <div className="text-center my-3">
            {mostrarMenuAncho ? (
              <h4 className="fw-bold text-success mb-0">Del Valle</h4>
            ) : (
              <Square size={18} className="text-white opacity-50" strokeWidth={1.5} />
            )}
          </div>
          <hr className="text-secondary my-3 opacity-25" />

          {/* LISTA DE NAVEGACIÓN */}
          <ul className="nav nav-pills flex-column gap-3 text-center mt-4">
            
            {/* INVENTARIO */}
            <li className="nav-item" title="Inventario">
              <Link to="/inventario" className={activeClass('inventario')}>
                <Package size={22} strokeWidth={1.5} />
                {mostrarMenuAncho && <span className="ms-3 fs-6">Inventario</span>}
              </Link>
            </li>
            
            {/* CLIENTES */}
            <li className="nav-item" title="Clientes">
              <Link to="/clientes" className={activeClass('clientes')}>
                <Users size={22} strokeWidth={1.5} />
                {mostrarMenuAncho && <span className="ms-3 fs-6">Clientes</span>}
              </Link>
            </li>
            
            {/* OPERACIONES */}
            <li className="nav-item" title="Operaciones de Venta">
              <Link to="/ventas" className={activeClass('ventas')}>
                <ShoppingCart size={22} strokeWidth={1.5} />
                {mostrarMenuAncho && <span className="ms-3 fs-6">Operaciones</span>}
              </Link>
            </li>
          </ul>
        </div>

        {/* BOTÓN INFERIOR DE SALIDA */}
        <div>
          <hr className="text-secondary opacity-25" />
          <Link to="/" className="nav-link text-danger text-center p-3 rounded" title="Cerrar Sesión">
            <LogOut size={22} strokeWidth={1.5} />
          </Link>
        </div>
      </div>

      {/* CONTENIDO PRINCIPAL (DERECHA) */}
      <div className="flex-grow-1 bg-light d-flex flex-column" style={{ backgroundColor: '#f7fafc', minWidth: 0 }}>
        
        {/* BARRA SUPERIOR (HEADER) */}
        <header className="bg-white p-3 d-flex justify-content-between align-items-center border-bottom shadow-sm" style={{ height: '65px' }}>
          <div className="d-flex align-items-center gap-2">
            <MapPin size={18} className="text-secondary" strokeWidth={1.5} />
            <span className="text-secondary fw-medium small">
              Sucursal Centro (Concepción)
            </span>
          </div>
          
        </header>

        {/* CONTENEDOR DE PÁGINAS DINÁMICAS */}
        <main className="p-4 flex-grow-1" style={{ overflowY: 'auto', backgroundColor: '#edf2f7' }}>
          <Outlet />
        </main>
      </div>

    </div>
  )
}

export default DashboardLayout
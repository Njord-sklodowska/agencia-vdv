import React, { useState } from 'react';
import { Search, Eye, Pencil, Trash2, ChevronLeft, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';

// DATOS SIMULADOS EXACTOS PARA CLIENTES
const clientesSimulados = [
  { 
    id_cliente: 1, 
    nombre: 'Juan', 
    apellido: 'Perez', 
    dni_cuit: '2034567891', 
    telefono: '3814567890', 
    email: 'juan.perez@email.com', 
    estado: 'activo' 
  },
  { 
    id_cliente: 2, 
    nombre: 'Maria', 
    apellido: 'Gomez', 
    dni_cuit: '2733445566', 
    telefono: '3854123456', 
    email: 'maria.g@email.com', 
    estado: 'inactivo' 
  },
  { 
    id_cliente: 3, 
    nombre: 'Carlos', 
    apellido: 'Ruiz', 
    dni_cuit: '2011223344', 
    telefono: '3819876543', 
    email: 'cruiz@empresa.com', 
    estado: 'activo' 
  }
];

function ClientesPage() {
  const [busqueda, setBusqueda] = useState('');
  const [listaClientes, setListaClientes] = useState(clientesSimulados);

  // CONFIGURACIÓN DE PAGINACIÓN (30 líneas fijas por página)
  const [paginaActual, setPaginaActual] = useState(1);
  const clientesPorPagina = 30; 

  const indiceUltimoCliente = paginaActual * clientesPorPagina;
  const indicePrimerCliente = indiceUltimoCliente - clientesPorPagina;
  const clientesDeLaPagina = listaClientes.slice(indicePrimerCliente, indiceUltimoCliente);
  const totalPaginas = Math.ceil(listaClientes.length / clientesPorPagina);
  const filasVisuales = Array.from({ length: clientesPorPagina });

  // 🔍 FUNCIÓN DE NORMALIZACIÓN PARA BÚSQUEDAS
  const normalizarTexto = (texto) => {
    if (!texto) return '';
    return texto
      .toString()
      .toLowerCase()
      .normalize('NFD')
      .replace(/[\u0300-\u036f]/g, '')
      .trim();
  };

  // Renderizador estético de Estados (ACTIVO / INACTIVO)
  const renderEstado = (estado) => {
    const estilos = {
      activo: { bg: '#5cb85c', texto: 'ACTIVO' },
      inactivo: { bg: '#d9534f', texto: 'INACTIVO' }
    };
    const config = estilos[estado] || { bg: '#777', texto: 'DESCONOCIDO' };
    
    return (
      <span className="badge fw-bold px-3 py-1 text-white shadow-sm" style={{ backgroundColor: config.bg, borderRadius: '12px', fontSize: '0.75rem' }}>
        {config.texto}
      </span>
    );
  };

  return (
    <div className="container-fluid p-0" style={{ minHeight: '100%' }}>
      
      {/* Migas de pan */}
      <div className="mb-2 text-muted small fw-semibold ps-1" style={{ letterSpacing: '0.5px' }}>
        Clientes &gt; <span style={{ color: '#4a5568' }}>Listado de clientes</span>
      </div>

      {/* CONTENEDOR PRINCIPAL */}
      <div className="card shadow-sm border-secondary border-opacity-25" style={{ borderRadius: '8px', overflow: 'hidden', backgroundColor: '#e2e8f0' }}>
        
        {/* ENCABEZADO TITULO */}
        <div className="p-3" style={{ backgroundColor: '#2c3e50' }}>
          <h2 className="text-white m-0 fw-bold fs-3" style={{ fontFamily: 'sans-serif', letterSpacing: '0.5px' }}>
            Listado de Clientes
          </h2>
        </div>

        {/* BARRA DE ACCIONES Y FILTROS */}
        <div className="d-flex justify-content-between align-items-center p-3 bg-white border-bottom border-secondary border-opacity-25 shadow-sm">
          
          {/* Buscador */}
          <div className="input-group" style={{ width: '420px' }}>
            <span className="input-group-text bg-light border-secondary border-opacity-50 text-muted px-3">
              <Search size={18} strokeWidth={1.5} className="text-secondary opacity-75" />
            </span>
            <input 
              type="text" 
              className="form-control bg-light border-secondary border-opacity-50" 
              placeholder="BUSCAR POR NOMBRE, DNI O EMAIL..." 
              style={{ fontSize: '0.8rem', letterSpacing: '0.5px', height: '42px' }}
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
            />
          </div>

          {/* Botón Agregar Cliente */}
          <Link 
            to="/clientes/nuevo" 
            className="btn fw-bold border-0 text-uppercase px-4 py-2 shadow-sm" 
            style={{ 
              backgroundColor: '#f0ad4e', 
              color: '#000', 
              fontSize: '0.8rem', 
              letterSpacing: '0.5px', 
              borderRadius: '6px', 
              height: '42px',
              display: 'inline-flex',
              alignItems: 'center',
              textDecoration: 'none'
            }}
          >
            Agregar Cliente
          </Link>
        </div>

        {/* TABLA DE CLIENTES CON ESTÉTICA UNIFICADA */}
        <div className="table-responsive bg-white">
          <table className="table table-bordered align-middle mb-0 text-center" style={{ borderColor: '#cbd5e0', fontSize: '0.85rem' }}>
            <thead>
              <tr className="fw-bold text-dark" style={{ backgroundColor: '#cbd5e0' }}>
                <th style={{ width: '8%', backgroundColor: '#a0aec0' }}>ID</th>
                <th style={{ width: '25%', backgroundColor: '#a0aec0' }}>Nombre y Apellido</th>
                <th style={{ width: '15%', backgroundColor: '#a0aec0' }}>DNI / CUIT</th>
                <th style={{ width: '15%', backgroundColor: '#a0aec0' }}>Teléfono</th>
                <th style={{ width: '21%', backgroundColor: '#a0aec0' }}>Email</th>
                <th style={{ width: '8%', backgroundColor: '#a0aec0' }}>Estado</th>
                <th style={{ width: '8%', backgroundColor: '#a0aec0' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filasVisuales.map((_, index) => {
                const cliente = clientesDeLaPagina[index] || {};
                
                // 🔍 LÓGICA DE BÚSQUEDA MULTI-CRITERIO
                const texto = normalizarTexto(busqueda);
                const nombreCompleto = cliente.nombre ? normalizarTexto(`${cliente.nombre} ${cliente.apellido}`) : '';

                const coincide = texto !== '' && cliente.id_cliente && (
                  nombreCompleto.includes(texto) ||
                  normalizarTexto(cliente.dni_cuit).startsWith(texto) ||
                  normalizarTexto(cliente.email).includes(texto) ||
                  normalizarTexto(cliente.estado).startsWith(texto)
                );

                // Alternado y Resaltado Amarillo Simétrico
                const colorFondo = coincide 
                  ? '#f6d9a2' 
                  : (index % 2 === 0 ? '#ffffff' : '#c4c4c4ef');

                return (
                  <tr key={index} style={{ height: '40px', '--bs-table-bg': colorFondo }}>
                    <td className="text-muted small">{cliente.id_cliente || ''}</td>
                    <td className="text-start px-3 text-dark fw-medium">
                      {cliente.nombre ? `${cliente.nombre} ${cliente.apellido}` : ''}
                    </td>
                    <td className="fw-mono text-dark">{cliente.dni_cuit || ''}</td>
                    <td className="text-dark">{cliente.telefono || ''}</td>
                    <td className="text-dark">{cliente.email || ''}</td>
                    <td>{cliente.estado ? renderEstado(cliente.estado) : ''}</td>
                    <td>
                      {cliente.id_cliente && (
                        <div className="d-flex justify-content-center gap-3">
                          <button className="btn btn-sm p-0 text-secondary opacity-70" title="Ver Detalle">
                            <Eye size={18} strokeWidth={1.5} />
                          </button>
                          <button className="btn btn-sm p-0 text-secondary opacity-70" title="Editar">
                            <Pencil size={18} strokeWidth={1.5} />
                          </button>
                          <button className="btn btn-sm p-0 text-secondary opacity-70" title="Eliminar">
                            <Trash2 size={18} strokeWidth={1.5} />
                          </button>
                        </div>
                      )}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        {/* --- CONTENEDOR DE PAGINACIÓN --- */}
        <div className="d-flex justify-content-between align-items-center p-3 bg-light border-top border-secondary border-opacity-25">
          <div className="text-muted fw-bold">
            Mostrando página {paginaActual} de {totalPaginas || 1}
          </div>

        <div className="d-flex gap-2">
            <button
              className="btn btn-primary"
              style={{
                backgroundColor: '#8d9caf',
                color: '#000000',
                fontSize: '16px',
                fontWeight: '800',
                border: 'none',
                padding: '10px 24px'
              }}
              disabled={paginaActual === 1}
              onClick={() => setPaginaActual(prev => prev - 1)}
            >
              <ChevronLeft size={20} className="me-1" /> Anterior
            </button>

            <button
              className="btn btn-primary"
              style={{
                backgroundColor: '#8d9caf',
                color: '#000000',
                fontSize: '16px',
                fontWeight: '800',
                border: 'none',
                padding: '10px 24px'
              }}
              disabled={paginaActual === totalPaginas || totalPaginas === 0}
              onClick={() => setPaginaActual(prev => prev + 1)}
            >
              Siguiente <ChevronRight size={20} className="ms-1" />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

export default ClientesPage;
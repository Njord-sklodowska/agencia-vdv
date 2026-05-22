import React from 'react';
import { Search, Eye, Pencil, Trash2, Filter } from 'lucide-react';

// DATOS SIMULADOS 100% COINCIDENTES CON EL MODELO DE BASE DE DATOS (.DOCX)
const vehiculosSimulados = [
  { 
    id_vehiculo: 1, 
    id_sucursal: 1, // Sucursal Concepción
    condicion_vehiculo: 'usado', 
    patente: 'AA123BB', 
    vin: null, 
    marca_nombre: 'VolksWagen', 
    modelo_nombre: 'Amarok', 
    anio: 2021, 
    precio: 28500000.00, 
    estado: 'en_stock' 
  },
  { 
    id_vehiculo: 2, 
    id_sucursal: 1, 
    condicion_vehiculo: '0km', 
    patente: null, 
    vin: '8A1FD8LM239482', 
    marca_nombre: 'Fiat', 
    modelo_nombre: 'Cronos', 
    anio: 2026, 
    precio: 19800000.00, 
    estado: 'en_stock' 
  },
  { 
    id_vehiculo: 3, 
    id_sucursal: 2, // Sucursal La Banda
    condicion_vehiculo: 'usado', 
    patente: 'AF999ZZ', 
    vin: null, 
    marca_nombre: 'Toyota', 
    modelo_nombre: 'Hilux', 
    anio: 2023, 
    precio: 35000000.00, 
    estado: 'reservado' 
  }
];

function InventarioPage() {
  // Generamos una grilla limpia de 14 filas para mantener la estética de Figma
  const filasTotales = Array.from({ length: 14 });

  // Renderizador estético de Estados según los ENUM de la Base de Datos
  const renderEstado = (estado) => {
    const estilos = {
      en_stock: { bg: '#5cb85c', texto: 'EN STOCK' },
      reservado: { bg: '#f0ad4e', texto: 'RESERVADO' },
      vendido: { bg: '#d9534f', texto: 'VENDIDO' }
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
      
      {/* Migas de pan de la esquina superior */}
      <div className="mb-2 text-muted small fw-semibold ps-1" style={{ letterSpacing: '0.5px' }}>
        Inventario &gt; <span style={{ color: '#4a5568' }}>Listado de vehículos</span>
      </div>

      {/* CONTENEDOR PRINCIPAL */}
      <div className="card shadow-sm border-secondary border-opacity-25" style={{ borderRadius: '8px', overflow: 'hidden', backgroundColor: '#e2e8f0' }}>
        
        {/* ENCABEZADO */}
        <div className="p-3" style={{ backgroundColor: '#2c3e50' }}>
          <h2 className="text-white m-0 fw-bold fs-3" style={{ fontFamily: 'sans-serif', letterSpacing: '0.5px' }}>
            Listado de Vehículos
          </h2>
        </div>

        {/* BARRA DE ACCIONES Y FILTROS */}
        <div className="d-flex justify-content-between align-items-center p-3 bg-white border-bottom border-secondary border-opacity-25 shadow-sm">
          
          {/* Buscador unificado estilo Bootstrap */}
          <div className="input-group" style={{ width: '420px' }}>
            <span className="input-group-text bg-light border-secondary border-opacity-50 text-muted px-3">
              <Search size={18} strokeWidth={1.5} className="text-secondary opacity-75" />
            </span>
            <input 
              type="text" 
              className="form-control bg-light border-secondary border-opacity-50" 
              placeholder="BUSCAR POR MARCA O MODELO..." 
              style={{ fontSize: '0.8rem', letterSpacing: '0.5px', height: '42px' }}
              disabled
            />
          </div>

          {/* Botón de Acción Principal */}
          <button 
            className="btn fw-bold border-0 text-uppercase px-4 py-2 shadow-sm" 
            style={{ backgroundColor: '#f0ad4e', color: '#000', fontSize: '0.8rem', letterSpacing: '0.5px', borderRadius: '6px', height: '42px' }}
          >
            Agregar Vehículo
          </button>
        </div>

        {/* TABLA DE STOCK CON LAS CLAVES REALES DEL BACKEND */}
        <div className="table-responsive bg-white">
          <table className="table table-bordered align-middle mb-0 text-center" style={{ borderColor: '#cbd5e0', fontSize: '0.85rem' }}>
            <thead>
              <tr className="fw-bold text-dark" style={{ backgroundColor: '#cbd5e0' }}>
                <th style={{ width: '8%', backgroundColor: '#a0aec0' }}>ID</th>
                <th style={{ width: '20%', backgroundColor: '#a0aec0' }}>Marca / Modelo</th>
                <th style={{ width: '12%', backgroundColor: '#a0aec0' }}>Año</th>
                <th style={{ width: '15%', backgroundColor: '#a0aec0' }}>Condición</th>
                <th style={{ width: '15%', backgroundColor: '#a0aec0' }}>Patente / VIN</th>
                <th style={{ width: '14%', backgroundColor: '#a0aec0' }}>Precio de Venta</th>
                <th style={{ width: '8%', backgroundColor: '#a0aec0' }}>Estado</th>
                <th style={{ width: '8%', backgroundColor: '#a0aec0' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filasTotales.map((_, index) => {
                // Evaluamos si existe un registro en esta posición del índice
                const auto = vehiculosSimulados[index] || {};
                
                return (
                  <tr key={index} style={{ height: '40px', backgroundColor: index % 2 === 0 ? '#ffffff' : '#f7fafc' }}>
                    <td className="text-muted small">{auto.id_vehiculo || ''}</td>
                    <td className="text-start px-3 fw-medium">
                      {auto.marca_nombre ? `${auto.marca_nombre} ${auto.modelo_nombre}` : ''}
                    </td>
                    <td>{auto.anio || ''}</td>
                    <td className="text-uppercase small fw-semibold text-secondary">
                      {auto.condicion_vehiculo || ''}
                    </td>
                    {/* LOGICA CONDICIONAL: Si es 0km muestra el VIN, sino la Patente */}
                    <td className="fw-mono small">
                      {auto.condicion_vehiculo === '0km' ? auto.vin : auto.patente}
                    </td>
                    <td className="text-end px-3 fw-bold text-dark">
                      {auto.precio ? `$ ${auto.precio.toLocaleString('es-AR')}` : ''}
                    </td>
                    <td>{auto.estado ? renderEstado(auto.estado) : ''}</td>
                    <td>
                      {auto.id_vehiculo && (
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
      </div>
    </div>
  );
}

export default InventarioPage;
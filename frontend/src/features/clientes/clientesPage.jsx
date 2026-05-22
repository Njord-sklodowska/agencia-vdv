import React from 'react';
import { Search, Eye, Pencil, Trash2 } from 'lucide-react';

// DATOS SIMULADOS 100% COINCIDENTES CON LA TABLA CLIENTE DEL .DOCX
const clientesSimulados = [
  { id_cliente: 1, dni_cuit: '28.344.192', nombre_completo: 'Juan Carlos Pérez', telefono: '385-4123456', email: 'juan.perez@email.com', domicilio_completo: 'Av. Belgrano N° 450, Concepción' },
  { id_cliente: 2, dni_cuit: '30-34881004-2', nombre_completo: 'María Inés Rodríguez (S.A.)', telefono: '385-5987654', email: 'maria.rodriguez@email.com', domicilio_completo: 'B° Autonomía Mza 4 Lote 12, Santiago Centro' },
  { id_cliente: 3, dni_cuit: '22.115.938', nombre_completo: 'Carlos Alberto Gómez', telefono: '385-4888222', email: 'gomez.carlos@email.com', domicilio_completo: 'San Martín 125, La Banda' },
];

function ClientesPage() {
  const filasTotales = Array.from({ length: 14 });

  return (
    <div className="container-fluid p-0" style={{ minHeight: '100%' }}>
      
      {/* Migas de pan */}
      <div className="mb-2 text-muted small fw-semibold ps-1" style={{ letterSpacing: '0.5px' }}>
        Clientes &gt; <span style={{ color: '#4a5568' }}>Listado de clientes</span>
      </div>

      {/* CONTENEDOR PRINCIPAL */}
      <div className="card shadow-sm border-secondary border-opacity-25" style={{ borderRadius: '8px', overflow: 'hidden', backgroundColor: '#e2e8f0' }}>
        
        {/* ENCABEZADO ESTILO CORPORATIVO */}
        <div className="p-3" style={{ backgroundColor: '#484d7a' }}>
          <h2 className="text-white m-0 fw-bold fs-3" style={{ fontFamily: 'sans-serif', letterSpacing: '0.5px' }}>
            Listado de Clientes
          </h2>
        </div>

        {/* BARRA DE ACCIONES */}
        <div className="d-flex justify-content-between align-items-center p-3 bg-white border-bottom border-secondary border-opacity-25 shadow-sm">
          
          <div className="input-group" style={{ width: '420px' }}>
            <span className="input-group-text bg-light border-secondary border-opacity-50 text-muted px-3">
              <Search size={18} strokeWidth={1.5} className="text-secondary opacity-75" />
            </span>
            <input 
              type="text" 
              className="form-control bg-light border-secondary border-opacity-50" 
              placeholder="BUSCAR POR NOMBRE, DNI O EMAIL..." 
              style={{ fontSize: '0.8rem', letterSpacing: '0.5px', height: '42px' }}
              disabled
            />
          </div>

          <button 
            className="btn fw-bold border-0 text-uppercase px-4 py-2 shadow-sm" 
            style={{ backgroundColor: '#f0ad4e', color: '#000', fontSize: '0.8rem', letterSpacing: '0.5px', borderRadius: '6px', height: '42px' }}
          >
            Agregar Cliente
          </button>
        </div>

        {/* TABLA DE CLIENTES CON CLAVES DE BASE DE DATOS */}
        <div className="table-responsive bg-white">
          <table className="table table-bordered align-middle mb-0 text-center" style={{ borderColor: '#cbd5e0', fontSize: '0.85rem' }}>
            <thead>
              <tr className="fw-bold text-dark" style={{ backgroundColor: '#cbd5e0' }}>
                <th style={{ width: '6%', backgroundColor: '#a0aec0' }}>ID</th>
                <th style={{ width: '24%', backgroundColor: '#a0aec0' }}>Nombre y Apellido</th>
                <th style={{ width: '14%', backgroundColor: '#a0aec0' }}>DNI / CUIT</th>
                <th style={{ width: '12%', backgroundColor: '#a0aec0' }}>Teléfono</th>
                <th style={{ width: '18%', backgroundColor: '#a0aec0' }}>Email</th>
                <th style={{ width: '18%', backgroundColor: '#a0aec0' }}>Domicilio Completo</th>
                <th style={{ width: '8%', backgroundColor: '#a0aec0' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {filasTotales.map((_, index) => {
                const cliente = clientesSimulados[index] || {};
                return (
                  <tr key={index} style={{ height: '40px', backgroundColor: index % 2 === 0 ? '#ffffff' : '#f7fafc' }}>
                    <td className="text-muted small">{cliente.id_cliente || ''}</td>
                    <td className="text-start px-3 fw-medium">{cliente.nombre_completo || ''}</td>
                    <td className="fw-mono">{cliente.dni_cuit || ''}</td>
                    <td>{cliente.telefono || ''}</td>
                    <td className="text-start px-3 text-muted">{cliente.email || ''}</td>
                    <td className="text-start px-3 small text-truncate" style={{ maxWidth: '180px' }}>
                      {cliente.domicilio_completo || ''}
                    </td>
                    <td>
                      {cliente.id_cliente && (
                        <div className="d-flex justify-content-center gap-3">
                          <button className="btn btn-sm p-0 text-secondary opacity-70" title="Ver ficha">
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

export default ClientesPage;
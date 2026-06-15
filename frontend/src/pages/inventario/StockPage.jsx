import React, { useState, useMemo, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  useReactTable, 
  getCoreRowModel, 
  flexRender, 
  createColumnHelper,
  getFilteredRowModel,
  getPaginationRowModel,
  getSortedRowModel
} from '@tanstack/react-table';
import { inventarioApi } from '../../api/inventarioApi';
import VehiculoFormModal from '../../components/inventario/VehiculoFormModal';

const columnHelper = createColumnHelper();

const columns = [
  columnHelper.accessor('patente', {
    header: 'Patente / VIN',
    cell: info => <span className="fw-medium text-dark">{info.getValue() || '---'}</span>,
  }),
  columnHelper.accessor('marca_nombre', {
    header: 'Marca',
    cell: info => <span>{info.getValue() || '---'}</span>,
  }),
  columnHelper.accessor('modelo_nombre', {
    header: 'Modelo',
    cell: info => <span>{info.getValue() || '---'}</span>,
  }),
  columnHelper.accessor('anio', {
    header: 'Año',
    cell: info => <span>{info.getValue() || '---'}</span>,
  }),
  columnHelper.accessor('precio', {
    header: 'Precio',
    cell: info => <span className="fw-bold text-dark">{info.getValue() ? `$${info.getValue()}` : '---'}</span>,
  }),
  columnHelper.accessor('estado', {
    header: 'Estado',
    cell: info => {
      const estado = info.getValue();
      const badgeClass = estado === 'Nuevo' || estado === 'disponible' ? 'badge-gold' : 'badge-salmon';
      return <span className={`badge ${badgeClass}`}>{estado || '---'}</span>;
    },
  }),
  columnHelper.display({
    id: 'acciones',
    header: 'Acciones',
    cell: props => {
      const vehicle = props.row.original;
      return (
        <div className="d-flex gap-2">
          <button 
            className="btn btn-outline-custom btn-sm" 
            title="Editar"
            onClick={() => props.table.options.meta?.onEdit(vehicle)}
          >
            <i className="bi bi-pencil"></i>
          </button>
          <button 
            className="btn btn-outline-custom btn-sm text-danger" 
            title="Desactivar"
            onClick={() => props.table.options.meta?.onDelete(vehicle)}
          >
            <i className="bi bi-trash"></i>
          </button>
        </div>
      );
    },
  }),
];

const StockPage = () => {
  const navigate = useNavigate();
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [globalFilter, setGlobalFilter] = useState('');
  const [statusFilter, setStatusFilter] = useState('todos');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [vehicleToEdit, setVehicleToEdit] = useState(null);

  const fetchData = async () => {
    try {
      setLoading(true);
      const result = await inventarioApi.getVehiculos();
      const vehicles = Array.isArray(result) ? result : (result.results || []);
      setData(vehicles);
    } catch (err) {
      console.error("Error loading stock:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleEdit = (vehicle) => {
    setVehicleToEdit(vehicle);
    setIsModalOpen(true);
  };

  const handleDelete = async (vehicle) => {
    if (window.confirm(`¿Estás seguro de que deseas desactivar el vehículo ${vehicle.modelo_nombre} (${vehicle.patente})?`)) {
      try {
        await inventarioApi.deleteVehiculo(vehicle.id);
        fetchData();
        alert('Vehículo desactivado correctamente.');
      } catch (err) {
        alert('Error al desactivar el vehículo.');
      }
    }
  };

  const filteredData = useMemo(() => {
    return data.filter(row => {
      const matchesGlobal = Object.values(row).some(val => 
        String(val).toLowerCase().includes(globalFilter.toLowerCase())
      );
      const matchesStatus = statusFilter === 'todos' || row.estado === statusFilter;
      return matchesGlobal && matchesStatus;
    });
  }, [data, globalFilter, statusFilter]);

  const table = useReactTable({
    data: filteredData,
    columns,
    state: {
      globalFilter,
    },
    onGlobalFilterChange: setGlobalFilter,
    getCoreRowModel: getCoreRowModel(),
    getFilteredRowModel: getFilteredRowModel(),
    getPaginationRowModel: getPaginationRowModel(),
    getSortedRowModel: getSortedRowModel(),
    meta: {
      onEdit: handleEdit,
      onDelete: handleDelete,
    },
  });

  return (
    <div className="fade-in">
      <VehiculoFormModal 
        isOpen={isModalOpen} 
        onClose={() => {
          setIsModalOpen(false);
          setVehicleToEdit(null);
        }} 
        onSave={fetchData} 
        vehicleToEdit={vehicleToEdit}
      />

      {/* Header Section */}
      <div className="d-flex justify-content-between align-items-center mb-2">
        <div>
          <h4 className="mb-0 fw-bold" style={{ color: 'var(--text-dark)' }}>Inventario de Vehículos</h4>
          <p className="mb-0 text-muted small">Gestión completa del stock y disponibilidad de unidades.</p>
        </div>
        <button 
          className="btn btn-gold px-4" 
          onClick={() => setIsModalOpen(true)}
        >
          <i className="bi bi-plus-lg me-1"></i> Nuevo Vehículo
        </button>
      </div>
      
      <div className="accent-bar mb-4"></div>

      {/* Filter Bar */}
      <div className="card card-custom p-3 mb-4 shadow-sm border-0" style={{ borderRadius: '12px' }}>
        <div className="row g-3">
          <div className="col-md-6 col-lg-8">
            <div className="input-group">
              <span className="input-group-text bg-transparent border-end-0" style={{ border: '1px solid #e8dfe1' }}>
                <i className="bi bi-search text-muted"></i>
              </span>
              <input 
                type="text" 
                className="form-control border-start-0" 
                placeholder="Buscar por patente, modelo, marca o VIN..." 
                value={globalFilter}
                onChange={e => setGlobalFilter(e.target.value)}
                style={{ border: '1px solid #e8dfe1' }}
              />
            </div>
          </div>
          <div className="col-md-3 col-lg-2">
            <select 
              className="form-select" 
              value={statusFilter}
              onChange={e => setStatusFilter(e.target.value)}
              style={{ border: '1px solid #e8dfe1' }}
            >
              <option value="todos">Todos los Estados</option>
              <option value="Nuevo">Nuevo</option>
              <option value="Usado">Usado</option>
            </select>
          </div>
          <div className="col-md-3 col-lg-2">
            <button 
              className="btn btn-outline-custom w-100" 
              onClick={() => { setGlobalFilter(''); setStatusFilter('todos'); }}
            >
              <i className="bi bi-arrow-clockwise me-1"></i> Limpiar
            </button>
          </div>
        </div>
      </div>

      {/* Table Section */}
      <div className="card shadow-sm border-0" style={{ borderRadius: '12px', background: '#fff' }}>
        <div className="card-body p-0">
          <div className="table-responsive">
            {loading ? (
              <div className="p-5 text-center">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Cargando...</span>
                </div>
                <p className="mt-2 text-muted small">Sincronizando con el servidor...</p>
              </div>
            ) : (
              <table className="table table-hover align-middle mb-0">
                <thead className="bg-light">
                  {table.getHeaderGroups().map(headerGroup => (
                    <tr key={headerGroup.id}>
                      {headerGroup.headers.map(header => (
                        <th 
                          key={header.id} 
                          className="py-3 ps-4 text-muted" 
                          style={{ fontSize: '12px', fontWeight: 600, textTransform: 'uppercase', cursor: 'pointer' }}
                          onClick={header.column.getToggleSortingHandler()}
                        >
                          {flexRender(header.column.columnDef.header, header.getContext())}
                          {{
                            asc: ' 🔼',
                            desc: ' 🔽',
                          }[header.column.getIsSorted()] ?? null}
                        </th>
                      ))}
                    </tr>
                  ))}
                </thead>
                <tbody>
                  {table.getRowModel().rows.length > 0 ? (
                    table.getRowModel().rows.map(row => (
                      <tr key={row.id}>
                        {row.getVisibleCells().map(cell => (
                          <td key={cell.id} className="py-3 ps-4" style={{ fontSize: '14px', color: 'var(--text-dark)' }}>
                            {flexRender(cell.column.columnDef.cell, cell.getContext())}
                          </td>
                        ))}
                      </tr>
                    ))
                  ) : (
                    <tr>
                      <td colSpan={columns.length} className="text-center py-5 text-muted">
                        <i className="bi bi-car-front d-block fs-2 mb-2 opacity-50"></i>
                        No se encontraron vehículos con los filtros aplicados.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            )}
          </div>
        </div>
        
        {!loading && table.getRowModel().rows.length > 0 && (
          <div className="card-footer bg-white py-3 d-flex justify-content-between align-items-center border-top">
            <div className="text-muted small">
              Mostrando <strong>{table.getRowModel().rows.length}</strong> de <strong>{data.length}</strong> vehículos
            </div>
            <div className="d-flex gap-2">
              <button 
                className="btn btn-outline-custom btn-sm" 
                onClick={() => table.previousPage()} 
                disabled={!table.getCanPreviousPage()}
              >
                <i className="bi bi-chevron-left"></i> Anterior
              </button>
              <button 
                className="btn btn-outline-custom btn-sm" 
                onClick={() => table.nextPage()} 
                disabled={!table.getCanNextPage()}
              >
                Siguiente <i className="bi bi-chevron-right"></i>
              </button>
            </div>
          </div>
        )}
      </div>

      <style>{`
        .fade-in {
          animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
          from { opacity: 0; transform: translateY(10px); }
          to { opacity: 1; transform: translateY(0); }
        }
        .badge-gold { background: #f9f2dc; color: #7a6310; font-weight: 500; }
        .badge-salmon { background: #fdecea; color: #9b3028; font-weight: 500; }
        .btn-gold {
          background: var(--accent-gold);
          color: var(--primary-dark);
          border: none;
          font-weight: 500;
          font-size: 13px;
          transition: all 0.2s;
        }
        .btn-gold:hover { background: #b89c45; color: var(--primary-dark); }
        .btn-outline-custom {
          border: 1px solid #d4c0c4;
          color: #5a4a4e;
          background: transparent;
          font-size: 13px;
          transition: all 0.2s;
        }
        .btn-outline-custom:hover {
          background: #f5f0f1;
          border-color: var(--accent-gold);
          color: var(--accent-gold);
        }
      `}</style>
    </div>
  );
};

export default StockPage;

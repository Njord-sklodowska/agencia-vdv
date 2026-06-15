import React, { useMemo, useState, useEffect } from 'react';
import { 
  useReactTable, 
  getCoreRowModel, 
  flexRender, 
  createColumnHelper 
} from '@tanstack/react-table';
import { inventarioApi } from '../../api/inventarioApi';

const columnHelper = createColumnHelper();

const columns = [
  columnHelper.accessor('marca_nombre', {
    header: 'Marca',
    cell: info => <span className="fw-semibold">{info.getValue() || '---'}</span>,
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
    cell: info => <span className="text-dark fw-medium">{info.getValue() ? `$${info.getValue()}` : '---'}</span>,
  }),
  columnHelper.accessor('estado', {
    header: 'Estado',
    cell: info => {
      const estado = info.getValue();
      const badgeClass = estado === 'Nuevo' || estado === 'disponible' ? 'badge-gold' : 'badge-salmon';
      return <span className={`badge ${badgeClass}`}>{estado || '---'}</span>;
    },
  }),
  columnHelper.accessor('fecha_alta', {
    header: 'Ingreso',
    cell: info => <span className="text-muted small">{info.getValue() ? new Date(info.getValue()).toLocaleDateString() : '---'}</span>,
  }),
];

const MetricCard = ({ label, value, subValue, color = 'var(--accent-gold)' }) => (
  <div className="col-md-3 col-sm-6 mb-3">
    <div className="card p-3 shadow-sm border-0" style={{ borderLeft: `4px solid ${color}`, borderRadius: '10px', background: '#fff' }}>
      <p className="text-muted small mb-1" style={{ fontSize: '12px', fontWeight: 500 }}>{label}</p>
      <h3 className="fw-bold mb-1" style={{ color: 'var(--text-dark)', fontSize: '24px' }}>{value}</h3>
      <p className="mb-0 small" style={{ color: color, fontSize: '12px' }}>
        <i className="bi bi-info-circle me-1"></i> {subValue}
      </p>
    </div>
  </div>
);

const DashboardPage = () => {
  const [vehicles, setVehicles] = useState([]);
  const [stats, setStats] = useState({
    total_vehiculos: 0,
    nuevos: 0,
    usados: 0,
    pendientes_entrega: 0,
    valor_total: 0,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [vehiclesData, statsData] = await Promise.all([
          inventarioApi.getVehiculos(),
          inventarioApi.getStats()
        ]);
        
        const results = Array.isArray(vehiclesData) ? vehiclesData : (vehiclesData.results || []);
        setVehicles(results);
        setStats(statsData);
        setError(null);
      } catch (err) {
        console.error("Dashboard fetch error:", err);
        setError("Error al sincronizar datos con el servidor.");
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const data = useMemo(() => vehicles, [vehicles]);
  
  const table = useReactTable({
    data,
    columns,
    getCoreRowModel: getCoreRowModel(),
  });

  return (
    <div className="fade-in">
      {/* Header Section */}
      <div className="d-flex justify-content-between align-items-center mb-2">
        <div>
          <h4 className="mb-0 fw-bold" style={{ color: 'var(--text-dark)' }}>Dashboard</h4>
          <p className="mb-0 text-muted small">Bienvenido de vuelta. Aquí tienes el resumen de tu concesionaria.</p>
        </div>
        <button className="btn btn-outline-custom btn-sm">
          <i className="bi bi-download me-1"></i> Exportar Reporte
        </button>
      </div>
      
      <div className="accent-bar mb-4"></div>

      {/* KPI Row */}
      <div className="row g-3 mb-4">
        <MetricCard 
          label="Vehículos en Stock" 
          value={stats.total_vehiculos} 
          subValue={`${stats.nuevos} Nuevos / ${stats.usados} Usados`} 
        />
        <MetricCard 
          label="Valor Total Stock" 
          value={`$${stats.valor_total?.toLocaleString() || '0'}`} 
          subValue="Precio de venta total" 
          color="#f4978e" 
        />
        <MetricCard 
          label="Entregas Pendientes" 
          value={stats.pendientes_entrega} 
          subValue="Vendido, no entregado" 
          color="#af42ae" 
        />
        <MetricCard 
          label="Estado del Sistema" 
          value="Sincronizado" 
          subValue="Conexión estable" 
          color="#c8ad55" 
        />
      </div>

      {/* Table Section */}
      <div className="card shadow-sm border-0" style={{ borderRadius: '12px', background: '#fff' }}>
        <div className="card-header bg-white py-3 border-bottom-0 d-flex justify-content-between align-items-center">
          <h6 className="mb-0 fw-bold" style={{ color: 'var(--text-dark)' }}>
            <i className="bi bi-car-front me-2 text-primary"></i>Últimos Ingresos al Stock
          </h6>
          {error && <span className="badge bg-danger-subtle text-danger" style={{ fontSize: '10px' }}>{error}</span>}
        </div>
        <div className="card-body p-0">
          <div className="table-responsive">
            {loading ? (
              <div className="p-5 text-center">
                <div className="spinner-border text-primary" role="status">
                  <span className="visually-hidden">Cargando...</span>
                </div>
                <p className="mt-2 text-muted small">Cargando datos del servidor...</p>
              </div>
            ) : (
              <table className="table table-hover align-middle mb-0">
                <thead className="bg-light">
                  {table.getHeaderGroups().map(headerGroup => (
                    <tr key={headerGroup.id}>
                      {headerGroup.headers.map(header => (
                        <th key={header.id} className="py-3 ps-4 text-muted" style={{ fontSize: '12px', fontWeight: 600, textTransform: 'uppercase' }}>
                          {flexRender(header.column.columnDef.header, header.getContext())}
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
                        <i className="bi bi-database-exclamation d-block fs-3 mb-2"></i>
                        No hay datos disponibles en el inventario.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            )}
          </div>
        </div>
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

export default DashboardPage;

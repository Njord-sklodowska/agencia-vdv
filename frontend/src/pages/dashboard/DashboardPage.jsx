import React, { useMemo, useState, useEffect } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
  createColumnHelper,
} from '@tanstack/react-table';
import { inventarioApi } from '../../api/inventarioApi';
import BadgeEstado from '../../components/common/BadgeEstado';

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
    cell: info => <BadgeEstado estado={info.getValue()} />,
  }),
  columnHelper.accessor('fecha_alta', {
    header: 'Ingreso',
    cell: info => <span className="text-muted small">{info.getValue() ? new Date(info.getValue()).toLocaleDateString() : '---'}</span>,
  }),
];

const MetricCard = ({ label, value, subValue, color = '#f0ad4e' }) => (
  <div className="col-md-3 col-sm-6 mb-3 metric-card">
    <div className="card p-3 shadow-sm border-0" style={{ borderLeft: `4px solid ${color}` }}>
      <p className="metric-label">{label}</p>
      <h3 className="metric-value">{value}</h3>
      <p className="metric-sub" style={{ color }}>
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
          inventarioApi.getStats(),
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
      <div className="page-header">
        <div>
          <h4 className="page-title">Dashboard</h4>
          <p className="page-subtitle">Bienvenido de vuelta. Aquí tienes el resumen de tu concesionaria.</p>
        </div>
        <button className="btn btn-outline-secondary btn-sm">
          <i className="bi bi-download me-1"></i> Exportar Reporte
        </button>
      </div>

      <div className="accent-bar mb-4"></div>

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
          label="Sucursales Activas"
          value="Sincronizado"
          subValue="Gestión de sedes"
          color="#c8ad55"
        />
      </div>

      <div className="card shadow-sm border-0 dashboard-table-card">
        <div className="card-header bg-white py-3 border-bottom-0 d-flex justify-content-between align-items-center">
          <h6 className="mb-0 fw-bold dashboard-table-title">
            <i className="bi bi-car-front me-2 text-primary"></i>Últimos Ingresos al Stock
          </h6>
          {error && <span className="badge bg-danger-subtle text-danger dashboard-error-badge">{error}</span>}
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
                        <th key={header.id} className="dashboard-table-th">
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
                          <td key={cell.id} className="dashboard-table-td">
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
    </div>
  );
};

export default DashboardPage;

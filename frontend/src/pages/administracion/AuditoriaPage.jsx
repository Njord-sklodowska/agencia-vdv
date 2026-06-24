import React, { useState, useEffect } from 'react';
import AuditoriaTabla from '../../components/administracion/AuditoriaTabla';
import { useAuditoria } from '../../hooks/useAuditoria';
import Spinner from '../../components/common/Spinner';

const AuditoriaPage = () => {
  const {
    logs,
    totalCount,
    isLoading,
    error,
    pagination,
    filters,
    sorting,
    updateFilter,
    setPage,
    setPageSize,
    toggleSort,
  } = useAuditoria();

  const [searchQuery, setSearchQuery] = useState(filters.search);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchQuery !== filters.search) {
        updateFilter({ search: searchQuery });
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [searchQuery, filters.search, updateFilter]);

  return (
    <div className="container-fluid page-container">
      <div className="page-header">
        <div>
          <h2 className="page-title">Visor de Auditoría</h2>
          <p className="page-subtitle">Registro detallado de todas las actividades del sistema</p>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger alert-danger-custom" role="alert">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="card filter-card">
        <div className="card-body">
          <div className="row g-3">
            <div className="col-md-4">
              <label className="form-label filter-label">Búsqueda General</label>
              <div className="input-group input-search">
                <span className="input-group-text">
                  <i className="bi bi-search text-muted"></i>
                </span>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Buscar en logs..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                />
              </div>
            </div>

            <div className="col-md-2">
              <label className="form-label filter-label">Acción</label>
              <select
                className="form-select"
                value={filters.accion}
                onChange={(e) => updateFilter({ accion: e.target.value })}
              >
                <option value="">Todas</option>
                <option value="CREAR">Crear</option>
                <option value="MODIFICAR">Modificar</option>
                <option value="ELIMINAR">Eliminar</option>
                <option value="LOGIN">Login</option>
                <option value="LOGOUT">Logout</option>
              </select>
            </div>

            <div className="col-md-3">
              <label className="form-label filter-label">Usuario</label>
              <input
                type="text"
                className="form-control"
                placeholder="Username o Email..."
                value={filters.usuario}
                onChange={(e) => updateFilter({ usuario: e.target.value })}
              />
            </div>

            <div className="col-md-3 d-flex gap-2 align-items-end">
              <div className="flex-grow-1">
                <label className="form-label filter-label">Desde</label>
                <input
                  type="date"
                  className="form-control"
                  value={filters.fecha_desde}
                  onChange={(e) => updateFilter({ fecha_desde: e.target.value })}
                />
              </div>
              <div className="flex-grow-1">
                <label className="form-label filter-label">Hasta</label>
                <input
                  type="date"
                  className="form-control"
                  value={filters.fecha_hasta}
                  onChange={(e) => updateFilter({ fecha_hasta: e.target.value })}
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="spinner-wrapper">
        {isLoading && (
          <div className="spinner-overlay">
            <Spinner size="lg" />
          </div>
        )}

        <div className={isLoading ? 'content-loading' : 'content-loaded'}>
          <AuditoriaTabla
            data={logs}
            totalCount={totalCount}
            pagination={pagination}
            setPage={setPage}
            setPageSize={setPageSize}
            filters={filters}
            sorting={sorting}
            toggleSort={toggleSort}
          />
        </div>
      </div>
    </div>
  );
};

export default AuditoriaPage;

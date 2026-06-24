import React, { useState, useEffect } from 'react';
import UsuarioTabla from '../../components/administracion/UsuarioTabla';
import { useUsuarios } from '../../hooks/useUsuarios';
import Spinner from '../../components/common/Spinner';

const UsuariosPage = () => {
  const {
    usuarios,
    totalCount,
    isLoading,
    error,
    pagination,
    filters,
    updateFilter,
    setPage,
    setPageSize,
  } = useUsuarios();

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
          <h2 className="page-title">Gestión de Usuarios</h2>
          <p className="page-subtitle">Administración de identidades, roles y accesos al sistema</p>
        </div>
        <div>
          <button className="btn btn-gold">
            + Nuevo Usuario
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger alert-danger-custom" role="alert">
          <strong>Error:</strong> {error}
        </div>
      )}

      <div className="card filter-card">
        <div className="card-body">
          <div className="row align-items-center">
            <div className="col-md-4">
              <div className="input-group input-search">
                <span className="input-group-text">
                  <i className="bi bi-search text-muted"></i>
                </span>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Buscar usuario, email..."
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
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
          <UsuarioTabla
            usuarios={usuarios}
            totalCount={totalCount}
            pagination={pagination}
            setPage={setPage}
            setPageSize={setPageSize}
            filters={filters}
          />
        </div>
      </div>
    </div>
  );
};

export default UsuariosPage;

import React, { useState, useEffect } from 'react';
import { useTraslados } from '../../hooks/useTraslados';
import TrasladoTabla from '../../components/inventario/TrasladoTabla';
import TrasladoFormModal from '../../components/inventario/TrasladoFormModal';
import TrasladoViewModal from '../../components/inventario/TrasladoViewModal';
import Spinner from '../../components/common/Spinner';

const TrasladosPage = () => {
  const {
    traslados,
    totalCount,
    loading,
    pagination,
    filters,
    sorting,
    handlePageChange,
    handlePageSizeChange,
    handleSearch,
    handleFilterChange,
    toggleSort,
    addTraslado,
    updateTraslado,
    deleteTraslado,
    confirmarTraslado,
    cancelarTraslado,
    refresh
  } = useTraslados();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedTraslado, setSelectedTraslado] = useState(null);
  const [searchTerm, setSearchTerm] = useState(filters.search);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm !== filters.search) {
        handleSearch(searchTerm);
      }
    }, 300);
    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  const handleOpenModal = (traslado = null) => {
    setSelectedTraslado(traslado);
    setIsModalOpen(true);
  };

  const handleOpenViewModal = (traslado) => {
    setSelectedTraslado(traslado);
    setIsViewModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedTraslado(null);
    setIsModalOpen(false);
  };

  const handleCloseViewModal = () => {
    setSelectedTraslado(null);
    setIsViewModalOpen(false);
  };

  const handleSaveTraslado = async (formData) => {
    try {
      const result = selectedTraslado
        ? await updateTraslado(selectedTraslado.id, formData)
        : await addTraslado(formData);

      if (result.success) {
        handleCloseModal();
      } else {
        alert(`Error al guardar el traslado:\n${result.error}`);
      }
    } catch (error) {
      alert('Error inesperado al guardar el traslado.');
    }
  };

  const handleConfirmar = async (traslado) => {
    if (window.confirm(`¿Confirmar la recepción del vehículo ${traslado.vehiculo_detalle} en sucursal destino?`)) {
      const result = await confirmarTraslado(traslado.id);
      if (result.success) {
        alert('Traslado completado exitosamente. Sucursal del vehículo actualizada.');
      } else {
        alert(`Error al confirmar: ${result.error}`);
      }
    }
  };

  const handleCancelar = async (traslado) => {
    if (window.confirm(`¿Estás seguro de que deseas cancelar el traslado del vehículo ${traslado.vehiculo_detalle}?`)) {
      const result = await cancelarTraslado(traslado.id);
      if (result.success) {
        alert('Traslado cancelado.');
      } else {
        alert(`Error al cancelar: ${result.error}`);
      }
    }
  };

  return (
    <div className="container-fluid page-container">
      <div className="page-header">
        <div>
          <h3 className="page-title">Gestión de Traslados</h3>
          <p className="page-subtitle">Control de movimiento de vehículos entre sucursales.</p>
        </div>
        <button className="btn btn-gold" onClick={() => handleOpenModal()}>
          <i className="bi bi-truck me-2"></i>
          Nuevo Traslado
        </button>
      </div>

      <div className="card filter-card">
        <div className="card-body">
          <div className="row g-3 align-items-center">
            <div className="col-md-4">
              <div className="input-group input-search">
                <span className="input-group-text">
                  <i className="bi bi-search text-muted"></i>
                </span>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Buscar por patente, VIN, motivo..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div className="col-md-3">
              <select
                className="form-select"
                value={filters.estado}
                onChange={(e) => handleFilterChange('estado', e.target.value)}
              >
                <option value="">Todos los Estados</option>
                <option value="pendiente">Pendiente</option>
                <option value="completado">Completado</option>
                <option value="cancelado">Cancelado</option>
              </select>
            </div>
            <div className="col-md-3">
              <div className="d-flex gap-2">
                <select
                  className="form-select"
                  value={filters.sucursal_origen}
                  onChange={(e) => handleFilterChange('sucursal_origen', e.target.value)}
                >
                  <option value="">Cualquier Origen</option>
                </select>
                <select
                  className="form-select"
                  value={filters.sucursal_destino}
                  onChange={(e) => handleFilterChange('sucursal_destino', e.target.value)}
                >
                  <option value="">Cualquier Destino</option>
                </select>
              </div>
            </div>
            <div className="col-md-2 card-total-badge">
              Total: <strong>{totalCount}</strong>
            </div>
          </div>
        </div>
      </div>

      {loading ? (
        <div className="d-flex justify-content-center align-items-center py-5">
          <Spinner />
        </div>
      ) : (
        <TrasladoTabla
          traslados={traslados}
          totalCount={totalCount}
          pagination={pagination}
          sorting={sorting}
          setPage={handlePageChange}
          setPageSize={handlePageSizeChange}
          toggleSort={toggleSort}
          filters={filters}
          onView={handleOpenViewModal}
          onEdit={handleOpenModal}
          onDelete={(t) => {
            if (window.confirm('¿Eliminar registro de traslado?')) {
              deleteTraslado(t.id);
            }
          }}
          onConfirmar={handleConfirmar}
          onCancelar={handleCancelar}
        />
      )}

      <TrasladoFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSaveTraslado}
        initialData={selectedTraslado}
      />

      <TrasladoViewModal
        isOpen={isViewModalOpen}
        onClose={handleCloseViewModal}
        data={selectedTraslado}
      />
    </div>
  );
};

export default TrasladosPage;

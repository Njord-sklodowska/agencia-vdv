import React, { useState, useEffect } from 'react';
import { useTalleres } from '../../hooks/useTalleres';
import TallerTabla from '../../components/inventario/TallerTabla';
import TallerFormModal from '../../components/inventario/TallerFormModal';
import TallerViewModal from '../../components/inventario/TallerViewModal';
import Spinner from '../../components/common/Spinner';

const TalleresPage = () => {
  const {
    talleres,
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
    addTaller,
    updateTaller,
    deleteTaller,
    refresh
  } = useTalleres();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedTaller, setSelectedTaller] = useState(null);
  const [searchTerm, setSearchTerm] = useState(filters.search);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm !== filters.search) {
        handleSearch(searchTerm);
      }
    }, 300);
    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  const handleOpenModal = (taller = null) => {
    setSelectedTaller(taller);
    setIsModalOpen(true);
  };

  const handleOpenViewModal = (taller) => {
    setSelectedTaller(taller);
    setIsViewModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedTaller(null);
    setIsModalOpen(false);
  };

  const handleCloseViewModal = () => {
    setSelectedTaller(null);
    setIsViewModalOpen(false);
  };

  const handleSaveTaller = async (formData) => {
    if (selectedTaller) {
      await updateTaller(selectedTaller.id, formData);
    } else {
      await addTaller(formData);
    }
    handleCloseModal();
  };

  return (
    <div className="container-fluid page-container">
      <div className="page-header">
        <div>
          <h3 className="page-title">Gestión de Talleres</h3>
          <p className="page-subtitle">Administración de talleres evaluadores y centros de servicio.</p>
        </div>
        <button className="btn btn-gold" onClick={() => handleOpenModal()}>
          <i className="bi bi-plus-lg me-2"></i>
          Nuevo Taller
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
                  placeholder="Buscar taller por nombre, dirección..."
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
                <option value="activo">Activo</option>
                <option value="inactivo">Inactivo</option>
              </select>
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
        <TallerTabla
          talleres={talleres}
          totalCount={totalCount}
          pagination={pagination}
          sorting={sorting}
          setPage={handlePageChange}
          setPageSize={handlePageSizeChange}
          toggleSort={toggleSort}
          filters={filters}
          onView={handleOpenViewModal}
          onEdit={handleOpenModal}
          onDelete={(taller) => {
            if (window.confirm(`¿Eliminar el taller ${taller.nombre}?`)) {
              deleteTaller(taller.id);
            }
          }}
        />
      )}

      <TallerFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSaveTaller}
        initialData={selectedTaller}
      />

      <TallerViewModal
        isOpen={isViewModalOpen}
        onClose={handleCloseViewModal}
        data={selectedTaller}
      />
    </div>
  );
};

export default TalleresPage;

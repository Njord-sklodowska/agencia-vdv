import React, { useState, useEffect } from 'react';
import { useSucursales } from '../../hooks/useSucursales';
import SucursalTabla from '../../components/inventario/SucursalTabla';
import SucursalFormModal from '../../components/inventario/SucursalFormModal';
import SucursalViewModal from '../../components/inventario/SucursalViewModal';
import Spinner from '../../components/common/Spinner';

const SucursalesPage = () => {
  const {
    sucursales,
    totalCount,
    loading,
    pagination,
    filters,
    sorting,
    provincias,
    handlePageChange,
    handlePageSizeChange,
    handleSearch,
    handleFilterChange,
    toggleSort,
    addSucursal,
    updateSucursal,
    deleteSucursal,
    refresh
  } = useSucursales();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedSucursal, setSelectedSucursal] = useState(null);
  const [searchTerm, setSearchTerm] = useState(filters.search);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm !== filters.search) {
        handleSearch(searchTerm);
      }
    }, 300);
    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  const handleOpenModal = (sucursal = null) => {
    setSelectedSucursal(sucursal);
    setIsModalOpen(true);
  };

  const handleOpenViewModal = (sucursal) => {
    setSelectedSucursal(sucursal);
    setIsViewModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedSucursal(null);
    setIsModalOpen(false);
  };

  const handleCloseViewModal = () => {
    setSelectedSucursal(null);
    setIsViewModalOpen(false);
  };

  const handleSaveSucursal = async (formData) => {
    try {
      const result = selectedSucursal
        ? await updateSucursal(selectedSucursal.id, formData)
        : await addSucursal(formData);

      if (result.success) {
        handleCloseModal();
      } else {
        alert(`Error al guardar la sucursal:\n${result.error}`);
      }
    } catch (error) {
      alert('Error inesperado al guardar la sucursal.');
    }
  };

  return (
    <div className="container-fluid page-container">
      <div className="page-header">
        <div>
          <h3 className="page-title">Gestión de Sucursales</h3>
          <p className="page-subtitle">Administración de los puntos de venta y centros operativos.</p>
        </div>
        <button className="btn btn-gold" onClick={() => handleOpenModal()}>
          <i className="bi bi-building-plus-fill me-2"></i>
          Nueva Sucursal
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
                  placeholder="Buscar sucursal por nombre, ciudad..."
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
                <option value="activa">Activa</option>
                <option value="inactiva">Inactiva</option>
              </select>
            </div>
            <div className="col-md-3">
              <select
                className="form-select"
                value={filters.provincia}
                onChange={(e) => handleFilterChange('provincia', e.target.value)}
              >
                <option value="">Todas las Provincias</option>
                {provincias.map(prov => (
                  <option key={prov} value={prov}>{prov}</option>
                ))}
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
        <SucursalTabla
          sucursales={sucursales}
          totalCount={totalCount}
          pagination={pagination}
          sorting={sorting}
          setPage={handlePageChange}
          setPageSize={handlePageSizeChange}
          toggleSort={toggleSort}
          filters={filters}
          onView={handleOpenViewModal}
          onEdit={handleOpenModal}
          onDelete={(sucursal) => {
            if (window.confirm(`¿Eliminar la sucursal ${sucursal.nombre}?`)) {
              deleteSucursal(sucursal.id);
            }
          }}
        />
      )}

      <SucursalFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSaveSucursal}
        initialData={selectedSucursal}
      />

      <SucursalViewModal
        isOpen={isViewModalOpen}
        onClose={handleCloseViewModal}
        data={selectedSucursal}
      />
    </div>
  );
};

export default SucursalesPage;

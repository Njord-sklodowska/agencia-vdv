import React, { useState, useEffect } from 'react';
import { useClientes } from '../../hooks/useClientes';
import ClienteTabla from '../../components/clientes/ClienteTabla';
import ClienteFormModal from '../../components/clientes/ClienteFormModal';
import ClienteViewModal from '../../components/clientes/ClienteViewModal';
import Spinner from '../../components/common/Spinner';

const ClientesPage = () => {
  const {
    clientes,
    totalCount,
    loading,
    pagination,
    filters,
    sorting,
    addCliente,
    updateCliente,
    deleteCliente,
    handlePageChange,
    handlePageSizeChange,
    handleSearch,
    handleFilterChange,
    toggleSort,
    refresh
  } = useClientes();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedCliente, setSelectedCliente] = useState(null);
  const [searchTerm, setSearchTerm] = useState(filters.search);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm !== filters.search) {
        handleSearch(searchTerm);
      }
    }, 300);
    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  const handleOpenModal = (cliente = null) => {
    setSelectedCliente(cliente);
    setIsModalOpen(true);
  };

  const handleOpenViewModal = (cliente) => {
    setSelectedCliente(cliente);
    setIsViewModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedCliente(null);
    setIsModalOpen(false);
  };

  const handleCloseViewModal = () => {
    setSelectedCliente(null);
    setIsViewModalOpen(false);
  };

  const handleSaveCliente = async (formData) => {
    if (selectedCliente) {
      await updateCliente(selectedCliente.id, formData);
    } else {
      await addCliente(formData);
    }
    handleCloseModal();
  };

  const handleDeleteCliente = async (cliente) => {
    if (!window.confirm(`¿Estás seguro de que deseas eliminar a ${cliente.nombre || cliente.razon_social}?`)) return;
    await deleteCliente(cliente.id);
  };

  return (
    <div className="container-fluid page-container">
      <div className="page-header">
        <div>
          <h3 className="page-title">Gestión de Clientes</h3>
          <p className="page-subtitle">Administración de personas físicas y jurídicas.</p>
        </div>
        <button
          className="btn btn-gold"
          onClick={() => handleOpenModal()}
        >
          <i className="bi bi-person-plus-fill me-2"></i>
          Nuevo Cliente
        </button>
      </div>

      <div className="card filter-card">
        <div className="card-body">
          <div className="row g-3 align-items-center">
            <div className="col-md-3">
              <div className="input-group input-search">
                <span className="input-group-text">
                  <i className="bi bi-search text-muted"></i>
                </span>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Buscar por DNI, CUIT, nombre..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div className="col-md-3">
              <div className="input-group input-search">
                <span className="input-group-text">
                  <i className="bi bi-telephone text-muted"></i>
                </span>
                <input
                  type="text"
                  className="form-control"
                  placeholder="Buscar por teléfono..."
                  value={filters.telefono}
                  onChange={(e) => handleFilterChange('telefono', e.target.value)}
                />
              </div>
            </div>
            <div className="col-md-2">
              <select
                className="form-select"
                value={filters.tipo_persona}
                onChange={(e) => handleFilterChange('tipo_persona', e.target.value)}
              >
                <option value="">Todos los Tipos</option>
                <option value="fisica">Física</option>
                <option value="juridica">Jurídica</option>
              </select>
            </div>
            <div className="col-md-2">
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
        <ClienteTabla
          clientes={clientes}
          totalCount={totalCount}
          pagination={pagination}
          sorting={sorting}
          setPage={handlePageChange}
          setPageSize={handlePageSizeChange}
          toggleSort={toggleSort}
          filters={filters}
          onView={handleOpenViewModal}
          onEdit={handleOpenModal}
          onDelete={handleDeleteCliente}
        />
      )}

      <ClienteFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSaveCliente}
        initialData={selectedCliente}
      />

      <ClienteViewModal
        isOpen={isViewModalOpen}
        onClose={handleCloseViewModal}
        cliente={selectedCliente}
      />
    </div>
  );
};

export default ClientesPage;

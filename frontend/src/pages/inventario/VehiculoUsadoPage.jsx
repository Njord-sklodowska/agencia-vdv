import React, { useState, useEffect } from 'react';
import { useVehiculoUsados } from '../../hooks/useVehiculoUsados';
import VehiculoUsadoTabla from '../../components/inventario/VehiculoUsadoTabla';
import VehiculoUsadoForm from '../../components/inventario/VehiculoUsadoForm';
import VehiculoUsadoViewModal from '../../components/inventario/VehiculoUsadoViewModal';
import Spinner from '../../components/common/Spinner';
import { inventarioApi } from '../../api/inventarioApi';
import { usuariosApi } from '../../api/usuariosApi';

const VehiculoUsadoPage = () => {
  const {
    vehiculosUsados,
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
    addVehiculoUsado,
    updateVehiculoUsado,
    deleteVehiculoUsado,
    refresh
  } = useVehiculoUsados();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedUsado, setSelectedUsado] = useState(null);
  const [searchTerm, setSearchTerm] = useState(filters.search);
  const [talleres, setTalleres] = useState([]);
  const [usuarios, setUsuarios] = useState([]);

  useEffect(() => {
    const loadFilters = async () => {
      try {
        const [tData, uData] = await Promise.all([
          inventarioApi.getTalleres(),
          usuariosApi.getUsers()
        ]);
        setTalleres(tData.results || tData);
        setUsuarios(uData.results || uData);
      } catch (error) {
        console.error('Error loading filters:', error);
      }
    };
    loadFilters();
  }, []);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm !== filters.search) {
        handleSearch(searchTerm);
      }
    }, 300);
    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  const handleOpenModal = (usado = null) => {
    setSelectedUsado(usado);
    setIsModalOpen(true);
  };

  const handleOpenViewModal = (usado) => {
    setSelectedUsado(usado);
    setIsViewModalOpen(true);
  };

  const handleCloseModal = () => {
    setSelectedUsado(null);
    setIsModalOpen(false);
  };

  const handleCloseViewModal = () => {
    setSelectedUsado(null);
    setIsViewModalOpen(false);
  };

  const handleSaveUsado = async (formData) => {
    try {
      const result = selectedUsado
        ? await updateVehiculoUsado(selectedUsado.id, formData)
        : await addVehiculoUsado(formData);

      if (result.success) {
        handleCloseModal();
      } else {
        alert(`Error al guardar:\n${result.error}`);
      }
    } catch (error) {
      alert('Error inesperado al guardar la evaluación.');
    }
  };

  return (
    <div className="container-fluid page-container">
      <div className="page-header">
        <div>
          <h3 className="page-title">Evaluaciones de Vehículos Usados</h3>
          <p className="page-subtitle">Gestión de tasaciones y evaluaciones técnicas de ingresados.</p>
        </div>
        <button
          className="btn btn-gold"
          onClick={() => handleOpenModal()}
        >
          <i className="bi bi-plus-circle-fill me-2"></i>
          Nueva Evaluación
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
                  placeholder="Buscar por patente, VIN, observaciones..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
              </div>
            </div>
            <div className="col-md-3">
              <select
                className="form-select"
                value={filters.taller}
                onChange={(e) => handleFilterChange('taller', e.target.value)}
              >
                <option value="">Todos los Talleres</option>
                {talleres.map(t => (
                  <option key={t.id} value={t.id}>{t.nombre}</option>
                ))}
              </select>
            </div>
            <div className="col-md-3">
              <select
                className="form-select"
                value={filters.usuario_autoriza}
                onChange={(e) => handleFilterChange('usuario_autoriza', e.target.value)}
              >
                <option value="">Todos los Autorizadores</option>
                {usuarios.map(u => (
                  <option key={u.id} value={u.id}>{u.get_full_name || u.username}</option>
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
        <VehiculoUsadoTabla
          vehiculosUsados={vehiculosUsados}
          totalCount={totalCount}
          pagination={pagination}
          sorting={sorting}
          setPage={handlePageChange}
          setPageSize={handlePageSizeChange}
          toggleSort={toggleSort}
          filters={filters}
          onView={handleOpenViewModal}
          onEdit={handleOpenModal}
          onDelete={(u) => {
            if (window.confirm(`¿Estás seguro de que deseas eliminar la evaluación del vehículo ${u.vehiculo_detalle}?`)) {
              deleteVehiculoUsado(u.id);
            }
          }}
        />
      )}

      {isModalOpen && (
        <VehiculoUsadoForm
          isOpen={isModalOpen}
          onClose={handleCloseModal}
          onSubmit={handleSaveUsado}
          initialData={selectedUsado}
        />
      )}

      <VehiculoUsadoViewModal
        isOpen={isViewModalOpen}
        onClose={handleCloseViewModal}
        data={selectedUsado}
      />
    </div>
  );
};

export default VehiculoUsadoPage;

import React, { useState, useEffect } from 'react';
import FiltrosStock from '../../components/inventario/FiltrosStock';
import VehiculoTabla from '../../components/inventario/VehiculoTabla';
import VehiculoFormModal from '../../components/inventario/VehiculoFormModal';
import VehiculoViewModal from '../../components/inventario/VehiculoViewModal';
import { useVehiculos } from '../../hooks/useVehiculos';
import Spinner from '../../components/common/Spinner';
import Swal from 'sweetalert2';

const StockPage = () => {
  const {
    vehicles,
    totalCount,
    isLoading,
    error,
    pagination,
    filters,
    marcas,
    modelos,
    handlePageChange,
    handlePageSizeChange,
    handleSearch,
    handleFilterChange,
    toggleSort,
    sorting,
    refresh,
    deleteVehiculo,
  } = useVehiculos();

  const [searchTerm, setSearchTerm] = useState(filters.search);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [vehicleToEdit, setVehicleToEdit] = useState(null);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [selectedVehicle, setSelectedVehicle] = useState(null);

  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm !== filters.search) {
        handleSearch(searchTerm);
      }
    }, 300);
    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm]);

  const handleOpenCreate = () => {
    setVehicleToEdit(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (vehicle) => {
    setVehicleToEdit(vehicle);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setVehicleToEdit(null);
  };

  const handleOpenView = (vehicle) => {
    setSelectedVehicle(vehicle);
    setIsViewModalOpen(true);
  };

  const handleCloseViewModal = () => {
    setIsViewModalOpen(false);
    setSelectedVehicle(null);
  };

  const handleDelete = async (vehicle) => {
    const result = await Swal.fire({
      title: '¿Estás seguro?',
      text: `Vas a desactivar el vehículo ${vehicle.patente || vehicle.vin}. Esta acción no se puede deshacer fácilmente.`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, desactivar',
      cancelButtonText: 'Cancelar',
    });

    if (result.isConfirmed) {
      try {
        await deleteVehiculo(vehicle.id);
        Swal.fire('Desactivado', 'El vehículo ha sido desactivado correctamente', 'success');
      } catch (error) {
        Swal.fire('Error', 'No se pudo desactivar el vehículo', 'error');
      }
    }
  };

  return (
    <div className="container-fluid page-container">
      <div className="page-header">
        <div>
          <h2 className="page-title">Gestión de Stock</h2>
          <p className="page-subtitle">Visualización y control de vehículos en inventario</p>
        </div>
        <div>
          <button className="btn btn-gold" onClick={handleOpenCreate}>
            + Nuevo Vehículo
          </button>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger alert-danger-custom" role="alert">
          <strong>Error:</strong> {error}
        </div>
      )}

      <FiltrosStock
        filters={filters}
        updateFilter={handleFilterChange}
        handleSearch={(val) => setSearchTerm(val)}
        marcas={marcas}
        modelos={modelos}
      />

      <div className="spinner-wrapper">
        {isLoading && (
          <div className="spinner-overlay">
            <Spinner size="lg" />
          </div>
        )}

        <div className={isLoading ? 'content-loading' : 'content-loaded'}>
          <VehiculoTabla
            vehicles={vehicles}
            totalCount={totalCount}
            pagination={pagination}
            sorting={sorting}
            setPage={handlePageChange}
            setPageSize={handlePageSizeChange}
            toggleSort={toggleSort}
            filters={filters}
            onEdit={handleOpenEdit}
            onView={handleOpenView}
            onDelete={handleDelete}
          />
        </div>
      </div>

      <VehiculoFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSave={refresh}
        vehicleToEdit={vehicleToEdit}
      />

      <VehiculoViewModal
        isOpen={isViewModalOpen}
        onClose={handleCloseViewModal}
        vehiculo={selectedVehicle}
      />
    </div>
  );
};

export default StockPage;

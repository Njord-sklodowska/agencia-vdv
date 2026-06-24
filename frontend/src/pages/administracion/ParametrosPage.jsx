import React, { useState, useEffect } from 'react';
import ParametroTabla from '../../components/administracion/ParametroTabla';
import ParametroFormModal from '../../components/administracion/ParametroFormModal';
import { useParametros } from '../../hooks/useParametros';
import Spinner from '../../components/common/Spinner';
import Swal from 'sweetalert2';

const ParametrosPage = () => {
  const {
    parametros,
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
    addParametro,
    updateParametro,
    deleteParametro,
    refresh,
  } = useParametros();

  const [isModalOpen, setIsModalOpen] = useState(false);
  const [parametroToEdit, setParametroToEdit] = useState(null);
  const [searchQuery, setSearchQuery] = useState(filters.search);

  useEffect(() => {
    const timer = setTimeout(() => {
      if (searchQuery !== filters.search) {
        updateFilter({ search: searchQuery });
      }
    }, 300);
    return () => clearTimeout(timer);
  }, [searchQuery, filters.search, updateFilter]);

  const handleOpenEdit = (parametro) => {
    setParametroToEdit(parametro);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setParametroToEdit(null);
  };

  const handleSaveParametro = async (formData) => {
    try {
      let result;
      if (parametroToEdit) {
        result = await updateParametro(parametroToEdit.id, formData);
        if (result.success) {
          Swal.fire('Actualizado', 'El parámetro ha sido actualizado correctamente', 'success');
        }
      } else {
        result = await addParametro(formData);
        if (result.success) {
          Swal.fire('Creado', 'El parámetro ha sido creado correctamente', 'success');
        }
      }
      if (result.success) {
        handleCloseModal();
      } else {
        const errorMsg = result.error?.response?.data
          ? JSON.stringify(result.error.response.data)
          : 'No se pudo guardar el parámetro';
        Swal.fire('Error', errorMsg, 'error');
      }
    } catch (error) {
      Swal.fire('Error', 'Error inesperado al guardar el parámetro', 'error');
    }
  };

  const handleDelete = async (parametro) => {
    const result = await Swal.fire({
      title: '¿Estás seguro?',
      text: `Vas a eliminar el parámetro ${parametro.nombre_parametro}. Esta acción puede afectar la configuración del sistema.`,
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar',
    });

    if (result.isConfirmed) {
      try {
        await deleteParametro(parametro.id);
        Swal.fire('Eliminado', 'El parámetro ha sido eliminado correctamente', 'success');
      } catch (error) {
        Swal.fire('Error', 'No tienes permisos para eliminar este parámetro o ocurrió un error', 'error');
      }
    }
  };

  return (
    <div className="container-fluid page-container">
      <div className="page-header">
        <div>
          <h2 className="page-title">Parámetros del Sistema</h2>
          <p className="page-subtitle">Configuración global y variables de entorno del sistema</p>
        </div>
        <div>
          <button
            className="btn btn-gold"
            onClick={() => {
              setParametroToEdit(null);
              setIsModalOpen(true);
            }}
          >
            + Nuevo Parámetro
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
                  placeholder="Buscar parámetro o descripción..."
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
          <ParametroTabla
            data={parametros}
            totalCount={totalCount}
            pagination={pagination}
            setPage={setPage}
            setPageSize={setPageSize}
            filters={filters}
            sorting={sorting}
            toggleSort={toggleSort}
            onEdit={handleOpenEdit}
            onDelete={handleDelete}
          />
        </div>
      </div>

      <ParametroFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSave={handleSaveParametro}
        parametroToEdit={parametroToEdit}
      />
    </div>
  );
};

export default ParametrosPage;

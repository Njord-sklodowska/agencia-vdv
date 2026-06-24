import React, { useState, useEffect } from 'react';
import { inventarioApi } from '../../api/inventarioApi';
import Swal from 'sweetalert2';

const VehiculoFotos = ({ vehiculoId }) => {
  const [fotos, setFotos] = useState([]);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFoto, setSelectedFoto] = useState(null);

  const fetchFotos = async () => {
    if (!vehiculoId) return;
    try {
      const data = await inventarioApi.getVehiculoFotos(vehiculoId);
      setFotos(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error('Error loading photos:', error);
    }
  };

  useEffect(() => {
    fetchFotos();
  }, [vehiculoId]);

  const handleFileChange = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (file.size > 5 * 1024 * 1024) {
      Swal.fire('Archivo demasiado grande', 'La imagen no puede superar los 5 MB', 'error');
      return;
    }

    setIsUploading(true);
    try {
      await inventarioApi.uploadVehiculoFoto(vehiculoId, file);
      Swal.fire('Éxito', 'Foto subida correctamente', 'success');
      await fetchFotos();
    } catch (error) {
      Swal.fire('Error', 'No se pudo subir la foto', 'error');
    } finally {
      setIsUploading(false);
    }
  };

  const handleSetPortada = async (fotoId) => {
    try {
      await inventarioApi.setPortadaFoto(fotoId);
      Swal.fire({
        title: 'Portada actualizada',
        icon: 'success',
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        timer: 3000,
        timerProgressBar: true,
      });
      await fetchFotos();
    } catch (error) {
      Swal.fire('Error', 'No se pudo establecer como portada', 'error');
    }
  };

  const handleDeleteFoto = async (fotoId) => {
    const result = await Swal.fire({
      title: '¿Eliminar foto?',
      text: 'Esta acción no se puede deshacer',
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#d33',
      cancelButtonColor: '#3085d6',
      confirmButtonText: 'Sí, eliminar',
      cancelButtonText: 'Cancelar',
    });

    if (result.isConfirmed) {
      try {
        await inventarioApi.deleteVehiculoFoto(fotoId);
        Swal.fire('Eliminado', 'La foto ha sido eliminada', 'success');
        await fetchFotos();
      } catch (error) {
        Swal.fire('Error', 'No se pudo eliminar la foto', 'error');
      }
    }
  };

  return (
    <div className="mt-4">
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h6 className="fw-bold text-primary mb-0">Galería de Imágenes</h6>
        <label className="btn btn-sm btn-outline-primary mb-0">
          <i className="bi bi-cloud-upload me-1"></i> {isUploading ? 'Subiendo...' : 'Subir Foto'}
          <input 
            type="file" 
            hidden 
            accept="image/*" 
            onChange={handleFileChange} 
            disabled={isUploading}
          />
        </label>
      </div>

      {fotos.length === 0 ? (
        <div className="text-center p-4 border rounded bg-light text-muted" style={{ borderStyle: 'dashed !important' }}>
          <i className="bi bi-image mb-2 d-block fs-3"></i>
          <span className="small">No hay fotografías disponibles para este vehículo.</span>
        </div>
      ) : (
        <div className="row g-2">
          {fotos.map((foto) => (
            <div key={foto.id} className="col-3 col-md-2">
              <div className="position-relative group-foto shadow-sm border rounded overflow-hidden" style={{ height: '90px' }}>
                <img 
                  src={`${process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'}/media/${foto.archivo}`} 
                  alt="Vehículo" 
                  className="img-fluid" 
                  style={{ height: '100%', width: '100%', objectFit: 'cover', cursor: 'pointer' }}
                  onClick={() => setSelectedFoto(foto)}
                />
                
                {/* Overlay de Acciones */}
                <div className="foto-overlay d-flex flex-column align-items-center justify-content-center gap-2">
                  {!foto.es_portada && (
                    <button 
                      className="btn btn-xs btn-light rounded-circle p-1" 
                      onClick={() => handleSetPortada(foto.id)}
                      title="Marcar como portada"
                    >
                      <i className="bi bi-star-fill text-warning"></i>
                    </button>
                  )}
                  <button 
                    className="btn btn-xs btn-danger rounded-circle p-1" 
                    onClick={() => handleDeleteFoto(foto.id)}
                    title="Eliminar foto"
                  >
                    <i className="bi bi-trash"></i>
                  </button>
                </div>

                {foto.es_portada && (
                  <span className="position-absolute top-0 start-0 badge bg-warning text-dark" style={{ fontSize: '0.6rem', zIndex: 1 }}>
                    Portada
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Lightbox / Zoom Modal */}
      {selectedFoto && (
        <div 
          className="modal show d-block" 
          style={{ backgroundColor: 'rgba(0,0,0,0.9)', zIndex: 2000 }}
          onClick={() => setSelectedFoto(null)}
        >
          <div className="modal-dialog modal-dialog-centered modal-lg">
            <div className="modal-content bg-transparent border-0">
              <div className="text-end mb-2">
                <button 
                  className="btn btn-close btn-close-white" 
                  onClick={() => setSelectedFoto(null)}
                ></button>
              </div>
              <div className="text-center">
                <img 
                  src={`${process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'}/media/${selectedFoto.archivo}`} 
                  alt="Vehículo Zoom" 
                  className="img-fluid rounded shadow-lg" 
                  style={{ maxHeight: '80vh' }}
                />
                <div className="text-white mt-3 small">
                  Archivo: {selectedFoto.nombre_original || 'Imagen de vehículo'}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      <style jsx>{`
        .group-foto {
          position: relative;
          transition: transform 0.2s;
        }
        .group-foto:hover {
          transform: scale(1.05);
        }
        .foto-overlay {
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          bottom: 0;
          background: rgba(0,0,0,0.4);
          opacity: 0;
          transition: opacity 0.2s;
          z-index: 2;
        }
        .group-foto:hover .foto-overlay {
          opacity: 1;
        }
        .btn-xs {
          width: 24px;
          height: 24px;
          padding: 0;
          display: flex;
          align-items: center;
          justify-content: center;
          font-size: 0.7rem;
        }
      `}</style>
    </div>
  );
};

export default VehiculoFotos;

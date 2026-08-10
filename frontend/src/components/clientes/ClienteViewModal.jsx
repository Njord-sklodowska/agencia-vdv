import React from 'react';
import BadgeEstado from '../common/BadgeEstado';

const ClienteViewModal = ({ isOpen, onClose, cliente }) => {
  if (!isOpen || !cliente) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-view-header">
            <h5 className="modal-title fw-bold">
              <i className="bi bi-person-fill me-2"></i>Detalles del Cliente
            </h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <div className="modal-body p-4">
            <div className="row g-4">
              <div className="col-12">
                <h6 className="form-section-title">Información Principal</h6>
                <div className="row g-3">
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Tipo de Persona</label>
                    <span className="fw-medium">{cliente.tipo_persona === 'fisica' ? 'Física' : 'Jurídica'}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">DNI / CUIT</label>
                    <span className="fw-medium">{cliente.dni_cuit}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">CUIL</label>
                    <span className="fw-medium">{cliente.cuil || '---'}</span>
                  </div>
                  {cliente.tipo_persona === 'fisica' ? (
                    <>
                      <div className="col-md-6">
                        <label className="text-muted small d-block">Nombre</label>
                        <span className="fw-medium">{cliente.nombre}</span>
                      </div>
                      <div className="col-md-6">
                        <label className="text-muted small d-block">Apellido</label>
                        <span className="fw-medium">{cliente.apellido}</span>
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="col-md-6">
                        <label className="text-muted small d-block">Razón Social</label>
                        <span className="fw-medium">{cliente.razon_social}</span>
                      </div>
                      <div className="col-md-6">
                        <label className="text-muted small d-block">Nombre Fantasía</label>
                        <span className="fw-medium">{cliente.nombre_fantasia || '---'}</span>
                      </div>
                    </>
                  )}
                </div>
              </div>

              <div className="col-12">
                <h6 className="form-section-title">Contacto y Ubicación</h6>
                <div className="row g-3">
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Teléfono</label>
                    <span className="fw-medium">{cliente.telefono}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Tel. Alternativo</label>
                    <span className="fw-medium">{cliente.telefono_alternativo || '---'}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Email</label>
                    <span className="fw-medium">{cliente.email || '---'}</span>
                  </div>
                  <div className="col-md-6">
                    <label className="text-muted small d-block">Domicilio Real</label>
                    <span className="fw-medium">{cliente.domicilio_real}</span>
                  </div>
                  <div className="col-md-6">
                    <label className="text-muted small d-block">Domicilio Fiscal</label>
                    <span className="fw-medium">{cliente.domicilio_fiscal || '---'}</span>
                  </div>
                </div>
              </div>

              <div className="col-12">
                <h6 className="form-section-title">Información Adicional</h6>
                <div className="row g-3">
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Condición IVA</label>
                    <span className="fw-medium">{cliente.condicion_iva}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Estado</label>
                    <BadgeEstado estado={cliente.estado} />
                  </div>
                  {cliente.tipo_persona === 'fisica' && (
                    <>
                      <div className="col-md-4">
                        <label className="text-muted small d-block">Fecha Nacimiento</label>
                        <span className="fw-medium">{cliente.fecha_nacimiento || '---'}</span>
                      </div>
                      <div className="col-md-4">
                        <label className="text-muted small d-block">Nacionalidad</label>
                        <span className="fw-medium">{cliente.nacionalidad || '---'}</span>
                      </div>
                    </>
                  )}
                  <div className="col-12">
                    <label className="text-muted small d-block">Observaciones</label>
                    <div className="p-2 bg-light border rounded modal-content-box">
                      {cliente.observaciones || 'Sin observaciones.'}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="modal-footer bg-light">
            <button type="button" className="btn btn-secondary" onClick={onClose}>Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ClienteViewModal;

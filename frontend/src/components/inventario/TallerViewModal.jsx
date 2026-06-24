import React from 'react';
import BadgeEstado from '../common/BadgeEstado';

const TallerViewModal = ({ isOpen, onClose, data }) => {
  if (!isOpen || !data) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', zIndex: 1050 }}>
      <div className="modal-dialog modal-md modal-dialog-centered">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-view-header">
            <h5 className="modal-title fw-bold">Detalles del Taller</h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <div className="modal-body modal-view-body">
            <div className="text-center mb-4">
              <div className="bg-light d-inline-block p-3 rounded-circle mb-2">
                <i className="bi bi-wrench-adjustable fs-1 text-primary"></i>
              </div>
              <h4 className="fw-bold">{data.nombre}</h4>
              <BadgeEstado estado={data.estado} />
            </div>
            <div className="list-group list-group-flush">
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Dirección</span>
                <span className="fw-medium">{data.direccion || '---'}</span>
              </div>
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Teléfono</span>
                <span className="fw-medium">{data.telefono || '---'}</span>
              </div>
              <div className="list-group-item d-flex justify-content-between align-items-center px-0">
                <span className="text-muted small">Email</span>
                <span className="fw-medium">{data.email || '---'}</span>
              </div>
            </div>
          </div>
          <div className="modal-footer modal-view-footer">
            <button className="btn btn-secondary px-4" onClick={onClose}>Cerrar</button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TallerViewModal;

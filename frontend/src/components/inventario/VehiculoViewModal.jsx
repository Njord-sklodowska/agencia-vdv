import React from 'react';
import VehiculoFotos from './VehiculoFotos';
import BadgeEstado from '../common/BadgeEstado';

const VehiculoViewModal = ({ isOpen, onClose, vehiculo }) => {
  if (!isOpen || !vehiculo) return null;

  const labels = {
    condicion: { '0km': '0km', 'usado': 'Usado' },
    estado: { 'en_stock': 'En Stock', 'reservado': 'Reservado', 'vendido': 'Vendido' },
    combustible: { 'nafta': 'Nafta', 'diesel': 'Diesel', 'gnc': 'GNC', 'hibrido': 'Híbrido', 'electrico': 'Eléctrico' },
    transmision: { 'manual': 'Manual', 'automatica': 'Automática' },
    traccion: { 'delantera': 'Delantera', 'trasera': 'Trasera', '4x4': '4x4' },
    procedencia: { 'compra_directa': 'Compra Directa', 'parte_de_pago': 'Parte de Pago' },
  };

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}>
      <div className="modal-dialog modal-lg">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-view-header">
            <h5 className="modal-title fw-bold">
              <i className="bi bi-car-front-fill me-2"></i>Ficha Técnica del Vehículo
            </h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <div className="modal-body p-4">
            <div className="row g-4">
              <div className="col-12">
                <h6 className="form-section-title">Identificación General</h6>
                <div className="row g-3">
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Marca</label>
                    <span className="fw-medium">{vehiculo.marca_nombre || '---'}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Modelo</label>
                    <span className="fw-medium">{vehiculo.modelo_nombre || '---'}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Año</label>
                    <span className="fw-medium">{vehiculo.anio}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Patente</label>
                    <span className="fw-medium">{vehiculo.patente || 'S/P'}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">VIN / Chasis</label>
                    <span className="fw-medium">{vehiculo.vin || '---'}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Color</label>
                    <span className="fw-medium">{vehiculo.color}</span>
                  </div>
                </div>
              </div>

              <div className="col-12">
                <h6 className="form-section-title">Especificaciones Técnicas</h6>
                <div className="row g-3">
                  <div className="col-md-3">
                    <label className="text-muted small d-block">Motor</label>
                    <span className="fw-medium">{vehiculo.motor}</span>
                  </div>
                  <div className="col-md-3">
                    <label className="text-muted small d-block">Combustible</label>
                    <span className="fw-medium">{labels.combustible[vehiculo.combustible] || vehiculo.combustible}</span>
                  </div>
                  <div className="col-md-3">
                    <label className="text-muted small d-block">Transmisión</label>
                    <span className="fw-medium">{labels.transmision[vehiculo.transmision] || vehiculo.transmision}</span>
                  </div>
                  <div className="col-md-3">
                    <label className="text-muted small d-block">Tracción</label>
                    <span className="fw-medium">{labels.traccion[vehiculo.traccion] || '---'}</span>
                  </div>
                  <div className="col-md-3">
                    <label className="text-muted small d-block">Puertas</label>
                    <span className="fw-medium">{vehiculo.puertas}</span>
                  </div>
                  <div className="col-md-3">
                    <label className="text-muted small d-block">Kilometraje</label>
                    <span className="fw-medium">{vehiculo.kilometraje?.toLocaleString()} km</span>
                  </div>
                  <div className="col-md-3">
                    <label className="text-muted small d-block">Condición</label>
                    <span className="fw-medium">{labels.condicion[vehiculo.condicion_vehiculo] || vehiculo.condicion_vehiculo}</span>
                  </div>
                  <div className="col-md-3">
                    <label className="text-muted small d-block">Procedencia</label>
                    <span className="fw-medium">{labels.procedencia[vehiculo.procedencia] || '---'}</span>
                  </div>
                </div>
              </div>

              <div className="col-12">
                <h6 className="form-section-title">Estado y Comercialización</h6>
                <div className="row g-3">
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Estado Actual</label>
                    <BadgeEstado estado={vehiculo.estado} />
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Precio de Venta</label>
                    <span className="fw-bold text-dark fs-5">${vehiculo.precio?.toLocaleString()}</span>
                  </div>
                  <div className="col-md-4">
                    <label className="text-muted small d-block">Entregado</label>
                    <span className="fw-medium">{vehiculo.entregado ? 'Sí' : 'No'}</span>
                  </div>
                  <div className="col-12">
                    <label className="text-muted small d-block">Descripción Técnica / Observaciones</label>
                    <div className="p-2 bg-light border rounded modal-content-box">
                      {vehiculo.descripcion_tecnica || 'Sin descripción técnica disponible.'}
                    </div>
                  </div>
                </div>
              </div>

              <div className="col-12">
                <VehiculoFotos vehiculoId={vehiculo.id} />
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

export default VehiculoViewModal;

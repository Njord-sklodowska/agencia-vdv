import React, { useState, useEffect } from 'react';
import { inventarioApi } from '../../api/inventarioApi';
import { usuariosApi } from '../../api/usuariosApi';

const VehiculoUsadoForm = ({ isOpen, onClose, onSubmit, initialData }) => {
  const [formData, setFormData] = useState({
    vehiculo: '', taller: '', usuario_autoriza: '',
    precio_info_auto: '', porcentaje_deduccion: '', precio_tasacion_final: '',
    estado_cubierta: 'bueno', estado_motor: 'bueno', estado_chapa_pintura: 'bueno', estado_interior: 'bueno',
    fecha_evaluacion: '', fecha_ingreso: '', observaciones: '',
  });

  const [vehiculos, setVehiculos] = useState([]);
  const [talleres, setTalleres] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [loadingLists, setLoadingLists] = useState(true);

  useEffect(() => {
    const loadLists = async () => {
      try {
        const [vData, tData, uData] = await Promise.all([
          inventarioApi.getVehiculos({ condicion_vehiculo: 'usado' }),
          inventarioApi.getTalleres(),
          usuariosApi.getUsers()
        ]);
        setVehiculos(vData.results || vData);
        setTalleres(tData.results || tData);
        setUsuarios(uData.results || uData);
      } catch (error) {
        console.error('Error loading lists for form:', error);
      } finally {
        setLoadingLists(false);
      }
    };
    loadLists();
  }, []);

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      setFormData({
        vehiculo: '', taller: '', usuario_autoriza: '',
        precio_info_auto: '', porcentaje_deduccion: '', precio_tasacion_final: '',
        estado_cubierta: 'bueno', estado_motor: 'bueno', estado_chapa_pintura: 'bueno', estado_interior: 'bueno',
        fecha_evaluacion: '', fecha_ingreso: '', observaciones: '',
      });
    }
  }, [initialData, isOpen]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  if (!isOpen) return null;

  return (
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5)', backdropFilter: 'blur(4px)' }}>
      <div className="modal-dialog modal-lg modal-dialog-centered">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-header-dark">
            <h5 className="modal-title fw-bold">{initialData ? 'Editar Evaluación de Usado' : 'Nueva Evaluación de Usado'}</h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body modal-body-light">
              {loadingLists ? (
                <div className="text-center py-5">Cargando datos...</div>
              ) : (
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Vehículo Usado</label>
                    <select className="form-select" name="vehiculo" value={formData.vehiculo} onChange={handleChange} required>
                      <option value="">Seleccione un vehículo...</option>
                      {vehiculos.map(v => (
                        <option key={v.id} value={v.id}>{v.patente} - {v.marca_nombre} {v.modelo_nombre}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Taller Evaluador</label>
                    <select className="form-select" name="taller" value={formData.taller} onChange={handleChange}>
                      <option value="">Sin taller asignado</option>
                      {talleres.map(t => (
                        <option key={t.id} value={t.id}>{t.nombre}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-12">
                    <label className="form-label small fw-bold">Usuario que Autoriza</label>
                    <select className="form-select" name="usuario_autoriza" value={formData.usuario_autoriza} onChange={handleChange} required>
                      <option value="">Seleccione usuario...</option>
                      {usuarios.map(u => (
                        <option key={u.id} value={u.id}>{u.get_full_name || u.username}</option>
                      ))}
                    </select>
                  </div>

                  <hr className="my-4" />
                  <h6 className="fw-bold text-secondary mb-3"><i className="bi bi-cash-stack me-2"></i>Tasación Financiera</h6>

                  <div className="col-md-4">
                    <label className="form-label small fw-bold">Precio Info Auto</label>
                    <input type="number" step="0.01" className="form-control" name="precio_info_auto" value={formData.precio_info_auto} onChange={handleChange} />
                  </div>
                  <div className="col-md-4">
                    <label className="form-label small fw-bold">Deducción (%)</label>
                    <input type="number" step="0.01" className="form-control" name="porcentaje_deduccion" value={formData.porcentaje_deduccion} onChange={handleChange} />
                  </div>
                  <div className="col-md-4">
                    <label className="form-label small fw-bold">Tasación Final</label>
                    <input type="number" step="0.01" className="form-control fw-bold text-success" name="precio_tasacion_final" value={formData.precio_tasacion_final} onChange={handleChange} required />
                  </div>

                  <hr className="my-4" />
                  <h6 className="fw-bold text-secondary mb-3"><i className="bi bi-gear-wide-connected me-2"></i>Estado Técnico</h6>

                  {['motor', 'cubierta', 'chapa_pintura', 'interior'].map(campo => (
                    <div key={campo} className="col-md-3">
                      <label className="form-label small fw-bold">{campo === 'chapa_pintura' ? 'Chapa/Pintura' : campo.charAt(0).toUpperCase() + campo.slice(1)}</label>
                      <select className="form-select" name={`estado_${campo}`} value={formData[`estado_${campo}`]} onChange={handleChange}>
                        <option value="bueno">Bueno</option>
                        <option value="regular">Regular</option>
                        <option value="malo">Malo</option>
                      </select>
                    </div>
                  ))}

                  <hr className="my-4" />
                  <h6 className="fw-bold text-secondary mb-3"><i className="bi bi-calendar-event me-2"></i>Fechas y Notas</h6>

                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Fecha de Evaluación</label>
                    <input type="date" className="form-control" name="fecha_evaluacion" value={formData.fecha_evaluacion} onChange={handleChange} />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Fecha de Ingreso</label>
                    <input type="date" className="form-control" name="fecha_ingreso" value={formData.fecha_ingreso} onChange={handleChange} required />
                  </div>
                  <div className="col-12">
                    <label className="form-label small fw-bold">Observaciones</label>
                    <textarea className="form-control" name="observaciones" rows="3" value={formData.observaciones} onChange={handleChange}></textarea>
                  </div>
                </div>
              )}
            </div>
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary px-4" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold px-4">Guardar Evaluación</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default VehiculoUsadoForm;

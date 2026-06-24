import React, { useState, useEffect } from 'react';
import { inventarioApi } from '../../api/inventarioApi';
import { sucursalesApi } from '../../api/sucursalesApi';
import { usuariosApi } from '../../api/usuariosApi';

const TrasladoFormModal = ({ isOpen, onClose, onSubmit, initialData }) => {
  const [formData, setFormData] = useState({
    vehiculo: '',
    sucursal_origen: '',
    sucursal_destino: '',
    usuario_autoriza: '',
    usuario_registro: '',
    costo_traslado: '',
    fecha_traslado: '',
    motivo: '',
    estado: 'pendiente',
  });

  const [vehiculos, setVehiculos] = useState([]);
  const [sucursales, setSucursales] = useState([]);
  const [usuarios, setUsuarios] = useState([]);
  const [loadingLists, setLoadingLists] = useState(true);

  useEffect(() => {
    const loadLists = async () => {
      setLoadingLists(true);
      try {
        const [vData, sData, uData] = await Promise.all([
          inventarioApi.getVehiculos({ estado: 'en_stock' }),
          sucursalesApi.getSucursales(),
          usuariosApi.getUsers()
        ]);
        setVehiculos(vData.results || vData);
        setSucursales(sData.results || sData);
        setUsuarios(uData.results || uData);
      } catch (error) {
        console.error('Error loading lists for traslado form:', error);
      } finally {
        setLoadingLists(false);
      }
    };
    if (isOpen) loadLists();
  }, [isOpen]);

  useEffect(() => {
    if (initialData) {
      setFormData(initialData);
    } else {
      setFormData({
        vehiculo: '', sucursal_origen: '', sucursal_destino: '',
        usuario_autoriza: '', usuario_registro: '', costo_traslado: '',
        fecha_traslado: '', motivo: '', estado: 'pendiente',
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
    <div className="modal show d-block" style={{ backgroundColor: 'rgba(0,0,0,0.5', zIndex: 1050 }}>
      <div className="modal-dialog modal-lg modal-dialog-centered">
        <div className="modal-content border-0 shadow">
          <div className="modal-header modal-header-dark">
            <h5 className="modal-title fw-bold">{initialData ? 'Editar Traslado' : 'Nuevo Traslado de Vehículo'}</h5>
            <button type="button" className="btn-close btn-close-white" onClick={onClose}></button>
          </div>
          <form onSubmit={handleSubmit}>
            <div className="modal-body modal-body-light">
              {loadingLists ? (
                <div className="text-center py-5">Cargando datos...</div>
              ) : (
                <div className="row g-3">
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Vehículo</label>
                    <select className="form-select" name="vehiculo" value={formData.vehiculo} onChange={handleChange} required>
                      <option value="">Seleccione vehículo...</option>
                      {vehiculos.map(v => (
                        <option key={v.id} value={v.id}>{v.patente} - {v.marca_nombre} {v.modelo_nombre}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Fecha de Traslado</label>
                    <input type="date" className="form-control" name="fecha_traslado" value={formData.fecha_traslado} onChange={handleChange} required />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Sucursal Origen</label>
                    <select className="form-select" name="sucursal_origen" value={formData.sucursal_origen} onChange={handleChange} required>
                      <option value="">Seleccione origen...</option>
                      {sucursales.map(s => (
                        <option key={s.id} value={s.id}>{s.nombre}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Sucursal Destino</label>
                    <select className="form-select" name="sucursal_destino" value={formData.sucursal_destino} onChange={handleChange} required>
                      <option value="">Seleccione destino...</option>
                      {sucursales.map(s => (
                        <option key={s.id} value={s.id}>{s.nombre}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Costo de Traslado</label>
                    <input type="number" step="0.01" className="form-control" name="costo_traslado" value={formData.costo_traslado} onChange={handleChange} />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Motivo</label>
                    <input type="text" className="form-control" name="motivo" value={formData.motivo} onChange={handleChange} />
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Usuario Registro</label>
                    <select className="form-select" name="usuario_registro" value={formData.usuario_registro} onChange={handleChange} required>
                      <option value="">Seleccione usuario...</option>
                      {usuarios.map(u => (
                        <option key={u.id} value={u.id}>{u.get_full_name || u.username}</option>
                      ))}
                    </select>
                  </div>
                  <div className="col-md-6">
                    <label className="form-label small fw-bold">Usuario Autoriza</label>
                    <select className="form-select" name="usuario_autoriza" value={formData.usuario_autoriza} onChange={handleChange} required>
                      <option value="">Seleccione autorizador...</option>
                      {usuarios.map(u => (
                        <option key={u.id} value={u.id}>{u.get_full_name || u.username}</option>
                      ))}
                    </select>
                  </div>
                </div>
              )}
            </div>
            <div className="modal-footer modal-footer-light">
              <button type="button" className="btn btn-secondary" onClick={onClose}>Cancelar</button>
              <button type="submit" className="btn btn-gold">Guardar Traslado</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TrasladoFormModal;

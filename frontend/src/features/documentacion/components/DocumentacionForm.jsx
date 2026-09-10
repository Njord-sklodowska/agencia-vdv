import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { documentacionApi } from '../../../api/documentacionApi';
import { inventarioApi } from '../../../api/inventarioApi';

const ESTADOS_DOCUMENTO = [
  { value: 'pendiente', label: 'Pendiente' },
  { value: 'recibido', label: 'Recibido' },
  { value: 'en_tramite', label: 'En Trámite' },
  { value: 'completado', label: 'Completado' },
];

const DocumentacionForm = ({ documentoInicial = null }) => {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const esEdicionExplicita = Boolean(documentoInicial);

  // Si se llegó acá desde la tabla del listado (celda vacía → "cargar
  // documento"), la URL trae ?vehiculo=X&tipo_documento=Y y arrancamos
  // el formulario con esos dos campos ya elegidos.
  const [formData, setFormData] = useState(documentoInicial || {
    vehiculo: searchParams.get('vehiculo') || '',
    tipo_documento: searchParams.get('tipo_documento') || '',
    estado_documento: 'pendiente',
    gestor: '',
    fecha_recepcion: '',
    fecha_entrega_gestor: '',
    fecha_estimada_devolucion: '',
    fecha_devolucion_real: '',
    fecha_vencimiento: '',
    observaciones: '',
  });

  const [archivoPdf, setArchivoPdf] = useState(null);

  const [vehiculos, setVehiculos] = useState([]);
  const [tiposDocumento, setTiposDocumento] = useState([]);
  const [gestores, setGestores] = useState([]);
  const [cargandoOpciones, setCargandoOpciones] = useState(true);

  const [idExistenteDetectado, setIdExistenteDetectado] = useState(null);
  const [estadoDetectado, setEstadoDetectado] = useState(null);
  const [gestorBloqueado, setGestorBloqueado] = useState(false);

  const editando = esEdicionExplicita || Boolean(idExistenteDetectado);

  useEffect(() => {
    const cargarOpciones = async () => {
      try {
        const [dataVehiculos, dataTipos, dataGestores] = await Promise.all([
          inventarioApi.getVehiculos(),
          documentacionApi.getTiposDocumento(),
          documentacionApi.getGestores(),
        ]);

        setVehiculos(dataVehiculos.results || dataVehiculos);
        setTiposDocumento(dataTipos.results || dataTipos);
        setGestores(dataGestores.results || dataGestores);
      } catch (error) {
        console.error('Error al cargar opciones del formulario:', error);
        alert('No se pudieron cargar los datos del formulario (vehículos/tipos/gestores).');
      } finally {
        setCargandoOpciones(false);
      }
    };

    cargarOpciones();
  }, []);

  // Un solo gestor por vehículo: apenas se elige el vehículo, buscamos
  // entre TODOS sus documentos (sin filtrar por tipo) si alguno ya tiene
  // gestor asignado. Si es así, se precarga y se bloquea — no se puede
  // asignar otro gestor distinto al mismo vehículo.
  useEffect(() => {
    if (esEdicionExplicita) return;

    if (!formData.vehiculo) {
      setGestorBloqueado(false);
      return;
    }

    const buscarGestorDelVehiculo = async () => {
      try {
        const data = await documentacionApi.getDocumentos({ vehiculo: formData.vehiculo });
        const lista = data.results || data;
        const conGestor = lista.find((d) => d.gestor);

        if (conGestor) {
          setGestorBloqueado(true);
          setFormData((prev) => ({ ...prev, gestor: String(conGestor.gestor) }));
        } else {
          setGestorBloqueado(false);
        }
      } catch (error) {
        console.error('Error al verificar el gestor asignado al vehículo:', error);
      }
    };

    buscarGestorDelVehiculo();
  }, [formData.vehiculo, esEdicionExplicita]);

  // Detección automática: si ya existe un documento de este tipo para este
  // vehículo, cargamos sus datos y pasamos a actualizarlo en vez de crear
  // uno nuevo. Solo aplica en el formulario de alta.
  useEffect(() => {
    if (esEdicionExplicita) return;

    if (!formData.vehiculo || !formData.tipo_documento) {
      if (idExistenteDetectado) {
        setIdExistenteDetectado(null);
        setEstadoDetectado(null);
      }
      return;
    }

    const buscarDocumentoExistente = async () => {
      try {
        const data = await documentacionApi.getDocumentos({
          vehiculo: formData.vehiculo,
          tipo_documento: formData.tipo_documento,
        });
        const lista = data.results || data;

        if (lista.length > 0) {
          const existente = lista[0];

          const indiceActual = ESTADOS_DOCUMENTO.findIndex((e) => e.value === existente.estado_documento);
          const siguientes = ESTADOS_DOCUMENTO.slice(indiceActual + 1);
          const proximoEstado = siguientes[0]?.value || existente.estado_documento;

          setIdExistenteDetectado(existente.id);
          setEstadoDetectado(existente.estado_documento);
          setFormData((prev) => ({
            ...prev,
            ...existente,
            vehiculo: String(existente.vehiculo),
            tipo_documento: String(existente.tipo_documento),
            // El gestor lo gobierna el vehículo (ver useEffect de arriba),
            // no lo pisamos con lo que tenga este documento puntual.
            gestor: prev.gestor,
            estado_documento: proximoEstado,
          }));
        } else {
          setIdExistenteDetectado(null);
          setEstadoDetectado(null);
        }
      } catch (error) {
        console.error('Error al verificar si ya existe un documento de este tipo:', error);
      }
    };

    buscarDocumentoExistente();
  }, [formData.vehiculo, formData.tipo_documento, esEdicionExplicita]);

  const tipoSeleccionado = tiposDocumento.find(
    (t) => String(t.id) === String(formData.tipo_documento)
  );
  const requiereVencimiento = tipoSeleccionado?.requiere_vencimiento || false;
  const tieneGestor = Boolean(formData.gestor);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleArchivoChange = (e) => {
    setArchivoPdf(e.target.files[0] || null);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const body = new FormData();
    Object.entries(formData).forEach(([key, value]) => {
      if (value !== '' && value !== null) {
        body.append(key, value);
      }
    });
    if (archivoPdf) {
      body.append('archivo_pdf', archivoPdf);
    }

    const idParaGuardar = documentoInicial?.id || idExistenteDetectado;

    try {
      if (idParaGuardar) {
        await documentacionApi.updateDocumento(idParaGuardar, body);
        alert('¡Documento actualizado con éxito!');
      } else {
        await documentacionApi.createDocumento(body);
        alert('¡Documento registrado con éxito!');
      }
      navigate('/documentacion');
    } catch (error) {
      console.error('Error al guardar documento:', error);
      const detalle = error.response?.data
        ? JSON.stringify(error.response.data)
        : 'No se pudo conectar con el backend.';
      alert('Error al guardar: ' + detalle);
    }
  };

  if (cargandoOpciones) {
    return <div className="p-4">Cargando formulario...</div>;
  }

  const indiceEstadoDetectado = estadoDetectado
    ? ESTADOS_DOCUMENTO.findIndex((e) => e.value === estadoDetectado)
    : -1;
  const opcionesEstadoFiltradas =
    indiceEstadoDetectado >= 0
      ? ESTADOS_DOCUMENTO.filter((_, i) => i > indiceEstadoDetectado)
      : ESTADOS_DOCUMENTO;
  const opcionesEstado =
    opcionesEstadoFiltradas.length > 0
      ? opcionesEstadoFiltradas
      : ESTADOS_DOCUMENTO.filter((e) => e.value === estadoDetectado);

  return (
    <div className="container-fluid p-0" style={{ minHeight: '100%' }}>
      <div className="mb-3 text-muted small fw-semibold ps-1" style={{ letterSpacing: '0.5px' }}>
        Documentación &gt; <span style={{ color: '#4a5568' }}>{editando ? 'Editar Documento' : 'Nuevo Documento'}</span>
      </div>

      <form onSubmit={handleSubmit} className="p-4 border rounded shadow-sm" style={{ backgroundColor: '#b1c3db' }}>
        <h3 className="mb-4 text-dark fw-bold">
          {editando ? 'Editar Documentación de Vehículo' : 'Registro de Documentación de Vehículo'}
        </h3>

        {idExistenteDetectado && !esEdicionExplicita && (
          <div className="alert alert-warning py-2 px-3 mb-3" style={{ fontSize: '0.9rem' }}>
            Ya existe un documento de este tipo para este vehículo — vas a actualizar ese registro en vez de crear uno nuevo.
          </div>
        )}

        <div className="row g-3 align-items-end">
          {/* --- SECCIÓN 1: VEHÍCULO Y GESTOR (uno solo por vehículo) --- */}
          <div className="col-md-6">
            <label className="form-label fw-semibold">Vehículo</label>
            <select name="vehiculo" className="form-select" value={formData.vehiculo} onChange={handleChange} required>
              <option value="">Seleccionar vehículo...</option>
              {vehiculos.map((v) => (
                <option key={v.id} value={v.id}>
                  {v.patente || v.vin} — {v.marca_nombre} {v.modelo_nombre}
                </option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label className="form-label fw-semibold">Gestor</label>
            <select
              name="gestor" className="form-select" value={formData.gestor} onChange={handleChange}
              disabled={gestorBloqueado} required
            >
              <option value="">Seleccionar gestor...</option>
              {gestores.map((g) => (
                <option key={g.id} value={g.id}>{g.apellido}, {g.nombre}</option>
              ))}
            </select>
            {gestorBloqueado && (
              <small className="text-muted">
                Este vehículo ya tiene un gestor asignado — toda su documentación la tramita la misma persona.
              </small>
            )}
          </div>

          {/* --- SECCIÓN 2: DOCUMENTO Y SU ESTADO --- */}
          <div className="col-md-6">
            <label className="form-label fw-semibold">Tipo de Documento</label>
            <select name="tipo_documento" className="form-select" value={formData.tipo_documento} onChange={handleChange} required>
              <option value="">Seleccionar tipo...</option>
              {tiposDocumento.map((t) => (
                <option key={t.id} value={t.id}>{t.nombre}</option>
              ))}
            </select>
          </div>
          <div className="col-md-6">
            <label className="form-label fw-semibold">Estado del Documento</label>
            <select name="estado_documento" className="form-select" value={formData.estado_documento} onChange={handleChange} required>
              {opcionesEstado.map((e) => (
                <option key={e.value} value={e.value}>{e.label}</option>
              ))}
            </select>
            {estadoDetectado && (
              <small className="text-muted">
                Este documento ya estaba en "{ESTADOS_DOCUMENTO.find((e) => e.value === estadoDetectado)?.label}" — solo se puede avanzar desde ahí.
              </small>
            )}
          </div>
          <div className="col-md-6">
            <label className="form-label fw-semibold">Fecha de Recepción</label>
            <input
              type="date" name="fecha_recepcion" className="form-control"
              value={formData.fecha_recepcion} onChange={handleChange}
              required={['recibido', 'completado'].includes(formData.estado_documento)}
            />
          </div>

          {/* --- SECCIÓN 3: GESTORÍA EXTERNA (fechas correspondientes al documento) --- */}
          <div className="col-12 mt-4 mb-2">
            <h6 className="fw-bold text-dark border-bottom border-secondary pb-2">Gestoría Externa</h6>
          </div>
          <div className="col-md-4">
            <label className="form-label fw-semibold">Fecha de Entrega al Gestor</label>
            <input
              type="date" name="fecha_entrega_gestor" className="form-control"
              value={formData.fecha_entrega_gestor} onChange={handleChange}
              required={tieneGestor}
            />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-semibold">Fecha Estimada de Devolución</label>
            <input
              type="date" name="fecha_estimada_devolucion" className="form-control"
              value={formData.fecha_estimada_devolucion} onChange={handleChange}
              required={tieneGestor}
            />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-semibold">Fecha Real de Devolución</label>
            <input
              type="date" name="fecha_devolucion_real" className="form-control"
              value={formData.fecha_devolucion_real} onChange={handleChange}
              required={tieneGestor && formData.estado_documento === 'completado'}
            />
          </div>

          {/* --- SECCIÓN 4: VENCIMIENTO Y ARCHIVO --- */}
          <div className="col-12 mt-4 mb-2">
            <h6 className="fw-bold text-dark border-bottom border-secondary pb-2">Vencimiento y Archivo</h6>
          </div>
          {requiereVencimiento && (
            <div className="col-md-6">
              <label className="form-label fw-semibold">Fecha de Vencimiento</label>
              <input
                type="date" name="fecha_vencimiento" className="form-control"
                value={formData.fecha_vencimiento} onChange={handleChange}
                required={formData.estado_documento === 'completado'}
              />
              <small className="text-muted">Este tipo de documento requiere fecha de vencimiento.</small>
            </div>
          )}
          <div className={requiereVencimiento ? 'col-md-6' : 'col-md-12'}>
            <label className="form-label fw-semibold">Archivo PDF</label>
            <input
              type="file" name="archivo_pdf" className="form-control"
              accept="application/pdf" onChange={handleArchivoChange}
            />
          </div>

          <div className="col-12">
            <label className="form-label fw-semibold">Observaciones</label>
            <textarea
              name="observaciones" className="form-control" rows="3"
              value={formData.observaciones} onChange={handleChange}
            />
          </div>
        </div>

        <div className="mt-5 d-flex justify-content-end gap-3 border-top border-secondary border-opacity-25 pt-4">
          <button
            type="button"
            className="btn btn-outline-dark fw-bold"
            style={{ padding: '10px 24px', fontSize: '15px' }}
            onClick={() => navigate('/documentacion')}
          >
            Cancelar
          </button>

          <button
            type="submit"
            className="btn btn-primary"
            style={{
              backgroundColor: '#8d9caf',
              color: '#000000',
              fontSize: '16px',
              fontWeight: '800',
              border: 'none',
              padding: '10px 24px',
            }}
          >
            {editando ? 'Guardar Cambios' : 'Guardar Documento'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default DocumentacionForm;

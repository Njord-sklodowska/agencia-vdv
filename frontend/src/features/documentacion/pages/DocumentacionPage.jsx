import React, { useState, useEffect } from 'react';
import { Search, Eye, Pencil, Plus, ChevronLeft, ChevronRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { documentacionApi } from '../../../api/documentacionApi';
import { inventarioApi } from '../../../api/inventarioApi';

const ESTADOS_DOCUMENTO = [
  { value: 'pendiente', label: 'Pendiente' },
  { value: 'recibido', label: 'Recibido' },
  { value: 'en_tramite', label: 'En Trámite' },
  { value: 'completado', label: 'Completado' },
];

const COLOR_POR_ESTADO = {
  pendiente: '#777',
  recibido: '#5bc0de',
  en_tramite: '#f0ad4e',
  completado: '#5cb85c',
};

const ORDEN_TIPOS = [
  '08', 'Titulo', 'Cedula', 'Informe de Dominio', 'Informe de Multas',
  'Patentes', 'Verificacion', 'F12', 'VTV', 'Prenda', 'Manuales',
  'Duplicados de Llave',
];

function DocumentacionPage() {
  const [busqueda, setBusqueda] = useState('');
  const [vehiculos, setVehiculos] = useState([]);
  const [tiposDocumento, setTiposDocumento] = useState([]);
  const [documentos, setDocumentos] = useState([]);
  const [cargando, setCargando] = useState(true);

  const [paginaActual, setPaginaActual] = useState(1);
  const vehiculosPorPagina = 30;

  const cargarTodo = async () => {
    try {
      setCargando(true);
      const [dataVehiculos, dataTipos, dataDocumentos] = await Promise.all([
        inventarioApi.getVehiculos(),
        documentacionApi.getTiposDocumento(),
        documentacionApi.getDocumentos(),
      ]);
      setVehiculos(dataVehiculos.results || dataVehiculos);
      setTiposDocumento(dataTipos.results || dataTipos);
      setDocumentos(dataDocumentos.results || dataDocumentos);
    } catch (error) {
      console.error('Error al traer la documentación del servidor:', error);
    } finally {
      setCargando(false);
    }
  };

  useEffect(() => {
    cargarTodo();
  }, []);

  const tiposOrdenados = [...tiposDocumento].sort((a, b) => {
    const iA = ORDEN_TIPOS.indexOf(a.nombre);
    const iB = ORDEN_TIPOS.indexOf(b.nombre);
    if (iA === -1 && iB === -1) return 0;
    if (iA === -1) return 1;
    if (iB === -1) return -1;
    return iA - iB;
  });

  const mapaDocumentos = {};
  documentos.forEach((doc) => {
    const clave = `${doc.vehiculo}-${doc.tipo_documento}`;
    if (!mapaDocumentos[clave]) {
      mapaDocumentos[clave] = doc;
    }
  });

  const normalizarTexto = (texto) => {
    if (!texto) return '';
    return texto.toString().toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '').trim();
  };

  const vehiculosFiltrados = busqueda
    ? vehiculos.filter((v) => {
        const texto = normalizarTexto(busqueda);
        return (
          normalizarTexto(v.patente).includes(texto) ||
          normalizarTexto(v.vin).includes(texto) ||
          normalizarTexto(v.marca_nombre).includes(texto) ||
          normalizarTexto(v.modelo_nombre).includes(texto)
        );
      })
    : vehiculos;

  const indiceUltimo = paginaActual * vehiculosPorPagina;
  const indicePrimero = indiceUltimo - vehiculosPorPagina;
  const vehiculosDeLaPagina = vehiculosFiltrados.slice(indicePrimero, indiceUltimo);
  const totalPaginas = Math.ceil(vehiculosFiltrados.length / vehiculosPorPagina);

  const handleCambiarEstado = async (documento, nuevoEstado) => {
    try {
      await documentacionApi.updateDocumento(documento.id, { estado_documento: nuevoEstado });
      setDocumentos((prev) =>
        prev.map((d) => (d.id === documento.id ? { ...d, estado_documento: nuevoEstado } : d))
      );
    } catch (error) {
      console.error('Error al actualizar el estado:', error);
      const detalle = error.response?.data ? JSON.stringify(error.response.data) : 'Error desconocido.';
      alert('No se pudo actualizar el estado: ' + detalle);
    }
  };

  const renderCelda = (vehiculo, tipo) => {
    const documento = mapaDocumentos[`${vehiculo.id}-${tipo.id}`];

    if (!documento) {
      return (
        <Link
          to={`/documentacion/nuevo?vehiculo=${vehiculo.id}&tipo_documento=${tipo.id}`}
          className="d-inline-flex align-items-center justify-content-center"
          title={`Cargar ${tipo.nombre}`}
          style={{
            backgroundColor: '#f0ad4e',
            color: '#000',
            width: '24px',
            height: '24px',
            borderRadius: '50%',
            textDecoration: 'none',
          }}
        >
          <Plus size={14} />
        </Link>
      );
    }

    const indiceActual = ESTADOS_DOCUMENTO.findIndex((e) => e.value === documento.estado_documento);
    const opciones = ESTADOS_DOCUMENTO.slice(indiceActual);

    return (
      <div className="d-flex align-items-center justify-content-center gap-1">
        <select
          className="form-select form-select-sm fw-bold text-white text-center border-0"
          style={{
            fontSize: '0.68rem',
            width: '78px',
            padding: '2px 3px',
            backgroundColor: COLOR_POR_ESTADO[documento.estado_documento],
            borderRadius: '10px',
            appearance: 'none',
            WebkitAppearance: 'none',
          }}
          value={documento.estado_documento}
          onChange={(e) => handleCambiarEstado(documento, e.target.value)}
        >
          {opciones.map((op) => (
            <option key={op.value} value={op.value} style={{ backgroundColor: '#fff', color: '#000' }}>
              {op.label}
            </option>
          ))}
        </select>
        <Link to={`/documentacion/editar/${documento.id}`} className="text-secondary opacity-70" title="Editar documento completo">
          <Pencil size={12} />
        </Link>
      </div>
    );
  };

  return (
    <div className="container-fluid p-0" style={{ minHeight: '100%', marginLeft: '-12px', marginRight: '-12px' }}>

      <div className="mb-2 text-muted small fw-semibold ps-1" style={{ letterSpacing: '0.5px' }}>
        Documentación &gt; <span style={{ color: '#4a5568' }}>Listado de documentación</span>
      </div>

      <div className="card shadow-sm border-secondary border-opacity-25" style={{ borderRadius: '8px', overflow: 'hidden', backgroundColor: '#e2e8f0' }}>

        <div className="p-3" style={{ backgroundColor: '#2c3e50' }}>
          <h2 className="text-white m-0 fw-bold fs-3" style={{ fontFamily: 'sans-serif', letterSpacing: '0.5px' }}>
            Listado de Documentación de Vehículos
          </h2>
        </div>

        <div className="d-flex justify-content-between align-items-center p-3 bg-white border-bottom border-secondary border-opacity-25 shadow-sm">
          <div className="input-group" style={{ width: '420px' }}>
            <span className="input-group-text bg-light border-secondary border-opacity-50 text-muted px-3">
              <Search size={18} strokeWidth={1.5} className="text-secondary opacity-75" />
            </span>
            <input
              type="text"
              className="form-control bg-light border-secondary border-opacity-50"
              placeholder="BUSCAR POR PATENTE, VIN, MARCA O MODELO..."
              style={{ fontSize: '0.8rem', letterSpacing: '0.5px', height: '42px' }}
              value={busqueda}
              onChange={(e) => setBusqueda(e.target.value)}
            />
          </div>

          <Link
            to="/documentacion/nuevo"
            className="btn fw-bold border-0 text-uppercase px-4 py-2 shadow-sm"
            style={{
              backgroundColor: '#f0ad4e',
              color: '#000',
              fontSize: '0.8rem',
              letterSpacing: '0.5px',
              borderRadius: '6px',
              height: '42px',
              display: 'inline-flex',
              alignItems: 'center',
              textDecoration: 'none'
            }}
          >
            Agregar Documento
          </Link>
        </div>

        <div className="table-responsive bg-white">
          <table className="table table-bordered align-middle mb-0 text-center" style={{ borderColor: '#cbd5e0', fontSize: '0.8rem' }}>
            <thead>
              <tr className="fw-bold text-dark" style={{ backgroundColor: '#a0aec0' }}>
                <th style={{ minWidth: '50px' }}>ID</th>
                <th style={{ minWidth: '130px' }}>Marca y Modelo</th>
                <th style={{ minWidth: '130px' }}>N° de VIN</th>
                {tiposOrdenados.map((tipo) => (
                  <th key={tipo.id} style={{ minWidth: '95px', fontSize: '0.75rem' }}>{tipo.nombre}</th>
                ))}
                <th style={{ minWidth: '70px' }}>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {cargando && (
                <tr>
                  <td colSpan={4 + tiposOrdenados.length} className="py-4 text-muted">Cargando...</td>
                </tr>
              )}

              {!cargando && vehiculosDeLaPagina.length === 0 && (
                <tr>
                  <td colSpan={4 + tiposOrdenados.length} className="py-4 text-muted">No hay vehículos para mostrar.</td>
                </tr>
              )}

              {!cargando && vehiculosDeLaPagina.map((vehiculo, index) => (
                <tr key={vehiculo.id} style={{ '--bs-table-bg': index % 2 === 0 ? '#ffffff' : '#c4c4c4ef', height: '30px' }}>
                  <td className="text-muted small py-1">{vehiculo.id}</td>
                  <td className="text-start px-3 text-dark fw-medium py-1">
                    {vehiculo.marca_nombre} {vehiculo.modelo_nombre}
                  </td>
                  <td className="text-dark small py-1">{vehiculo.vin}</td>
                  {tiposOrdenados.map((tipo) => (
                    <td key={tipo.id} className="py-1">{renderCelda(vehiculo, tipo)}</td>
                  ))}
                  <td className="py-1">
                    <div className="d-flex justify-content-center gap-2">
                      <Link to={`/documentacion/nuevo?vehiculo=${vehiculo.id}`} className="text-secondary opacity-70" title="Ver / cargar documentación">
                        <Eye size={16} />
                      </Link>
                      <Link to={`/documentacion/nuevo?vehiculo=${vehiculo.id}`} className="text-secondary opacity-70" title="Editar">
                        <Pencil size={16} />
                      </Link>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <div className="d-flex justify-content-between align-items-center p-3 bg-light border-top border-secondary border-opacity-25">
          <div className="text-muted fw-bold">
            {cargando ? 'Cargando...' : `Mostrando página ${paginaActual} de ${totalPaginas || 1}`}
          </div>

          <div className="d-flex gap-2">
            <button
              className="btn btn-primary"
              style={{ backgroundColor: '#8d9caf', color: '#000000', fontSize: '16px', fontWeight: '800', border: 'none', padding: '10px 24px' }}
              disabled={paginaActual === 1}
              onClick={() => setPaginaActual((prev) => prev - 1)}
            >
              <ChevronLeft size={20} className="me-1" /> Anterior
            </button>

            <button
              className="btn btn-primary"
              style={{ backgroundColor: '#8d9caf', color: '#000000', fontSize: '16px', fontWeight: '800', border: 'none', padding: '10px 24px' }}
              disabled={paginaActual === totalPaginas || totalPaginas === 0}
              onClick={() => setPaginaActual((prev) => prev + 1)}
            >
              Siguiente <ChevronRight size={20} className="ms-1" />
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}

export default DocumentacionPage;

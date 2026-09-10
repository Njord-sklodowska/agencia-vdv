import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import DocumentacionForm from '../components/DocumentacionForm';
import { documentacionApi } from '../../../api/documentacionApi';

function DocumentacionEditarPage() {
  const { id } = useParams();
  const [documento, setDocumento] = useState(null);
  const [cargando, setCargando] = useState(true);

  useEffect(() => {
    const cargarDocumento = async () => {
      try {
        const data = await documentacionApi.getDocumentoById(id);
        setDocumento(data);
      } catch (error) {
        console.error(`Error al cargar el documento ${id}:`, error);
        alert('No se pudo cargar el documento a editar.');
      } finally {
        setCargando(false);
      }
    };

    cargarDocumento();
  }, [id]);

  if (cargando) {
    return <div className="p-4">Cargando documento...</div>;
  }

  if (!documento) {
    return <div className="p-4">No se encontró el documento solicitado.</div>;
  }

  return <DocumentacionForm documentoInicial={documento} />;
}

export default DocumentacionEditarPage;

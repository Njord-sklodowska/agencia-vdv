import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const ClientesForm = ({ clienteInicial = null }) => {
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState(clienteInicial || {
    nombre: '',
    apellido: '',
    dni_cuit: '',
    email: '',
    telefono: '',
    direccion: '',
    localidad: '',
    fecha_nacimiento: '',
    empleador: '',
    antiguedad_laboral: '',
    activo: true
  });

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({ 
      ...formData, 
      [name]: type === 'checkbox' ? checked : type === 'number' ? Number(value) : value 
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/clientes/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        alert("¡Cliente registrado con éxito!");
        console.log("Respuesta del servidor:", data);
        navigate('/clientes'); // Redirige automáticamente a la lista de clientes
      } else {
        const errorData = await response.json();
        console.error("Error del servidor:", errorData);
        alert("Error al guardar: " + JSON.stringify(errorData));
      }
    } catch (error) {
      console.error("Error de conexión:", error);
      alert("No se pudo conectar con el backend de Django.");
    }
  };

  return (
    <div className="container-fluid p-0" style={{ minHeight: '100%' }}>
      {/* Migas de pan */}
      <div className="mb-3 text-muted small fw-semibold ps-1" style={{ letterSpacing: '0.5px' }}>
        Clientes &gt; <span style={{ color: '#4a5568' }}>Nuevo Cliente</span>
      </div>

      <form onSubmit={handleSubmit} className="p-4 border rounded shadow-sm" style={{ backgroundColor: '#b1c3db' }}>
        <h3 className="mb-4 text-dark fw-bold">Registro de Nuevo Cliente</h3>

        <div className="row g-3 align-items-end">
          {/* --- SECCIÓN 1: DATOS PERSONALES --- */}
          <div className="col-md-6">
            <label className="form-label fw-semibold">Nombre</label>
            <input type="text" name="nombre" className="form-control" value={formData.nombre} onChange={handleChange} required />
          </div>
          <div className="col-md-6">
            <label className="form-label fw-semibold">Apellido</label>
            <input type="text" name="apellido" className="form-control" value={formData.apellido} onChange={handleChange} required />
          </div>

          {/* --- SECCIÓN 2: IDENTIFICACIÓN Y CONTACTO --- */}
          <div className="col-md-4">
            <label className="form-label fw-semibold">DNI / CUIT</label>
            <input type="text" name="dni_cuit" className="form-control" value={formData.dni_cuit} onChange={handleChange} required />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-semibold">Fecha de Nacimiento</label>
            <input type="date" name="fecha_nacimiento" className="form-control" value={formData.fecha_nacimiento} onChange={handleChange} />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-semibold">Teléfono</label>
            <input type="text" name="telefono" className="form-control" value={formData.telefono} onChange={handleChange} required />
          </div>

          <div className="col-md-12">
            <label className="form-label fw-semibold">Email</label>
            <input type="email" name="email" className="form-control" value={formData.email} onChange={handleChange} required />
          </div>

          {/* --- SECCIÓN 3: UBICACIÓN --- */}
          <div className="col-md-8">
            <label className="form-label fw-semibold">Dirección (Calle y Número)</label>
            <input type="text" name="direccion" className="form-control" value={formData.direccion} onChange={handleChange} />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-semibold">Localidad</label>
            <input type="text" name="localidad" className="form-control" value={formData.localidad} onChange={handleChange} />
          </div>

          {/* --- SECCIÓN 4: DATOS LABORALES --- */}
          <div className="col-12 mt-4 mb-2">
            <h6 className="fw-bold text-dark border-bottom border-secondary pb-2">Información Laboral (Para financiamiento interno)</h6>
          </div>
          <div className="col-md-8">
            <label className="form-label fw-semibold">Empleador (Opcional)</label>
            <input type="text" name="empleador" className="form-control" value={formData.empleador} onChange={handleChange} />
          </div>
          <div className="col-md-4">
            <label className="form-label fw-semibold">Antigüedad Laboral (Años)</label>
            <input type="number" name="antiguedad_laboral" className="form-control" value={formData.antiguedad_laboral} onChange={handleChange} />
          </div>
        </div> 

        {/* --- SECCIÓN BOTONES --- */}
        <div className="mt-5 d-flex justify-content-end gap-3 border-top border-secondary border-opacity-25 pt-4">
          <button 
            type="button" 
            className="btn btn-outline-dark fw-bold"
            style={{ padding: '10px 24px', fontSize: '15px' }}
            onClick={() => navigate('/clientes')}
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
              padding: '10px 24px'
            }}
          >
            Guardar Cliente
          </button>
        </div>
      </form>
    </div>
  );
};

export default ClientesForm;
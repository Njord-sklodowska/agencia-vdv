import React, { useState } from 'react';

const VehiculosForm = ({ vehiculoInicial = null }) => {
  const [formData, setFormData] = useState(vehiculoInicial || {
    id_sucursal: '', 
    id_marca: '', 
    id_modelo: '', 
    condicion_vehiculo: '0km',
    vin: '', 
    patente: '', 
    anio: new Date().getFullYear(),
    color: '',
    precio: '',
    descripcion_tecnica: '',
    estado: 'en_stock', 
    kilometraje: 0,
    combustible: 'nafta', 
    transmision: 'manual', 
    puertas: 4, 
    motor: '', 
    traccion: 'delantera', 
    numero_serie_motor: '', 
    procedencia: 'compra_directa', 
    activo: true,
    entregado: false
  });

  const handleChange = (e) => {
    const { name, value, type } = e.target;
    setFormData({ 
      ...formData, 
      [name]: type === 'number' ? Number(value) : value 
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('http://127.0.0.1:8000/api/inventario/vehiculos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        alert("¡Vehículo registrado con éxito!");
        console.log("Respuesta del servidor:", data);
        // Aquí podrías redirigir al usuario a la lista de vehículos
      } else {
        const errorData = await response.json();
        console.error("Error del servidor:", errorData);
        alert("Error al guardar: " + JSON.stringify(errorData));
      }
    } catch (error) {
      console.error("Error de conexión:", error);
      alert("No se pudo conectar con el servidor.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded shadow-sm bg-light">
      <h3 className="mb-4">Registro de Vehículo</h3>

      <div className="row g-3">
        {/* --- SECCIÓN 1: UBICACIÓN Y CONDICIÓN --- */}
        <div className="col-md-6">
          <label>ID Sucursal</label>
          <input type="number" name="id_sucursal" className="form-control" value={formData.id_sucursal} onChange={handleChange} required />
        </div>

        <div className="col-md-6">
          <label className="form-label">Condición</label>
          <select name="condicion_vehiculo" className="form-select" value={formData.condicion_vehiculo} onChange={handleChange}>
            <option value="0km">0km</option>
            <option value="usado">Usado</option>
          </select>
        </div>

        {/* --- SECCIÓN 2: IDENTIFICACIÓN PRINCIPAL --- */}
        <div className="col-md-6">
          {formData.condicion_vehiculo === '0km' ? (
            <>
              <label className="form-label">VIN (17 caracteres)</label>
              <input name="vin" className="form-control" value={formData.vin} onChange={handleChange} required />
            </>
          ) : (
            <>
              <label className="form-label">Patente</label>
              <input name="patente" className="form-control" value={formData.patente} onChange={handleChange} required />
            </>
          )}
        </div>

        <div className="col-md-3">
          <label>ID Marca</label>
          <input type="number" name="id_marca" className="form-control" value={formData.id_marca} onChange={handleChange} required />
        </div>
        <div className="col-md-3">
          <label>ID Modelo</label>
          <input type="number" name="id_modelo" className="form-control" value={formData.id_modelo} onChange={handleChange} required />
        </div>

        {/* --- SECCIÓN 3: DATOS COMERCIALES --- */}
        <div className="col-md-4">
          <label>Año</label>
          <input type="number" name="anio" className="form-control" value={formData.anio} onChange={handleChange} required />
        </div>
        <div className="col-md-4">
          <label>Color</label>
          <input type="text" name="color" className="form-control" value={formData.color} onChange={handleChange} required />
        </div>
        <div className="col-md-4">
          <label>Precio de Venta</label>
          <input type="number" name="precio" className="form-control" value={formData.precio} onChange={handleChange} required />
        </div>

        {/* --- SECCIÓN 4: FICHA TÉCNICA --- */}
        <div className="col-md-3">
          <label>Combustible</label>
          <select name="combustible" className="form-select" value={formData.combustible} onChange={handleChange}>
            <option value="nafta">Nafta</option>
            <option value="diesel">Diésel</option>
            <option value="gnc">GNC</option>
            <option value="hibrido">Híbrido</option>
            <option value="electrico">Eléctrico</option>
          </select>
        </div>
        <div className="col-md-3">
          <label>Transmisión</label>
          <select name="transmision" className="form-select" value={formData.transmision} onChange={handleChange}>
            <option value="manual">Manual</option>
            <option value="automatica">Automática</option>
          </select>
        </div>
        <div className="col-md-3">
          <label>Tracción</label>
          <select name="traccion" className="form-select" value={formData.traccion} onChange={handleChange}>
            <option value="delantera">Delantera</option>
            <option value="trasera">Trasera</option>
            <option value="4x4">4x4</option>
          </select>
        </div>
        <div className="col-md-3">
          <label>Puertas</label>
          <select name="puertas" className="form-select" value={formData.puertas} onChange={handleChange}>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </select>
        </div>

        <div className="col-md-4">
          <label>Cilindrada del Motor (Ej: 1.6)</label>
          <input type="text" name="motor" className="form-control" value={formData.motor} onChange={handleChange} required />
        </div>

        {/* --- SECCIÓN 5: EXCLUSIVO USADOS --- */}
        {formData.condicion_vehiculo === 'usado' && (
          <>
            <div className="col-md-4">
              <label>Número de Serie de Motor</label>
              <input type="text" name="numero_serie_motor" className="form-control" value={formData.numero_serie_motor} onChange={handleChange} required />
            </div>
            <div className="col-md-4">
              <label>Kilometraje</label>
              <input type="number" name="kilometraje" className="form-control" value={formData.kilometraje} onChange={handleChange} required />
            </div>
            <div className="col-md-12">
              <label>Procedencia</label>
              <select name="procedencia" className="form-select" value={formData.procedencia} onChange={handleChange}>
                <option value="compra_directa">Compra Directa</option>
                <option value="parte_de_pago">Parte de Pago</option>
              </select>
            </div>
          </>
        )}

        {/* --- SECCIÓN 6: DESCRIPCIÓN --- */}
        {/* --- SECCIÓN 6: DESCRIPCIÓN --- */}
        <div className="col-12">
          <label className="form-label">Descripción Técnica (Opcional)</label>
          <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
            <textarea 
              name="descripcion_tecnica" 
              className="form-control" 
              rows="8" 
              value={formData.descripcion_tecnica} 
              onChange={handleChange}
              style={{ height: '100%', resize: 'none' }}
            ></textarea>
          </div>
        </div>
      </div> {/* <--- AQUÍ ESTÁ EL CIERRE QUE FALTABA PARA EL DIV "row g-3" */}

      <div className="mt-4 d-flex justify-content-end">
        <button type="submit" className="btn btn-primary px-4">
          Guardar Vehículo
        </button>
      </div>
    </form>
  );
};

export default VehiculosForm;
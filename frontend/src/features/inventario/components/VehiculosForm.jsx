import React, { useState } from 'react';

const VehiculosForm = () => {
  const [formData, setFormData] = useState({
    patente_vin: '',
    condicion: '0km', // '0km' o 'usado'
    marca: '',
    modelo: '',
    anio: new Date().getFullYear(),
    kilometraje: 0,
    numero_serie_motor: '',
    procedencia: 'compra_directa',
    precio_venta: '',
    estado: 'en_stock'
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Aquí es donde el día de mañana conectaremos con el POST
    console.log("Datos del formulario listo para enviar:", formData);
    alert("Formulario listo para la presentación (Revisar consola)");
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border rounded shadow-sm bg-light">
      <h3 className="mb-4">Registro de Vehículo</h3>

      <div className="row g-3">
        {/* Condición: 0km o Usado */}
        <div className="col-md-6">
          <label className="form-label">Condición</label>
          <select name="condicion" className="form-select" onChange={handleChange}>
            <option value="0km">0km</option>
            <option value="usado">Usado</option>
          </select>
        </div>

        {/* Identificador Dinámico (VIN o Patente) */}
        <div className="col-md-6">
          <label className="form-label">
            {formData.condicion === '0km' ? 'VIN (17 caracteres)' : 'Patente'}
          </label>
          <input name="patente_vin" className="form-control" onChange={handleChange} required />
        </div>

        {/* Campos obligatorios según documento v3 */}
        <div className="col-md-4"><label>Marca</label><input name="marca" className="form-control" onChange={handleChange} required /></div>
        <div className="col-md-4"><label>Modelo</label><input name="modelo" className="form-control" onChange={handleChange} required /></div>
        <div className="col-md-4"><label>Año</label><input type="number" name="anio" className="form-control" value={formData.anio} onChange={handleChange} /></div>

        {/* Campos exclusivos para usados (Lógica requerida en v3) */}
        {formData.condicion === 'usado' && (
          <>
            <div className="col-md-6">
              <label>Número de Serie de Motor</label>
              <input name="numero_serie_motor" className="form-control" onChange={handleChange} required />
            </div>
            <div className="col-md-6">
              <label>Kilometraje</label>
              <input type="number" name="kilometraje" className="form-control" onChange={handleChange} required />
            </div>
          </>
        )}
      </div>

      <button type="submit" className="btn btn-primary mt-4">Guardar Vehículo</button>
    </form>
  );
};

export default VehiculosForm;
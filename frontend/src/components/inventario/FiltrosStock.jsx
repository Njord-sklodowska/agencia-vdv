import React from 'react';

const FiltrosStock = ({ filters, updateFilter, handleSearch, marcas, modelos }) => {
  return (
    <div className="card filter-card">
      <div className="card-header modal-header-dark">
        <i className="bi bi-search me-2"></i>
        Filtros de Inventario
      </div>
      <div className="card-body bg-card-white">
        <div className="row g-3">
          <div className="col-md-3">
            <label className="form-label filter-label">Búsqueda Rápida</label>
            <input
              type="text"
              className="form-control"
              placeholder="VIN, Patente, Modelo..."
              value={filters.search}
              onChange={(e) => handleSearch(e.target.value)}
            />
          </div>

          <div className="col-md-3">
            <label className="form-label filter-label">Marca</label>
            <select
              className="form-select"
              value={filters.marca}
              onChange={(e) => updateFilter('marca', e.target.value)}
            >
              <option value="">Todas las Marcas</option>
              {marcas.map(marca => (
                <option key={marca.id} value={marca.id}>{marca.nombre}</option>
              ))}
            </select>
          </div>

          <div className="col-md-3">
            <label className="form-label filter-label">Modelo</label>
            <select
              className="form-select"
              value={filters.modelo}
              onChange={(e) => updateFilter('modelo', e.target.value)}
            >
              <option value="">Todos los Modelos</option>
              {modelos.map(modelo => (
                <option key={modelo.id} value={modelo.id}>{modelo.nombre}</option>
              ))}
            </select>
          </div>

          <div className="col-md-3">
            <label className="form-label filter-label">Estado</label>
            <select
              className="form-select"
              value={filters.estado}
              onChange={(e) => updateFilter('estado', e.target.value)}
            >
              <option value="">Todos los Estados</option>
              <option value="Nuevo">Nuevo</option>
              <option value="Usado">Usado</option>
              <option value="en_stock">En Stock</option>
              <option value="reservado">Reservado</option>
              <option value="vendido">Vendido</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default FiltrosStock;

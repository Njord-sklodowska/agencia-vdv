import React from 'react';

const BadgeEstado = ({ estado }) => {
  const getBadgeClass = (estado) => {
    switch (estado?.toLowerCase()) {
      case 'en_stock':
      case 'activo':
      case 'activa':
        return 'badge-activo';
      case 'reservado':
        return 'badge-reservado';
      case 'vendido':
      case 'inactivo':
      case 'inactiva':
        return 'badge-inactivo';
      default:
        return 'badge-secondary';
    }
  };

  const getLabel = (estado) => {
    switch (estado?.toLowerCase()) {
      case 'en_stock': return 'En Stock';
      case 'activo':
      case 'activa': return 'Activo';
      case 'reservado': return 'Reservado';
      case 'vendido': return 'Vendido';
      case 'inactivo':
      case 'inactiva': return 'Inactivo';
      default: return estado ? estado.charAt(0).toUpperCase() + estado.slice(1) : 'Desconocido';
    }
  };

  return (
    <span className={`badge badge-estado ${getBadgeClass(estado)}`}>
      {getBadgeClass(estado) === 'badge-secondary' ? (
        <span className="badge-text-white">{getLabel(estado)}</span>
      ) : (
        getLabel(estado)
      )}
    </span>
  );
};

export default BadgeEstado;

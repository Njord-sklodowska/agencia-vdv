import React from 'react';

const Spinner = ({ size = 'md' }) => {
  const spinnerClass = size === 'lg' ? 'spinner-border-lg' : 'spinner-border-sm';
  
  return (
    <div className="d-flex flex-column align-items-center justify-content-center">
      <div className={`spinner-border text-warning ${spinnerClass}`} role="status">
        <span className="visually-hidden">Cargando...</span>
      </div>
      {size === 'lg' && (
        <span className="mt-2 small text-muted fw-medium">Cargando datos...</span>
      )}
      <style>{`
        .spinner-border-lg {
          width: 3rem;
          height: 3rem;
        }
      `}</style>
    </div>
  );
};

export default Spinner;

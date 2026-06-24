import React from 'react';

const PaginadorTabla = ({ currentPage, totalCount, pageSize, onPageChange, onPageSizeChange }) => {
  const totalPages = Math.ceil(totalCount / pageSize);

  const getPageNumbers = () => {
    const pages = [];
    const startPage = Math.max(1, currentPage - 2);
    const endPage = Math.min(totalPages, currentPage + 2);
    for (let i = startPage; i <= endPage; i++) {
      pages.push(i);
    }
    return pages;
  };

  if (totalPages <= 1) return null;

  return (
    <div className="d-flex flex-column flex-md-row justify-content-between align-items-center gap-3 py-2">
      <div className="pagination-info">
        Mostrando <strong>{Math.min((currentPage - 1) * pageSize + 1, totalCount)}</strong> a{' '}
        <strong>{Math.min(currentPage * pageSize, totalCount)}</strong> de{' '}
        <strong>{totalCount}</strong> registros
      </div>

      <div className="d-flex align-items-center gap-3">
        <div className="d-flex align-items-center gap-2">
          <span className="small text-muted">Mostrar:</span>
          <select
            className="form-select form-select-sm page-size-select"
            value={pageSize}
            onChange={(e) => onPageSizeChange(Number(e.target.value))}
          >
            <option value={10}>10</option>
            <option value={25}>25</option>
            <option value={50}>50</option>
            <option value={100}>100</option>
          </select>
        </div>

        <nav aria-label="Page navigation">
          <ul className="pagination pagination-sm mb-0 pagination-erp">
            <li className={`page-item ${currentPage === 1 ? 'disabled' : ''}`}>
              <button
                className="page-link"
                onClick={() => onPageChange(currentPage - 1)}
              >
                <i className="bi bi-chevron-left"></i>
              </button>
            </li>

            {getPageNumbers().map((page) => (
              <li key={page} className={`page-item ${page === currentPage ? 'active' : ''}`}>
                <button
                  className="page-link"
                  onClick={() => onPageChange(page)}
                >
                  {page}
                </button>
              </li>
            ))}

            <li className={`page-item ${currentPage === totalPages ? 'disabled' : ''}`}>
              <button
                className="page-link"
                onClick={() => onPageChange(currentPage + 1)}
              >
                <i className="bi bi-chevron-right"></i>
              </button>
            </li>
          </ul>
        </nav>
      </div>
    </div>
  );
};

export default PaginadorTabla;

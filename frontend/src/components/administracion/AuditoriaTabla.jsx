import React, { useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from '@tanstack/react-table';
import PaginadorTabla from '../common/PaginadorTabla';
import BadgeEstado from '../common/BadgeEstado';

const AuditoriaTabla = ({
  data,
  totalCount,
  pagination,
  setPage,
  setPageSize,
  filters,
  sorting,
  toggleSort,
}) => {
  const columns = useMemo(() => [
    {
      accessorKey: 'fecha',
      header: 'Fecha y Hora',
      cell: info => new Date(info.getValue()).toLocaleString(),
    },
    {
      accessorKey: 'usuario_nombre',
      header: 'Usuario',
      cell: info => <span className="fw-bold">{info.getValue() || 'Sistema'}</span>,
    },
    {
      accessorKey: 'accion',
      header: 'Acción',
      cell: info => {
        const accion = info.getValue();
        const estadoMap = {
          'CREAR': 'activo',
          'MODIFICAR': 'reservado',
          'ELIMINAR': 'inactivo',
          'LOGIN': 'activo',
          'LOGOUT': 'inactivo',
        };
        return <BadgeEstado estado={estadoMap[accion] || 'activo'} />;
      },
    },
    {
      accessorKey: 'modulo',
      header: 'Módulo',
    },
    {
      accessorKey: 'tabla_afectada',
      header: 'Tabla',
    },
    {
      accessorKey: 'descripcion',
      header: 'Descripción',
    },
  ], []);

  const table = useReactTable({
    data,
    columns,
    pageCount: Math.ceil(totalCount / pagination.pageSize),
    state: {
      pagination: {
        pageIndex: pagination.page - 1,
        pageSize: pagination.pageSize,
      },
    },
    onPaginationChange: (updater) => {
      if (typeof updater === 'function') {
        const nextState = updater({ pageIndex: pagination.page - 1, pageSize: pagination.pageSize });
        setPage(nextState.pageIndex + 1);
        setPageSize(nextState.pageSize);
      }
    },
    manualPagination: true,
    manualFiltering: true,
    manualSorting: true,
    getCoreRowModel: getCoreRowModel(),
  });

  const highlightText = (text, highlight) => {
    if (!highlight || !text) return text;
    const parts = text.toString().split(new RegExp(`(${highlight})`, 'gi'));
    return (
      <span>
        {parts.map((part, i) =>
          part.toLowerCase() === highlight.toLowerCase()
            ? <mark key={i} className="highlight">{part}</mark>
            : part
        )}
      </span>
    );
  };

  return (
    <div className="card table-card">
      <div className="card-body">
        <div className="table-responsive">
          <table className="table-erp">
            <thead>
              <tr>
                {table.getHeaderGroups().map(headerGroup =>
                  headerGroup.headers.map(header => (
                    <th
                      key={header.id}
                      onClick={() => toggleSort(header.column.id)}
                    >
                      <div className="d-flex align-items-center justify-content-between">
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        <span className="sort-icon">
                          {sorting.id === header.column.id ? (
                            sorting.desc
                              ? <i className="bi bi-sort-down sort-icon-active"></i>
                              : <i className="bi bi-sort-up sort-icon-active"></i>
                          ) : (
                            <i className="bi bi-sort-down-up sort-icon-inactive"></i>
                          )}
                        </span>
                      </div>
                    </th>
                  ))
                )}
              </tr>
            </thead>
            <tbody>
              {table.getRowModel().rows.map(row => (
                <tr key={row.id}>
                  {row.getVisibleCells().map(cell => (
                    <td key={cell.id}>
                      {typeof cell.getValue() === 'string'
                        ? highlightText(cell.getValue(), filters.search)
                        : flexRender(cell.column.columnDef.cell, cell.getContext())}
                    </td>
                  ))}
                </tr>
              ))}
              {data.length === 0 && (
                <tr>
                  <td colSpan={columns.length} className="empty-state">
                    No se encontraron registros de auditoría.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <div className="card-footer">
        <PaginadorTabla
          currentPage={pagination.page}
          totalCount={totalCount}
          pageSize={pagination.pageSize}
          onPageChange={setPage}
          onPageSizeChange={setPageSize}
        />
      </div>
    </div>
  );
};

export default AuditoriaTabla;

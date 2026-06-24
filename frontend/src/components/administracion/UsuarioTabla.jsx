import React, { useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from '@tanstack/react-table';
import PaginadorTabla from '../common/PaginadorTabla';
import BadgeEstado from '../common/BadgeEstado';

const UsuarioTabla = ({ usuarios, totalCount, pagination, setPage, setPageSize, filters }) => {
  const columns = useMemo(() => [
    {
      accessorKey: 'username',
      header: 'Usuario',
      cell: info => <span className="fw-bold">{info.getValue()}</span>,
    },
    {
      accessorKey: 'email',
      header: 'Correo Electrónico',
    },
    {
      id: 'full_name',
      header: 'Nombre Completo',
      cell: info => {
        const user = info.row.original;
        const firstName = user.first_name || '';
        const lastName = user.last_name || '';
        const fullName = `${firstName} ${lastName}`.trim();
        return <span className="fw-bold">{fullName || user.username}</span>;
      },
    },
    {
      accessorKey: 'rol_nombre',
      header: 'Rol',
      cell: info => {
        const val = info.getValue();
        const rolValue = typeof val === 'string' ? val.toLowerCase() : '';
        const rolLabels = {
          'super administrador': { label: 'Super Administrador', color: 'danger' },
          'administrador': { label: 'Administrador', color: 'primary' },
          'vendedor': { label: 'Vendedor', color: 'info' },
        };
        const { label, color } = rolLabels[rolValue] || { label: val || 'Sin Rol', color: 'secondary' };
        return <span className={`badge bg-${color} text-white`}>{label}</span>;
      },
    },
    {
      accessorKey: 'estado',
      header: 'Estado',
      cell: info => <BadgeEstado estado={info.getValue()} />,
    },
    {
      id: 'actions',
      header: 'Acciones',
      cell: () => (
        <div className="d-flex gap-2">
          <button className="btn btn-sm btn-outline-info" title="Ver"><i className="bi bi-eye"></i></button>
          <button className="btn btn-sm btn-outline-primary" title="Editar"><i className="bi bi-pencil"></i></button>
          <button className="btn btn-sm btn-outline-danger" title="Eliminar"><i className="bi bi-trash"></i></button>
        </div>
      ),
    },
  ], []);

  const table = useReactTable({
    data: usuarios,
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
                    <th key={header.id}>
                      {flexRender(header.column.columnDef.header, header.getContext())}
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
              {usuarios.length === 0 && (
                <tr>
                  <td colSpan={columns.length} className="empty-state">
                    No se encontraron usuarios registrados.
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

export default UsuarioTabla;

import React, { useMemo } from 'react';
import {
  useReactTable,
  getCoreRowModel,
  flexRender,
} from '@tanstack/react-table';
import PaginadorTabla from '../common/PaginadorTabla';
import BadgeEstado from '../common/BadgeEstado';

const VehiculoUsadoTabla = ({
  vehiculosUsados,
  totalCount,
  pagination,
  sorting = { id: 'fecha_evaluacion', desc: true },
  setPage,
  setPageSize,
  toggleSort,
  filters,
  onView,
  onEdit,
  onDelete,
}) => {
  const columns = useMemo(() => [
    {
      accessorKey: 'vehiculo_detalle',
      header: 'Vehículo',
      enableSorting: true,
      id: 'marca_nombre',
      cell: info => <span className="fw-bold">{info.getValue()}</span>,
    },
    {
      accessorKey: 'taller_nombre',
      header: 'Taller',
      enableSorting: true,
    },
    {
      accessorKey: 'precio_tasacion_final',
      header: 'Tasación',
      enableSorting: true,
      cell: info => {
        const value = info.getValue();
        return new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS' }).format(value);
      },
    },
    {
      accessorKey: 'fecha_evaluacion',
      header: 'Evaluación',
      enableSorting: true,
      cell: info => info.getValue() || '---',
    },
    {
      accessorKey: 'fecha_ingreso',
      header: 'Ingreso',
      enableSorting: true,
      cell: info => info.getValue() || '---',
    },
    {
      accessorKey: 'estado_motor',
      header: 'Motor',
      enableSorting: false,
      cell: info => <BadgeEstado estado={info.getValue()} />,
    },
    {
      accessorKey: 'estado_cubierta',
      header: 'Cubiertas',
      enableSorting: false,
      cell: info => <BadgeEstado estado={info.getValue()} />,
    },
    {
      accessorKey: 'estado_chapa_pintura',
      header: 'Chapa/Pint.',
      enableSorting: false,
      cell: info => <BadgeEstado estado={info.getValue()} />,
    },
    {
      accessorKey: 'estado_interior',
      header: 'Interior',
      enableSorting: false,
      cell: info => <BadgeEstado estado={info.getValue()} />,
    },
    {
      id: 'acciones',
      header: 'Acciones',
      disableSorting: true,
      cell: info => (
        <div className="d-flex gap-2">
          <button
            className="btn btn-sm btn-outline-info"
            onClick={() => onView(info.row.original)}
            title="Ver Detalles"
          >
            <i className="bi bi-eye"></i>
          </button>
          <button
            className="btn btn-sm btn-outline-primary"
            onClick={() => onEdit(info.row.original)}
            title="Editar"
          >
            <i className="bi bi-pencil"></i>
          </button>
          <button
            className="btn btn-sm btn-outline-danger"
            onClick={() => onDelete(info.row.original)}
            title="Eliminar"
          >
            <i className="bi bi-trash"></i>
          </button>
        </div>
      ),
    },
  ], [onView, onEdit, onDelete]);

  const table = useReactTable({
    data: vehiculosUsados,
    columns,
    pageCount: Math.ceil(totalCount / pagination.pageSize),
    state: {
      pagination: {
        pageIndex: pagination.page - 1,
        pageSize: pagination.pageSize,
      },
      sorting: [
        {
          id: sorting?.id || 'fecha_evaluacion',
          desc: sorting?.desc || true,
        },
      ],
    },
    onPaginationChange: (updater) => {
      if (typeof updater === 'function') {
        const nextState = updater({
          pageIndex: pagination.page - 1,
          pageSize: pagination.pageSize,
        });
        setPage(nextState.pageIndex + 1);
        setPageSize(nextState.pageSize);
      }
    },
    onSortingChange: () => {},
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
                      onClick={() => {
                        if (header.column.getCanSort()) {
                          toggleSort(header.id);
                        }
                      }}
                    >
                      <div className="d-flex align-items-center gap-2">
                        {flexRender(header.column.columnDef.header, header.getContext())}
                        {header.column.getCanSort() && (
                          <span className="sort-icon">
                            {{
                              asc: <i className="bi bi-sort-up sort-icon-active"></i>,
                              desc: <i className="bi bi-sort-down sort-icon-active"></i>,
                            }[header.column.getIsSorted()] || <i className="bi bi-sort-alpha-down sort-icon-inactive"></i>}
                          </span>
                        )}
                      </div>
                    </th>
                  ))
                )}
              </tr>
            </thead>
            <tbody>
              {table.getRowModel().rows.map(row => (
                <tr key={row.id}>
                  {row.getVisibleCells().map(cell => {
                    const value = cell.getValue();
                    const columnDef = cell.column.columnDef;
                    return (
                      <td key={cell.id}>
                        {columnDef.cell
                          ? flexRender(columnDef.cell, cell.getContext())
                          : typeof value === 'string'
                            ? highlightText(value, filters.search)
                            : value}
                      </td>
                    );
                  })}
                </tr>
              ))}
              {vehiculosUsados.length === 0 && (
                <tr>
                  <td colSpan={columns.length} className="empty-state">
                    No se encontraron evaluaciones de usados con los filtros seleccionados.
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

export default VehiculoUsadoTabla;

import { useState, useEffect, useCallback } from 'react';
import { auditoriaApi } from '../api/auditoriaApi';

export const useAuditoria = () => {
  const [logs, setLogs] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 15,
  });

  const [sorting, setSorting] = useState({
    id: 'fecha',
    desc: true,
  });

  const [filters, setFilters] = useState({
    search: '',
    usuario: '',
    accion: '',
    fecha_desde: '',
    fecha_hasta: '',
  });

  const fetchLogs = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        search: filters.search || undefined,
        usuario: filters.usuario || undefined,
        accion: filters.accion || undefined,
        fecha__gte: filters.fecha_desde || undefined,
        fecha__lte: filters.fecha_hasta || undefined,
        ordering: sorting.desc ? `-${sorting.id}` : sorting.id,
      };

      const data = await auditoriaApi.getLogs(params);

      if (Array.isArray(data)) {
        setLogs(data);
        setTotalCount(data.length);
      } else if (data && data.results) {
        setLogs(data.results);
        setTotalCount(data.count || 0);
      } else {
        setLogs([]);
        setTotalCount(0);
      }
    } catch (err) {
      setError(err.message || 'Error al cargar los logs de auditoría');
      console.error('useAuditoria fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [pagination.page, pagination.pageSize, filters, sorting]);

  useEffect(() => {
    fetchLogs();
  }, [fetchLogs]);

  const updateFilter = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const setPage = (page) => {
    setPagination(prev => ({ ...prev, page }));
  };

  const setPageSize = (pageSize) => {
    setPagination(prev => ({ ...prev, pageSize }));
    setPage(1);
  };

  const toggleSort = (columnId) => {
    setSorting(prev => {
      if (prev.id === columnId) {
        return { ...prev, desc: !prev.desc };
      }
      return { id: columnId, desc: false };
    });
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  return {
    logs,
    totalCount,
    isLoading,
    error,
    pagination,
    filters,
    sorting,
    updateFilter,
    setPage,
    setPageSize,
    toggleSort,
    refresh: fetchLogs,
  };
};

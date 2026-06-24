import { useState, useEffect, useCallback } from 'react';
import { parametrosApi } from '../api/parametrosApi';

export const useParametros = () => {
  const [parametros, setParametros] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Estado de Paginación
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
  });

  // Estado de Ordenamiento
  const [sorting, setSorting] = useState({
    id: 'nombre_parametro',
    desc: false,
  });

  // Estado de Filtros
  const [filters, setFilters] = useState({
    search: '',
  });

  const fetchParametros = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        search: filters.search || undefined,
        ordering: sorting.desc ? `-${sorting.id}` : sorting.id,
      };

      const data = await parametrosApi.getParametros(params);

      if (Array.isArray(data)) {
        setParametros(data);
        setTotalCount(data.length);
      } else if (data && data.results) {
        setParametros(data.results);
        setTotalCount(data.count || 0);
      } else {
        setParametros([]);
        setTotalCount(0);
      }
    } catch (err) {
      setError(err.message || 'Error al cargar los parámetros');
      console.error('useParametros fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [pagination.page, pagination.pageSize, filters, sorting]);

  useEffect(() => {
    fetchParametros();
  }, [fetchParametros]);

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

  const addParametro = async (data) => {
    try {
      await parametrosApi.createParametro(data);
      await fetchParametros();
      return { success: true };
    } catch (err) {
      console.error('useParametros create error:', err);
      return { success: false, error: err };
    }
  };

  const updateParametro = async (id, data) => {
    try {
      await parametrosApi.updateParametro(id, data);
      await fetchParametros();
      return { success: true };
    } catch (err) {
      console.error('useParametros update error:', err);
      return { success: false, error: err };
    }
  };

  const deleteParametro = async (id) => {
    try {
      await parametrosApi.deleteParametro(id);
      await fetchParametros();
      return { success: true };
    } catch (err) {
      console.error('useParametros delete error:', err);
      throw err;
    }
  };

  return {
    parametros,
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
    addParametro,
    updateParametro,
    deleteParametro,
    refresh: fetchParametros,
  };
};

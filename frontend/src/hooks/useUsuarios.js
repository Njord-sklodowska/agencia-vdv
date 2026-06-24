import { useState, useEffect, useCallback } from 'react';
import { usuariosApi } from '../api/usuariosApi';

export const useUsuarios = () => {
  const [usuarios, setUsuarios] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
  });

  const [filters, setFilters] = useState({
    search: '',
  });

  const fetchUsuarios = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        search: filters.search || undefined,
      };

      const data = await usuariosApi.getUsuarios(params);
      
      if (Array.isArray(data)) {
        setUsuarios(data);
        setTotalCount(data.length);
      } else if (data && data.results) {
        setUsuarios(data.results);
        setTotalCount(data.count || 0);
      } else {
        setUsuarios([]);
        setTotalCount(0);
      }
    } catch (err) {
      setError(err.message || 'Error al cargar los usuarios');
    } finally {
      setIsLoading(false);
    }
  }, [pagination.page, pagination.pageSize, filters]);

  useEffect(() => {
    fetchUsuarios();
  }, [fetchUsuarios]);

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

  return {
    usuarios,
    totalCount,
    isLoading,
    error,
    pagination,
    filters,
    updateFilter,
    setPage,
    setPageSize,
    refresh: fetchUsuarios,
  };
};

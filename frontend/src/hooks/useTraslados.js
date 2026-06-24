import { useState, useEffect, useCallback } from 'react';
import { trasladosApi } from '../api/trasladosApi';

export const useTraslados = () => {
  const [traslados, setTraslados] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
  });
  const [filters, setFilters] = useState({
    search: '',
    estado: '',
    sucursal_origen: '',
    sucursal_destino: '',
  });
  const [sorting, setSorting] = useState({
    id: 'fecha_traslado',
    desc: true,
  });

  const fetchTraslados = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        search: filters.search,
        estado: filters.estado,
        sucursal_origen: filters.sucursal_origen,
        sucursal_destino: filters.sucursal_destino,
        ordering: sorting.desc ? `-${sorting.id}` : sorting.id,
      };
      
      const data = await trasladosApi.getTraslados(params);
      
      setTraslados(data.results || data);
      setTotalCount(data.count || 0);
    } catch (error) {
      console.error('Error fetching traslados:', error);
    } finally {
      setLoading(false);
    }
  }, [pagination, filters, sorting]);

  useEffect(() => {
    fetchTraslados();
  }, [fetchTraslados]);

  const handlePageChange = (newPage) => {
    setPagination(prev => ({ ...prev, page: newPage }));
  };

  const handlePageSizeChange = (newSize) => {
    setPagination(prev => ({ ...prev, page: 1, pageSize: newSize }));
  };

  const handleSearch = (search) => {
    setFilters(prev => ({ ...prev, search }));
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const handleFilterChange = (field, value) => {
    setFilters(prev => ({ ...prev, [field]: value }));
    setPagination(prev => ({ ...prev, page: 1 }));
  };

  const toggleSort = (columnId) => {
    setSorting(prev => {
      if (prev.id === columnId) {
        return { ...prev, desc: !prev.desc };
      }
      return { id: columnId, desc: false };
    });
  };

  const addTraslado = async (data) => {
    try {
      await trasladosApi.createTraslado(data);
      await fetchTraslados();
      return { success: true };
    } catch (error) {
      console.error('Error creating traslado:', error);
      return { success: false, error };
    }
  };

  const updateTraslado = async (id, data) => {
    try {
      await trasladosApi.updateTraslado(id, data);
      await fetchTraslados();
      return { success: true };
    } catch (error) {
      console.error('Error updating traslado:', error);
      return { success: false, error };
    }
  };

  const deleteTraslado = async (id) => {
    try {
      await trasladosApi.deleteTraslado(id);
      await fetchTraslados();
      return { success: true };
    } catch (error) {
      console.error('Error deleting traslado:', error);
      return { success: false, error };
    }
  };

  const confirmarTraslado = async (id) => {
    try {
      await trasladosApi.confirmarTraslado(id);
      await fetchTraslados();
      return { success: true };
    } catch (error) {
      console.error('Error confirming traslado:', error);
      return { success: false, error };
    }
  };

  const cancelarTraslado = async (id) => {
    try {
      await trasladosApi.cancelarTraslado(id);
      await fetchTraslados();
      return { success: true };
    } catch (error) {
      console.error('Error canceling traslado:', error);
      return { success: false, error };
    }
  };

  return {
    traslados,
    totalCount,
    loading,
    pagination,
    filters,
    sorting,
    handlePageChange,
    handlePageSizeChange,
    handleSearch,
    handleFilterChange,
    toggleSort,
    addTraslado,
    updateTraslado,
    deleteTraslado,
    confirmarTraslado,
    cancelarTraslado,
    refresh: fetchTraslados
  };
};

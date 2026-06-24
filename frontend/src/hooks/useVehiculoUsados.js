import { useState, useEffect, useCallback } from 'react';
import { vehiculoUsadoApi } from '../api/vehiculoUsadoApi';

export const useVehiculoUsados = () => {
  const [vehiculosUsados, setVehiculosUsados] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
  });
  const [filters, setFilters] = useState({
    search: '',
    taller: '',
    usuario_autoriza: '',
  });
  const [sorting, setSorting] = useState({
    id: 'fecha_evaluacion',
    desc: true,
  });

  const fetchVehiculosUsados = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        search: filters.search,
        taller: filters.taller,
        usuario_autoriza: filters.usuario_autoriza,
        ordering: sorting.desc ? `-${sorting.id}` : sorting.id,
      };
      
      const data = await vehiculoUsadoApi.getVehiculosUsados(params);
      
      setVehiculosUsados(data.results || data);
      setTotalCount(data.count || 0);
    } catch (error) {
      console.error('Error fetching used vehicles:', error);
    } finally {
      setLoading(false);
    }
  }, [pagination, filters, sorting]);

  useEffect(() => {
    fetchVehiculosUsados();
  }, [fetchVehiculosUsados]);

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

  const addVehiculoUsado = async (data) => {
    try {
      await vehiculoUsadoApi.createVehiculoUsado(data);
      await fetchVehiculosUsados();
      return { success: true };
    } catch (error) {
      console.error('Error creating used vehicle evaluation:', error);
      return { success: false, error };
    }
  };

  const updateVehiculoUsado = async (id, data) => {
    try {
      await vehiculoUsadoApi.updateVehiculoUsado(id, data);
      await fetchVehiculosUsados();
      return { success: true };
    } catch (error) {
      console.error('Error updating used vehicle evaluation:', error);
      return { success: false, error };
    }
  };

  const deleteVehiculoUsado = async (id) => {
    try {
      await vehiculoUsadoApi.deleteVehiculoUsado(id);
      await fetchVehiculosUsados();
      return { success: true };
    } catch (error) {
      console.error('Error deleting used vehicle evaluation:', error);
      return { success: false, error };
    }
  };

  return {
    vehiculosUsados,
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
    addVehiculoUsado,
    updateVehiculoUsado,
    deleteVehiculoUsado,
    refresh: fetchVehiculosUsados
  };
};

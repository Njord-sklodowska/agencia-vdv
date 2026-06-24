import { useState, useEffect, useCallback } from 'react';
import { inventarioApi } from '../api/inventarioApi';

export const useTalleres = () => {
  const [talleres, setTalleres] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
  });
  const [filters, setFilters] = useState({
    search: '',
    estado: '',
  });
  const [sorting, setSorting] = useState({
    id: 'nombre',
    desc: false,
  });

  const fetchTalleres = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        search: filters.search,
        estado: filters.estado,
        ordering: sorting.desc ? `-${sorting.id}` : sorting.id,
      };
      
      const data = await inventarioApi.getTalleres(params);
      
      setTalleres(data.results || data);
      setTotalCount(data.count || 0);
    } catch (error) {
      console.error('Error fetching talleres:', error);
    } finally {
      setLoading(false);
    }
  }, [pagination, filters, sorting]);

  useEffect(() => {
    fetchTalleres();
  }, [fetchTalleres]);

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

  const addTaller = async (data) => {
    try {
      await inventarioApi.createTaller(data);
      await fetchTalleres();
      return { success: true };
    } catch (error) {
      console.error('Error creating taller:', error);
      return { success: false, error };
    }
  };

  const updateTaller = async (id, data) => {
    try {
      await inventarioApi.updateTaller(id, data);
      await fetchTalleres();
      return { success: true };
    } catch (error) {
      console.error('Error updating taller:', error);
      return { success: false, error };
    }
  };

  const deleteTaller = async (id) => {
    try {
      await inventarioApi.deleteTaller(id);
      await fetchTalleres();
      return { success: true };
    } catch (error) {
      console.error('Error deleting taller:', error);
      return { success: false, error };
    }
  };

  return {
    talleres,
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
    addTaller,
    updateTaller,
    deleteTaller,
    refresh: fetchTalleres
  };
};

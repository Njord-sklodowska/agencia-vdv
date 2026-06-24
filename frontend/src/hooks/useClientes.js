import { useState, useEffect, useCallback } from 'react';
import { clientesApi } from '../api/clientesApi';

export const useClientes = () => {
  const [clientes, setClientes] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
  });
  const [filters, setFilters] = useState({
    search: '',
    tipo_persona: '',
    estado: '',
    telefono: '',
  });
  const [sorting, setSorting] = useState({
    id: 'fecha_alta',
    desc: false,
  });

  const fetchClientes = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        search: filters.search,
        tipo_persona: filters.tipo_persona,
        estado: filters.estado,
        telefono: filters.telefono ? filters.telefono.replace(/[-\s().]/g, '') : undefined,
        ordering: sorting.desc ? `-${sorting.id}` : sorting.id,
      };
      
      const data = await clientesApi.getClientes(params);
      
      setClientes(data.results || data);
      setTotalCount(data.count || 0);
    } catch (error) {
      console.error('Error fetching clients:', error);
    } finally {
      setLoading(false);
    }
  }, [pagination, filters, sorting]);

  useEffect(() => {
    fetchClientes();
  }, [fetchClientes]);

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

  const addCliente = async (clienteData) => {
    try {
      await clientesApi.createCliente(clienteData);
      await fetchClientes();
      return { success: true };
    } catch (error) {
      console.error('Error creating client:', error);
      return { success: false, error };
    }
  };

  const updateCliente = async (id, clienteData) => {
    try {
      await clientesApi.updateCliente(id, clienteData);
      await fetchClientes();
      return { success: true };
    } catch (error) {
      console.error('Error updating client:', error);
      return { success: false, error };
    }
  };

  const deleteCliente = async (id) => {
    try {
      await clientesApi.deleteCliente(id);
      await fetchClientes();
      return { success: true };
    } catch (error) {
      console.error('Error deleting client:', error);
      return { success: false, error };
    }
  };

  return {
    clientes,
    totalCount,
    loading,
    pagination,
    filters,
    handlePageChange,
    handlePageSizeChange,
    handleSearch,
    handleFilterChange,
    toggleSort,
    addCliente,
    updateCliente,
    deleteCliente,
    refresh: fetchClientes
  };
};

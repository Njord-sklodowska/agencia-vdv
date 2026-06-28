import { useState, useEffect, useCallback } from 'react';
import { sucursalesApi } from '../api/sucursalesApi';

export const useSucursales = () => {
  const [sucursales, setSucursales] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
  });
  const [filters, setFilters] = useState({
    search: '',
    estado: '',
    provincia: '',
    ciudad: '',
  });
  const [sorting, setSorting] = useState({
    id: 'nombre',
    desc: false,
  });
  const [provincias, setProvincias] = useState([]);

  const fetchProvincias = useCallback(async () => {
    try {
      const data = await sucursalesApi.getSucursales({ page_size: 1000 });
      const todasLasSucursales = data.results || data;
      const provsUnicas = [...new Set(todasLasSucursales.map(s => s.provincia).filter(Boolean))];
      setProvincias(provsUnicas.sort());
    } catch (error) {
      console.error('Error fetching provincias:', error);
    }
  }, []);

  const fetchSucursales = useCallback(async () => {
    setLoading(true);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        search: filters.search,
        estado: filters.estado,
        provincia: filters.provincia,
        ciudad: filters.ciudad,
        ordering: sorting.desc ? `-${sorting.id}` : sorting.id,
      };
      
      const data = await sucursalesApi.getSucursales(params);
      
      setSucursales(data.results || data);
      setTotalCount(data.count || 0);
    } catch (error) {
      console.error('Error fetching sucursales:', error);
    } finally {
      setLoading(false);
    }
  }, [pagination, filters, sorting]);

  useEffect(() => {
    fetchProvincias();
  }, [fetchProvincias]);

  useEffect(() => {
    fetchSucursales();
  }, [fetchSucursales]);

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

  const addSucursal = async (data) => {
    await sucursalesApi.createSucursal(data);
    await fetchSucursales();
  };

  const updateSucursal = async (id, data) => {
    await sucursalesApi.updateSucursal(id, data);
    await fetchSucursales();
  };

  const deleteSucursal = async (id) => {
    await sucursalesApi.deleteSucursal(id);
    await fetchSucursales();
  };

  return {
    sucursales,
    totalCount,
    loading,
    pagination,
    filters,
    sorting,
    provincias,
    handlePageChange,
    handlePageSizeChange,
    handleSearch,
    handleFilterChange,
    toggleSort,
    addSucursal,
    updateSucursal,
    deleteSucursal,
    refresh: fetchSucursales
  };
};

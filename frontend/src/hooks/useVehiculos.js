import { useState, useEffect, useCallback } from 'react';
import { inventarioApi } from '../api/inventarioApi';

export const useVehiculos = () => {
  const [vehicles, setVehicles] = useState([]);
  const [totalCount, setTotalCount] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [marcas, setMarcas] = useState([]);
  const [modelos, setModelos] = useState([]);

  const [pagination, setPagination] = useState({
    page: 1,
    pageSize: 10,
  });

  const [filters, setFilters] = useState({
    marca: '',
    modelo: '',
    estado: '',
    search: '',
  });

  const [sorting, setSorting] = useState({
    id: 'anio',
    desc: false,
  });

  const fetchVehicles = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const params = {
        page: pagination.page,
        page_size: pagination.pageSize,
        marca: filters.marca || undefined,
        modelo: filters.modelo || undefined,
        estado: filters.estado || undefined,
        search: filters.search || undefined,
        ordering: sorting.desc ? `-${sorting.id}` : sorting.id,
      };

      const data = await inventarioApi.getVehiculos(params);
      
      if (Array.isArray(data)) {
        setVehicles(data);
        setTotalCount(data.length);
      } else if (data && data.results) {
        setVehicles(data.results);
        setTotalCount(data.count || 0);
      } else {
        setVehicles([]);
        setTotalCount(0);
      }
    } catch (err) {
      setError(err.message || 'Error al cargar los vehículos');
      console.error('useVehiculos fetch error:', err);
    } finally {
      setIsLoading(false);
    }
  }, [pagination, filters, sorting]);

  const fetchMarcas = useCallback(async () => {
    try {
      const data = await inventarioApi.getMarcas();
      setMarcas(data);
    } catch (err) {
      console.error('Error fetching marcas:', err);
    }
  }, []);

  const fetchModelos = useCallback(async (marcaId = null) => {
    try {
      const data = await inventarioApi.getModelos(marcaId);
      setModelos(data);
    } catch (err) {
      console.error('Error fetching modelos:', err);
    }
  }, []);

  useEffect(() => {
    fetchVehicles();
    fetchMarcas();
    fetchModelos(); // Carga inicial de todos los modelos
  }, [fetchVehicles, fetchMarcas]);

  useEffect(() => {
    if (filters.marca) {
      fetchModelos(filters.marca);
    } else {
      fetchModelos();
    }
  }, [filters.marca, fetchModelos]);

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
    setFilters(prev => {
      const nextFilters = { ...prev, [field]: value };
      // Si cambia la marca, resetear el modelo seleccionado
      if (field === 'marca') {
        nextFilters.modelo = '';
      }
      return nextFilters;
    });
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

  const deleteVehiculo = async (id) => {
    try {
      await inventarioApi.deleteVehiculo(id);
      await fetchVehicles();
      return { success: true };
    } catch (err) {
      console.error('useVehiculos delete error:', err);
      throw err;
    }
  };

  return {
    vehicles,
    totalCount,
    isLoading,
    error,
    pagination,
    filters,
    marcas,
    modelos,
    handlePageChange,
    handlePageSizeChange,
    handleSearch,
    handleFilterChange,
    toggleSort,
    sorting,
    refresh: fetchVehicles,
    deleteVehiculo,
  };
};

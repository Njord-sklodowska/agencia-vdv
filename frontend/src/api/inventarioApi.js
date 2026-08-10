import api from './axiosConfig';

export const inventarioApi = {
  getVehiculos: async (params = {}) => {
    try {
      const response = await api.get('/inventario/vehiculos/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching vehicles:', error);
      throw error;  
    }
  },

  getMarcas: async () => {
    try {
      const response = await api.get('/inventario/marcas/');
      return response.data;
    } catch (error) {
      console.error('Error fetching brands:', error);
      throw error;
    }
  },

  getModelos: async (marcaId = null) => {
    try {
      const params = marcaId ? { marca: marcaId } : {};
      const response = await api.get('/inventario/modelos/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching models:', error);
      throw error;
    }
  },

  getTalleres: async (params = {}) => {
    try {
      const response = await api.get('/inventario/talleres/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching talleres:', error);
      throw error;
    }
  },

  getTallerById: async (id) => {
    try {
      const response = await api.get(`/inventario/talleres/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching taller ${id}:`, error);
      throw error;
    }
  },

  createTaller: async (data) => {
    try {
      const response = await api.post('/inventario/talleres/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating taller:', error);
      throw error;
    }
  },

  updateTaller: async (id, data) => {
    try {
      const response = await api.patch(`/inventario/talleres/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error(`Error updating taller ${id}:`, error);
      throw error;
    }
  },

  deleteTaller: async (id) => {
    try {
      const response = await api.delete(`/inventario/talleres/${id}/`);
      return response.data;
    } catch (error) {
      console.error('Error deleting taller:', error);
      throw error;
    }
  },

  getVehiculoById: async (id) => {
    try {
      const response = await api.get(`/inventario/vehiculos/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching vehicle ${id}:`, error);
      throw error;
    }
  },

  getStats: async () => {
    try {
      const response = await api.get('/inventario/vehiculos/stats/');
      return response.data;
    } catch (error) {
      console.error('Error fetching stats:', error);
      throw error;
    }
  },

  createVehiculo: async (data) => {
    try {
      const response = await api.post('/inventario/vehiculos/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating vehicle:', error);
      throw error;
    }
  },

  updateVehiculo: async (id, data) => {
    try {
      const response = await api.patch(`/inventario/vehiculos/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error(`Error updating vehicle ${id}:`, error);
      throw error;
    }
  },

  deleteVehiculo: async (id) => {
    try {
      const response = await api.post(`/inventario/vehiculos/${id}/desactivar/`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting vehicle ${id}:`, error);
      throw error;
    }
  },

  // --- Gestión de Fotografías ---

  getVehiculoFotos: async (vehiculoId) => {
    try {
      const response = await api.get(`/inventario/vehiculos/${vehiculoId}/fotos/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching photos for vehicle ${vehiculoId}:`, error);
      throw error;
    }
  },

  uploadVehiculoFoto: async (vehiculoId, file) => {
    try {
      const formData = new FormData();
      formData.append('vehiculo', vehiculoId);
      formData.append('archivo', file);

      const response = await api.post('/inventario/fotos/subir/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      return response.data;
    } catch (error) {
      console.error('Error uploading vehicle photo:', error);
      throw error;
    }
  },

  deleteVehiculoFoto: async (fotoId) => {
    try {
      const response = await api.delete(`/inventario/fotos/${fotoId}/`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting photo ${fotoId}:`, error);
      throw error;
    }
  },

  setPortadaFoto: async (fotoId) => {
    try {
      const response = await api.post(`/inventario/fotos/${fotoId}/set_portada/`);
      return response.data;
    } catch (error) {
      console.error(`Error setting cover photo ${fotoId}:`, error);
      throw error;
    }
  },
};


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
};

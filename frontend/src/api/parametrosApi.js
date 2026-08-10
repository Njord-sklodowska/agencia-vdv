import api from './axiosConfig';

export const parametrosApi = {
  getParametros: async (params = {}) => {
    try {
      const response = await api.get('/parametro_sistema/parametros/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching parametros:', error);
      throw error;
    }
  },

  getParametroById: async (id) => {
    try {
      const response = await api.get(`/parametro_sistema/parametros/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error fetching parametro ${id}:`, error);
      throw error;
    }
  },

  updateParametro: async (id, data) => {
    try {
      const response = await api.patch(`/parametro_sistema/parametros/${id}/`, data);
      return response.data;
    } catch (error) {
      console.error(`Error updating parametro ${id}:`, error);
      throw error;
    }
  },

  createParametro: async (data) => {
    try {
      const response = await api.post('/parametro_sistema/parametros/', data);
      return response.data;
    } catch (error) {
      console.error('Error creating parametro:', error);
      throw error;
    }
  },

  deleteParametro: async (id) => {
    try {
      const response = await api.delete(`/parametro_sistema/parametros/${id}/`);
      return response.data;
    } catch (error) {
      console.error(`Error deleting parametro ${id}:`, error);
      throw error;
    }
  },
};

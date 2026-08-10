import api from './axiosConfig';

export const usuariosApi = {
  getUsuarios: async (params = {}) => {
    try {
      const response = await api.get('/usuario/usuarios/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching usuarios:', error);
      throw error;
    }
  },
};

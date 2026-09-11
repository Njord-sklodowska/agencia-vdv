import api from './axiosConfig';

export const auditoriaApi = {
  getLogs: async (params = {}) => {
    try {
      const response = await api.get('/auditoria/logs/', { params });
      return response.data;
    } catch (error) {
      console.error('Error fetching audit logs:', error);
      throw error;
    }
  },
};

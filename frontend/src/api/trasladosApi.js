import { axiosInstance } from './axiosConfig';

export const trasladosApi = {
  async getTraslados(params = {}) {
    const response = await axiosInstance.get('/inventario/traslados/', { params });
    return response.data;
  },

  async getTrasladoById(id) {
    const response = await axiosInstance.get(`/inventario/traslados/${id}/`);
    return response.data;
  },

  async createTraslado(data) {
    const response = await axiosInstance.post('/inventario/traslados/', data);
    return response.data;
  },

  async updateTraslado(id, data) {
    const response = await axiosInstance.patch(`/inventario/traslados/${id}/`, data);
    return response.data;
  },

  async deleteTraslado(id) {
    const response = await axiosInstance.delete(`/inventario/traslados/${id}/`);
    return response.data;
  },

  async confirmarTraslado(id) {
    const response = await axiosInstance.post(`/inventario/traslados/${id}/confirmar/`);
    return response.data;
  },

  async cancelarTraslado(id) {
    const response = await axiosInstance.post(`/inventario/traslados/${id}/cancelar/`);
    return response.data;
  },
};

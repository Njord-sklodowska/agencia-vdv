import { axiosInstance } from './axiosConfig';

export const sucursalesApi = {
  async getSucursales(params = {}) {
    const response = await axiosInstance.get('/sucursal/sucursales/', { params });
    return response.data;
  },

  async getSucursalById(id) {
    const response = await axiosInstance.get(`/sucursal/sucursales/${id}/`);
    return response.data;
  },

  async createSucursal(data) {
    const response = await axiosInstance.post('/sucursal/sucursales/', data);
    return response.data;
  },

  async updateSucursal(id, data) {
    const response = await axiosInstance.patch(`/sucursal/sucursales/${id}/`, data);
    return response.data;
  },

  async deleteSucursal(id) {
    const response = await axiosInstance.delete(`/sucursal/sucursales/${id}/`);
    return response.data;
  },
};

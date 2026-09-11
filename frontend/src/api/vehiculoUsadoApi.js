import { axiosInstance } from './axiosConfig';

export const vehiculoUsadoApi = {
  /**
   * Obtiene la lista de vehículos usados con paginación y filtros server-side.
   */
  async getVehiculosUsados(params = {}) {
    const response = await axiosInstance.get('/inventario/vehiculos-usados/', { params });
    return response.data;
  },

  /**
   * Obtiene el detalle de una evaluación de usado específica.
   */
  async getVehiculoUsadoById(id) {
    const response = await axiosInstance.get(`/inventario/vehiculos-usados/${id}/`);
    return response.data;
  },

  /**
   * Crea una nueva evaluación de vehículo usado.
   */
  async createVehiculoUsado(data) {
    const response = await axiosInstance.post('/inventario/vehiculos-usados/', data);
    return response.data;
  },

  /**
   * Actualiza una evaluación de vehículo usado existente.
   */
  async updateVehiculoUsado(id, data) {
    const response = await axiosInstance.patch(`/inventario/vehiculos-usados/${id}/`, data);
    return response.data;
  },

  /**
   * Elimina una evaluación de vehículo usado.
   */
  async deleteVehiculoUsado(id) {
    const response = await axiosInstance.delete(`/inventario/vehiculos-usados/${id}/`);
    return response.data;
  },
};

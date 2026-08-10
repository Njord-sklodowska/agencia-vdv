import { axiosInstance } from './axiosConfig';

export const clientesApi = {
  /**
   * Obtiene la lista de clientes con paginación y filtros server-side.
   */
  async getClientes(params = {}) {
    const response = await axiosInstance.get('/clientes/', { params });
    return response.data;
  },

  /**
   * Obtiene el detalle de un cliente específico.
   */
  async getClienteById(id) {
    const response = await axiosInstance.get(`/clientes/${id}/`);
    return response.data;
  },

  /**
   * Crea un nuevo cliente.
   */
  async createCliente(data) {
    const response = await axiosInstance.post('/clientes/', data);
    return response.data;
  },

  /**
   * Actualiza un cliente existente.
   */
  async updateCliente(id, data) {
    const response = await axiosInstance.patch(`/clientes/${id}/`, data);
    return response.data;
  },

  /**
   * Elimina un cliente (Borrado lógico si el backend lo soporta).
   */
  async deleteCliente(id) {
    const response = await axiosInstance.delete(`/clientes/${id}/`);
    return response.data;
  },
};

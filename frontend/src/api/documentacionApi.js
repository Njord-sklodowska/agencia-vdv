import { axiosInstance } from './axiosConfig';

export const documentacionApi = {
  // --- Documentación de Vehículo ---

  async getDocumentos(params = {}) {
    const response = await axiosInstance.get('/documentacion/documentacion-vehiculo/', { params });
    return response.data;
  },

  async getDocumentoById(id) {
    const response = await axiosInstance.get(`/documentacion/documentacion-vehiculo/${id}/`);
    return response.data;
  },

  /**
   * Crea un documento de vehículo. `data` puede ser un objeto plano o un
   * FormData (cuando incluye archivo_pdf, como en DocumentacionForm).
   */
  async createDocumento(data) {
    const esFormData = data instanceof FormData;
    const response = await axiosInstance.post(
      '/documentacion/documentacion-vehiculo/',
      data,
      esFormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : undefined
    );
    return response.data;
  },

  /**
   * Actualiza un documento existente (PATCH parcial). Igual que createDocumento,
   * acepta objeto plano o FormData si se está reemplazando el archivo_pdf.
   */
  async updateDocumento(id, data) {
    const esFormData = data instanceof FormData;
    const response = await axiosInstance.patch(
      `/documentacion/documentacion-vehiculo/${id}/`,
      data,
      esFormData ? { headers: { 'Content-Type': 'multipart/form-data' } } : undefined
    );
    return response.data;
  },

  async deleteDocumento(id) {
    const response = await axiosInstance.delete(`/documentacion/documentacion-vehiculo/${id}/`);
    return response.data;
  },

  /** RF08: búsqueda de documentación por patente o VIN. */
  async buscarPorPatenteOVin(query) {
    const response = await axiosInstance.get('/documentacion/documentacion-vehiculo/buscar/', {
      params: { q: query },
    });
    return response.data;
  },

  /** RN-18: estado agregado de documentación de un vehículo (completa/faltantes). */
  async getEstadoVehiculo(vehiculoId) {
    const response = await axiosInstance.get(
      `/documentacion/documentacion-vehiculo/estado-vehiculo/${vehiculoId}/`
    );
    return response.data;
  },

  /** Documentos vencidos o próximos a vencer (default: 30 días). */
  async getAlertasVencimiento(dias = 30) {
    const response = await axiosInstance.get('/documentacion/documentacion-vehiculo/alertas-vencimiento/', {
      params: { dias },
    });
    return response.data;
  },

  // --- Tipos de Documento ---

  async getTiposDocumento(params = {}) {
    const response = await axiosInstance.get('/documentacion/tipos-documento/', { params });
    return response.data;
  },

  async getTipoDocumentoById(id) {
    const response = await axiosInstance.get(`/documentacion/tipos-documento/${id}/`);
    return response.data;
  },

  async createTipoDocumento(data) {
    const response = await axiosInstance.post('/documentacion/tipos-documento/', data);
    return response.data;
  },

  async updateTipoDocumento(id, data) {
    const response = await axiosInstance.patch(`/documentacion/tipos-documento/${id}/`, data);
    return response.data;
  },

  async deleteTipoDocumento(id) {
    const response = await axiosInstance.delete(`/documentacion/tipos-documento/${id}/`);
    return response.data;
  },

  // --- Gestores ---

  async getGestores(params = {}) {
    const response = await axiosInstance.get('/documentacion/gestores/', { params });
    return response.data;
  },

  async getGestorById(id) {
    const response = await axiosInstance.get(`/documentacion/gestores/${id}/`);
    return response.data;
  },

  async createGestor(data) {
    const response = await axiosInstance.post('/documentacion/gestores/', data);
    return response.data;
  },

  async updateGestor(id, data) {
    const response = await axiosInstance.patch(`/documentacion/gestores/${id}/`, data);
    return response.data;
  },

  async deleteGestor(id) {
    const response = await axiosInstance.delete(`/documentacion/gestores/${id}/`);
    return response.data;
  },
};
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/api/inventario';

// Configuración base con el token JWT (el que implementó Sergio)
const getAuthHeaders = () => {
  const token = localStorage.getItem('token'); // Asumiendo que guardas el JWT aquí
  return {
    headers: { Authorization: `Bearer ${token}` }
  };
};

export const crearVehiculo = async (data) => {
  return await axios.post(`${API_URL}/vehiculos/`, data, getAuthHeaders());
};

// Podemos agregar más aquí (getVehiculos, etc.)
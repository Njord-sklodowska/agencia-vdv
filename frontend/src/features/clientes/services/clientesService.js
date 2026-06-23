import api from '../../../services/api'; // Ajusta los ../ según donde lo crees

export const getClientes = () => {
  return api.get('clientes/'); // Esto llamará a http://127.0.0.1:8000/api/clientes/
};
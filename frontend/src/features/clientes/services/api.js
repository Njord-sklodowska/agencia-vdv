// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/', // Esta es la puerta de entrada a Django
});

export default api;
import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../api/axiosConfig';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('accessToken'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (token) {
      // Aquí podrías llamar a un endpoint /me/ para validar el token al recargar la página
      setUser({ username: 'Usuario' }); 
    }
    setLoading(false);
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await api.post('/token/', { username, password });
      const { access, refresh } = response.data;
      
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      
      setToken(access);
      setUser({ username });
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.detail || 'Error de autenticación' };
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, token, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../api/axiosConfig';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('accessToken'));
  const [sucursalId, setSucursalId] = useState(localStorage.getItem('sucursalId'));
  const [loading, setLoading] = useState(true);

  const fetchUserProfile = async () => {
    try {
      const response = await api.get('/usuario/usuarios/me/');
      setUser(response.data);
      if (response.data.sucursal) {
        setSucursalId(response.data.sucursal);
      }
    } catch (error) {
      console.error('Error fetching user profile:', error);
      logout();
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (token) {
      fetchUserProfile();
    } else {
      setLoading(false);
    }
  }, [token]);

  const login = async (username, password) => {
    try {
      const response = await api.post('/token/', { username, password });
      const { access, refresh } = response.data;
      
      localStorage.setItem('accessToken', access);
      localStorage.setItem('refreshToken', refresh);
      
      setToken(access);
      
      // Fetch full profile after login to get name, role, etc.
      await fetchUserProfile();
      
      return { success: true };
    } catch (error) {
      return { success: false, message: error.response?.data?.detail || 'Error de autenticación' };
    }
  };

  const logout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('sucursalId');
    setToken(null);
    setSucursalId(null);
    setUser(null);
    setLoading(false);
  };

  return (
    <AuthContext.Provider value={{ user, token, sucursalId, login, logout, loading }}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/auth/Login';
import Layout from './components/common/Layout';
import DashboardPage from './pages/dashboard/DashboardPage';
import StockPage from './pages/inventario/StockPage';
import NuevoVehiculoPage from './pages/inventario/NuevoVehiculoPage';

const PrivateRoute = ({ children }) => {
  const { token } = useAuth();
  return token ? children : <Navigate to="/login" />;
};

const AppRouter = () => {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={
        <PrivateRoute>
          <Layout>
            <DashboardPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/inventario" element={
        <PrivateRoute>
          <Layout>
            <StockPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/inventario/nuevo" element={
        <PrivateRoute>
          <Layout>
            <NuevoVehiculoPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/" element={<Navigate to="/login" />} />
    </Routes>
  );
};

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRouter />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;

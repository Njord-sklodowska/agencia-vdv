<<<<<<< HEAD
<<<<<<< HEAD
import { RouterProvider } from 'react-router-dom';
import { router } from './router/index';

function App() {
  return (
    <RouterProvider router={router} />
  );
}

export default App;
=======
=======
>>>>>>> origin/feature/frontend-pardinho10
import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Login from './pages/auth/Login';
import Layout from './components/common/Layout';
import DashboardPage from './pages/dashboard/DashboardPage';
import StockPage from './pages/inventario/StockPage';
import NuevoVehiculoPage from './pages/inventario/NuevoVehiculoPage';
import ClientesPage from './pages/clientes/ClientesPage';
import ParametrosPage from './pages/administracion/ParametrosPage';
import AuditoriaPage from './pages/administracion/AuditoriaPage';
import UsuariosPage from './pages/administracion/UsuariosPage';
import VehiculoUsadoPage from './pages/inventario/VehiculoUsadoPage';
import TalleresPage from './pages/inventario/TalleresPage';
import TrasladosPage from './pages/inventario/TrasladosPage';
import SucursalesPage from './pages/inventario/SucursalesPage';

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
      <Route path="/clientes" element={
        <PrivateRoute>
          <Layout>
            <ClientesPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/admin/usuarios" element={
        <PrivateRoute>
          <Layout>
            <UsuariosPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/inventario/usados" element={
        <PrivateRoute>
          <Layout>
            <VehiculoUsadoPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/inventario/talleres" element={
        <PrivateRoute>
          <Layout>
            <TalleresPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/inventario/traslados" element={
        <PrivateRoute>
          <Layout>
            <TrasladosPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/gestion/sucursales" element={
        <PrivateRoute>
          <Layout>
            <SucursalesPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/admin/parametros" element={
        <PrivateRoute>
          <Layout>
            <ParametrosPage />
          </Layout>
        </PrivateRoute>
      } />
      <Route path="/admin/auditoria" element={
        <PrivateRoute>
          <Layout>
            <AuditoriaPage />
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
<<<<<<< HEAD
>>>>>>> origin/feature/frontend-pardinho10
=======
>>>>>>> origin/feature/frontend-pardinho10

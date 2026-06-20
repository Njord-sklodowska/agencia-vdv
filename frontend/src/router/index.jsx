import { createBrowserRouter, Navigate } from 'react-router-dom';
import AuthLayout from '../layouts/AuthLayout';
import DashboardLayout from '../layouts/DashboardLayout';
import InventarioPage from '../features/inventario/pages/InventarioPage';
import VehiculosForm from '../features/inventario/components/VehiculosForm';
import ClientesPage from '../features/clientes/pages/ClientesPage';
import ClientesForm from '../features/clientes/components/ClientesForm'; 

export const router = createBrowserRouter([
  {
    // --- 1. RUTAS PÚBLICAS ---
    path: '/login',
    element: <AuthLayout />
  },
  {
    // --- 2. RUTAS PRIVADAS (El sistema por dentro) ---
    path: '/',
    element: <DashboardLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/inventario" replace />
      },
      {
        path: 'inventario',
        element: <InventarioPage />
      },
      {
        // Ojo aquí: sin la barra inclinada al principio
        path: 'inventario/nuevoVehiculo',
        element: (
          <div className="p-4">
            <VehiculosForm />
          </div>
        )
      },
      {
        path: 'clientes', // Dejamos solo esta versión con el contenedor p-4
        element: (
          <div className="p-4">
            <ClientesPage />
          </div>
        )
      },
      {
        path: 'clientes/nuevo', 
        element: (
          <div className="p-4">
            <ClientesForm />
          </div>
        )
      },
      {
        path: 'ventas',
        element: (
          <div className="alert alert-light border p-4 shadow-sm">
            <h3 className="fw-bold text-muted">Módulo de Ventas</h3>
            <p className="mb-0 text-secondary">Bloqueado temporalmente hasta que Cecilia defina las modificaciones de las tablas.</p>
          </div>
        )
      }
    ]
  },
  {
    // --- 3. RUTA DE ESCAPE (Si escriben mal la URL) ---
    path: '*',
    element: <Navigate to="/" replace />
  }
]);
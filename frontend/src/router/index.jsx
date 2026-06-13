
import VehiculosForm from '../features/inventario/components/VehiculosForm';
import { createBrowserRouter, Navigate } from 'react-router-dom'
import AuthLayout from '../layouts/AuthLayout'
import DashboardLayout from '../layouts/DashboardLayout'
import InventarioPage from '../features/inventario/pages/InventarioPage'

export const router = createBrowserRouter([
  {
    // Rutas públicas (Login)
    path: '/login',
    element: <AuthLayout />,
    children: [
      {
        index: true,
        element: (
          <div className="card shadow p-4" style={{ width: '350px' }}>
            <h3 className="text-center mb-3 fw-bold">Iniciar Sesión</h3>
            <div className="mb-3">
              <label className="form-label text-muted smallfw-semibold">Usuario / CUIT</label>
              <input type="text" className="form-control" placeholder="Ej: 20-12345678-9" disabled />
            </div>
            <button className="btn btn-primary w-100 fw-semibold" disabled>
              Simular Login (Próximamente)
            </button>
          </div>
        )
      }
    ]
  },
  {
    // Rutas protegidas (El sistema por dentro)
    path: '/',
    element: <DashboardLayout />,
    children: [
      {
        index: true,
        element: <Navigate to="/inventario" replace /> // Si entra a la raíz, redirige a inventario
      },
      {
        path: 'inventario',
        element: <InventarioPage /> // ¡Tu tabla interactiva de vehículos!
      },
      {
        path: 'clientes',
        element: (
          <div className="alert alert-secondary border-0 p-4 shadow-sm">
            <h3 className="fw-bold">Módulo de Clientes</h3>
            <p className="mb-0 text-muted">Próximo paso en tu plan: Aquí diseñaremos el ABM de clientes, Sol.</p>
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
    // Ruta de escape por si escriben cualquier cosa en la URL
    path: '*',
    element: <Navigate to="/login" replace />
  }
])
import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

// Importamos el Layout y las páginas
import DashboardLayout from './layouts/DashboardLayout'
import InventarioPage from './features/inventario/InventarioPage'
import ClientesPage from './features/clientes/ClientesPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        
        {/* El Layout envuelve a las páginas del sistema */}
        <Route path="/" element={<DashboardLayout />}>
          
          {/* Rutas directas y limpias */}
          <Route path="inventario" element={<InventarioPage />} />
          <Route path="clientes" element={<ClientesPage />} />
          
        </Route>

      </Routes>
    </BrowserRouter>
  )
}

export default App

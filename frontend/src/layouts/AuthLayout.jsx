import React from 'react'
import { Outlet } from 'react-router-dom'

function AuthLayout() {
  return (
    <div className="bg-light min-vh-100 d-flex align-items-center justify-content-center">
      {/* El Outlet es el espacio donde React Router va a renderizar el formulario de Login */}
      <Outlet />
    </div>
  )
}

export default AuthLayout
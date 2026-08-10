import React from 'react'
import { Outlet } from 'react-router-dom'

function AuthLayout() {
  return (
    // Agregamos container-fluid para que sea idéntico a tus listas responsivas
    <div className="container-fluid bg-light min-vh-100 d-flex align-items-center justify-content-center">
      <Outlet />
    </div>
  )
}

export default AuthLayout
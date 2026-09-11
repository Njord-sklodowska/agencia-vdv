# 🗺️ ROADMAP: Desarrollo Frontend - Agencia VDV

Este documento define la hoja de ruta para la construcción del frontend de la concesionaria.

---

## 🚀 Sprint 0: "The Show-off" (Demostración)
**Objetivo:** Tener una presencia visual impactante y funcional. Mostrar que la arquitectura está montada y que el diseño es profesional.

- [x] **Infraestructura Base:**
    - [x] Configuración de Vite + React.
    - [x] Implementación de paleta de colores moderna (`#454A7B`).
    - [x] Configuración de `AppRouter.jsx` y rutas básicas.
- [x] **Autenticación Real:**
    - [x] Conexión con SimpleJWT (Backend).
    - [x] Pantalla de Login funcional con usuario real.
    - [x] Gestión de estado global con `AuthContext`.
- [x] **UI de Sistema:**
    - [x] Layout base: Navbar + Sidebar + Footer con Bootstrap 5.
- [x] **Pantallas de Impacto:**
    - [x] **Dashboard:** Página principal con KPIs básicos.
    - [x] **Inventario/Stock:** Tabla de vehículos con datos reales usando TanStack Table.

---

## 🔑 Sprint 1: Fundación, Auth y Seguridad
**Objetivo:** Convertir la maqueta en una aplicación real conectada al backend.

- [x] **Capa de Comunicación:**
    - [x] `axiosConfig.js`: Instancia base + interceptores JWT.
    - [x] Configuración de CORS en Django.
- [x] **Estado Global:**
    - [x] `AuthContext.jsx`: user, token, rol.
    - [x] Hook `useAuth.js` para acceso simplificado.
    - [x] Perfil de usuario real en Navbar (`/me/`).
- [x] **Seguridad de Rutas:**
    - [x] `PrivateRoute.jsx`: Bloqueo de acceso a usuarios no autenticados.
    - [x] `RoleRoute.jsx`: Restricción de páginas según el nivel de rol.

---

## 🚗 Sprint 2: Módulo de Inventario y Configuración (Core)
**Objetivo:** Gestión completa del stock de vehículos y parámetros del sistema, implementando la carga de datos desde el frontend.

- [x] **Fase 1: Visualización y Filtros (Frontend)**
    - [x] Conexión de `VehiculoTabla.jsx` con la API real (paginación y filtros server-side).
    - [x] Implementación de `FiltrosStock.jsx` (Marca, Modelo, Estado).
- [x] **Fase 2: Gestión de Datos (Frontend + Backend)**
    - [x] Formulario de Alta/Edición (`VehiculoForm.jsx`) con validaciones de VIN y Patente.
    - [x] **Módulo de Fotografías:** Implementación completa (Subida, Portada, Zoom y Eliminación).
    - [x] **Módulo de Traslados:** Implementar interfaz de movimiento de vehículos entre sucursales $\rightarrow$ API.
    - [x] **Lógica de Vehículos Usados:** Evaluación técnica y Tasación (Estándar de Oro).
    - [x] **Gestión de Talleres:** CRUD y administración de centros de servicio.
    - [x] **Gestión de Sucursales:** Administración de sedes y puntos de venta.
- [x] **Fase 3: Administración del Sistema (Frontend)**
    - [x] Panel de **Parámetros del Sistema** (CRUD completo conectado a la API).
    - [x] Visor de **Auditoría** (Logs de actividad del sistema con filtros y paginación).
    - [x] Sistema de Auditoría Automática (`AuditMixin`) implementada en Backend.
    - [ ] Gestión de **Usuarios** (Interfaz básica implementada $\rightarrow$ Pendiente CRUD completo).

---

## 👥 Sprint 3: Clientes y Flujo de Ventas
**Objetivo:** Implementar el ciclo comercial completo.

- [x] **Módulo de Clientes (Sprinting ahead ✅):**
    - [x] CRUD completo conectado a la API.
    - [x] Implementación de Tabla Profesional: Paginación, Filtrado y Ordenamiento Server-Side.
    - [x] Modal de Vista Detallada (Read-only).
    - [x] Borrado Lógico (Desactivación) implementada.
    - [x] Estética "Modern ERP" aplicada al 100%.
- [ ] **El Proceso de Venta (Multi-paso):**
    - [ ] Flujo completo desde selección de cliente hasta generación de boleto.

---

## 💰 Sprint 4: Cobranzas y Documentación
**Objetivo:** Control administrativo y legal de las operaciones.

- [ ] **Gestión de Cobranzas:**
    - [ ] Control de Títulos y Créditos Internos.
    - [ ] Sistema de alertas de vencimiento.
- [ ] **Documentación:**
    - [ ] Estado documental por vehículo y gestión de gestores.

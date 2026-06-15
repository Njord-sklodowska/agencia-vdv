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
- [ ] **UI de Sistema (Próximo Paso):**
    - [ ] Layout base: Navbar + Sidebar + Footer con Bootstrap 5.
- [ ] **Pantallas de Impacto:**
    - [ ] **Dashboard:** Página principal con KPIs básicos (estáticos/reales).
    - [ ] **Inventario/Stock:** Tabla de vehículos con datos reales usando TanStack Table.

---

## 🔑 Sprint 1: Fundación, Auth y Seguridad
**Objetivo:** Convertir la maqueta en una aplicación real conectada al backend.

- [x] **Capa de Comunicación:**
    - [x] `axiosConfig.js`: Instancia base + interceptores JWT.
    - [x] Configuración de CORS en Django.
- [x] **Estado Global:**
    - [x] `AuthContext.jsx`: user, token, rol.
    - [x] Hook `useAuth.js` para acceso simplificado.
- [ ] **Seguridad de Rutas:**
    - [ ] `PrivateRoute.jsx`: Bloqueo de acceso a usuarios no autenticados.
    - [ ] `RoleRoute.jsx`: Restricción de páginas según el nivel de rol.

---

## 🚗 Sprint 2: Módulo de Inventario (Core)
**Objetivo:** Gestión completa del stock de vehículos.

- [ ] **Vistas de Stock:**
    - [ ] Conexión de `VehiculoTabla.jsx` con la API real (paginación y filtros server-side).
    - [ ] Implementación de `FiltrosStock.jsx` (Marca, Modelo, Estado).
- [ ] **Gestión de Vehículos:**
    - [ ] Formulario de Alta/Edición (`VehiculoForm.jsx`) con validaciones de VIN y Patente.
    - [ ] Lógica de Vehículos Usados (Evaluación técnica).
    - [ ] Sistema de carga de fotografías y ordenamiento.

---

## 👥 Sprint 3: Clientes y Flujo de Ventas
**Objetivo:** Implementar el ciclo comercial completo.

- [ ] **Módulo de Clientes:**
    - [ ] CRUD de Clientes (Físicos y Jurídicos).
    - [ ] Buscador rápido por DNI/CUIT para uso en ventas.
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

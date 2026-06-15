# 🚗 Agencia VDV - Project Knowledge Base

Este documento sirve como guía rápida de inducción para cualquier agente o desarrollador que se integre al proyecto. Contiene la arquitectura, el estado actual y las decisiones técnicas clave.

---

## 📝 Resumen del Proyecto
**Agencia VDV** es un sistema de gestión (SaaS) diseñado para una concesionaria de vehículos con soporte para múltiples sucursales. El sistema abarca desde el control de inventario hasta el ciclo completo de venta, cobranzas y gestión documental.

## 🛠️ Stack Tecnológico

### Backend (API)
- **Framework:** Django + Django REST Framework (DRF).
- **Base de Datos:** MySQL.
- **Autenticación:** SimpleJWT (JSON Web Tokens).
- **Documentación:** `drf-spectacular` (OpenAPI 3).
- **Estructura:** Basada en aplicaciones modulares (`sucursal`, `usuario`, `inventario`, etc.).

### Frontend (Cliente)
- **Framework:** React 18 + Vite.
- **Estilos:** Bootstrap 5 (estilos personalizados en `custom.css`).
- **Tablas:** TanStack Table v8 (Implementación **Server-Side** para paginación y filtros).
- **Comunicación:** Axios con interceptores para:
    - Inyección automática del token JWT.
    - Envío de `X-Sucursal-ID` para filtrado de datos por sucursal.
- **Estado Global:** `AuthContext` (Único contexto global que maneja usuario, rol, token y sucursal activa).

---

## 🔐 Sistema de Roles y Permisos
El acceso al sistema está restringido por niveles de rol:

| Rol | Nivel | Permisos Principales |
| :--- | :---: | :--- |
| **Vendedor** | 1 | Lectura de stock de sucursal, creación de borradores de venta. |
| **Administrativo** | 2 | Gestión de stock, ventas, clientes y cobranzas de su sucursal. |
| **Gerente** | 3 | Todo lo anterior + Reportes gerenciales de su sucursal. |
| **Superadmin** | 4 | Acceso total a todas las sucursales, configuración y usuarios. |

---

## 🏗️ Arquitectura y Decisiones Clave

### 1. Manejo de Sucursales
- Los usuarios (excepto el Superadmin) están vinculados a una única sucursal.
- El filtrado de datos se realiza en el **Backend** basándose en el ID de la sucursal enviado en la request.

### 2. Flujo de Datos en Frontend
- **API Layer:** `src/api/` contiene instancias específicas por módulo (ej. `inventarioApi.js`).
- **Hooks Layer:** `src/hooks/` encapsula la lógica de negocio y llamadas a la API (ej. `useVehiculos.js`).
- **Component Layer:** División entre componentes comunes, de inventario, ventas, etc.

### 3. Seguridad de Rutas
- `PrivateRoute.jsx`: Protege rutas que requieren autenticación.
- `RoleRoute.jsx`: Restringe rutas basándose en el nivel mínimo de rol requerido.

---

## 📊 Estado Actual del Desarrollo (Snapshot)

### Frontend ✅ (Avanzado)
- Estructura de carpetas completa.
- Maquetado de la mayoría de las vistas y componentes (Tablas, Formularios, Dashboards).
- Sistema de rutas y autenticación implementado.
- Capa de hooks y API definida (aunque algunos endpoints están pendientes en el backend).

### Backend 🛠️ (Inicial)
- Configuración base de Django y MySQL completada.
- Modelo de usuario personalizado implementado.
- Apps básicas creadas: `sucursal`, `usuario`, `inventario`.
- **Pendientes:** Implementar apps de `clientes`, `ventas`, `cobranzas` y `documentacion`.

---

## 🗺️ Roadmap de Implementación
El proyecto sigue una estrategia de Sprints:
1. **Sprint 0 & 1:** Infraestructura, Auth y Seguridad (En proceso/Finalizando).
2. **Sprint 2:** Módulo de Inventario Core (En proceso).
3. **Sprint 3:** Clientes y Flujo de Ventas.
4. **Sprint 4:** Cobranzas y Documentación Legal.

## 🔑 Acceso y Usuarios de Prueba

Para fines de desarrollo y testing, el sistema cuenta con usuarios predefinidos cargados mediante el comando `load_usuarios`.

**Contraseña universal:** `Pass123!`

| Usuario | Rol | Sucursal |
| :--- | :--- | :--- |
| `admin_global` | Administrador | Global (Todas) |
| `gerente_san_miguel` | Gerente | San Miguel |
| `gerente_concepcion` | Gerente | Concepción |
| `gerente_banda` | Gerente | Banda |
| `vendedor_sm1` / `vendedor_sm2` | Vendedor | San Miguel |
| `vendedor_con1` / `vendedor_con2` | Vendedor | Concepción |
| `vendedor_ban1` / `vendedor_ban2` | Vendedor | Banda |

---

## 🎨 Optimización Visual y Comparativa (Junio 2026)

Se realizó un análisis comparativo entre el frontend actual y una propuesta externa (`agencia-vdv-frontend-sol`).

### 1. Análisis de Funcionalidad vs Estética
- **Frontend Actual:** Posee una arquitectura profesional basada en **TanStack Table v8**, con paginación server-side, ordenamiento avanzado y modales de gestión. Es la base funcional del proyecto.
- **Propuesta Externa:** Implementa una arquitectura basada en *Features* y una estética de "Modern ERP". Sin embargo, su funcionalidad de tablas y formularios es básica (HTML estático), careciendo de la potencia técnica del proyecto principal.

### 2. Actualización de la Identidad Visual
Se adoptó la paleta de colores de la propuesta externa para modernizar la interfaz sin comprometer la robustez técnica.

**Detalle de Colores por Componente:**

- **Menú Lateral (Sidebar):**
    - Fondo: `#1a202c` (Gris oscuro azulado).
    - Enlaces Activos: `bg-success` ($\approx$ `#198754`) con texto blanco.
    - Enlaces Inactivos: `text-white-50`.
    - Botón Salida: `text-danger` ($\approx$ `#dc3545`).
- **Barra Superior (Navbar):**
    - Fondo: `bg-white` (`#ffffff`).
    - Texto e Iconos: `text-secondary` ($\approx$ `#6c757d`).
- **Áreas de Fondo:**
    - Fondo General: `#f7fafc` (Blanco azulado).
    - Área de Trabajo (Main): `#edf2f7` (Gris azulado claro).
- **Tarjetas (Cards) y Contenedores:**
    - Fondo Exterior: `#e2e8f0` (Gris claro).
    - Encabezado de Título: `#2c3e50` (Azul medianoche) con texto blanco.
    - Cuerpo/Barra de Acciones: `bg-white` (`#ffffff`).
- **Tablas de Datos:**
    - Encabezados: `#cbd5e0` (Fondo general) y `#a0aec0` (Celdas).
    - Filas: Alternancia entre `#ffffff` (Paares) y `#c4c4c4ef` (Impares).
    - Resaltado de Búsqueda: `#f6d9a2` (Amarillo pálido).
    - Bordes: `#cbd5e0`.
- **Componentes de Interacción:**
    - Botón Principal (Agregar): `#f0ad4e` (Naranja/Dorado) con texto negro.
    - Badges de Estado:
        - Activo/En Stock: `#5cb85c` (Verde).
        - Reservado/Deudor: `#f0ad4e` o `#e67e22` (Naranja).
        - Vendido/Inactivo: `#d9534f` (Rojo).

**Cambios Estructurales:**
- Se eliminaron restricciones de ancho fijo en `index.css` para lograr un diseño **Full-Width**.
- Actualización de variables globales en `layout.css` y `custom.css`.


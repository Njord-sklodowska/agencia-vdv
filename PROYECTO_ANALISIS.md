# 🚗 Agencia VDV - Project Knowledge Base (Updated)

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
- **Estructura:** Basada en aplicaciones modulares (`sucursal`, `usuario`, `inventario`, `clientes`, `auditoria`, `parametro_sistema`).

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

### 4. Auditoría Automática (Estándar de Oro)
- Se implementó un `AuditMixin` en el backend que intercepta automáticamente las acciones de `CREAR`, `MODIFICAR` y `ELIMINAR`.
- Registra: Usuario, Acción, Módulo, Tabla, ID del registro, IP y Fecha.
- Implementada en: Clientes, Inventario y Parámetros del Sistema.

---

## 🗄️ Estructura de Datos y Flujo de Carga

(Mantenido según diseño original)

---

## 📊 Estado Actual del Desarrollo (Snapshot - Junio 2026)

### Frontend ✅ (Muy Avanzado)
- Estructura de carpetas completa.
- Maquetado de la mayoría de las vistas y componentes (Tablas, Formularios, Dashboards).
- Sistema de rutas y autenticación implementado con perfil de usuario real.
- Capa de hooks y API definida.
- **Módulos Finalizados (Interfaz & Lógica)**: Clientes, Inventario (incluyendo Galería de Fotos), Parámetros del Sistema, Visor de Auditoría.
- **En Proceso**: Gestión de Usuarios (Interfaz base terminada).

### Backend ⚙️ (Core Implementado)
- Configuración base de Django y MySQL completada.
- Modelo de usuario personalizado implementado.
- **Apps Core Implementadas**: `sucursal`, `usuario`, `inventario`, `clientes`, `auditoria`, `parametro_sistema`.
- **Pendientes**: Implementar apps de `ventas`, `cobranzas` y `documentacion`.

---

## 🗺️ Roadmap de Implementación
El proyecto sigue una estrategia de Sprints:
1. **Sprint 0 & 1:** Infraestructura, Auth y Seguridad (Completado).
2. **Sprint 2:** Módulo de Inventario y Configuración (Casi completado - Pendiente CRUD Usuarios).
3. **Sprint 3:** Clientes y Flujo de Ventas (Clientes completado - Ventas pendiente).
4. **Sprint 4:** Cobranzas y Documentación.

# 🚗 Agencia VDV - Project Knowledge Base (Updated)

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
- **Estructura:** Basada en aplicaciones modulares (`sucursal`, `usuario`, `inventario`, `clientes`, `auditoria`, `parametro_sistema`).

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

### 4. Auditoría Automática (Estándar de Oro)
- Se implementó un `AuditMixin` en el backend que intercepta automáticamente las acciones de `CREAR`, `MODIFICAR` y `ELIMINAR`.
- Registra: Usuario, Acción, Módulo, Tabla, ID del registro, IP y Fecha.
- Implementada en: Clientes, Inventario y Parámetros del Sistema.

---

## 🗄️ Estructura de Datos y Flujo de Carga

(Mantenido según diseño original)

---

## 📊 Estado Actual del Desarrollo (Snapshot - Junio 2026)

### Frontend ✅ (Muy Avanzado)
- Estructura de carpetas completa.
- Maquetado de la mayoría de las vistas y componentes (Tablas, Formularios, Dashboards).
- Sistema de rutas y autenticación implementado con perfil de usuario real.
- Capa de hooks y API definida.
- **Módulos Finalizados (Interfaz & Lógica)**: Clientes, Inventario (incluyendo Galería de Fotos), Parámetros del Sistema, Visor de Auditoría.
- **En Proceso**: Gestión de Usuarios (Interfaz base terminada).

### Backend ⚙️ (Core Implementado)
- Configuración base de Django y MySQL completada.
- Modelo de usuario personalizado implementado.
- **Apps Core Implementadas**: `sucursal`, `usuario`, `inventario`, `clientes`, `auditoria`, `parametro_sistema`.
- **Pendientes**: Implementar apps de `ventas`, `cobranzas` y `documentacion`.

---

## 🗺️ Roadmap de Implementación
El proyecto sigue una estrategia de Sprints:
1. **Sprint 0 & 1:** Infraestructura, Auth y Seguridad (Completado).
2. **Sprint 2:** Módulo de Inventario y Configuración (Casi completado - Pendiente CRUD Usuarios).
3. **Sprint 3:** Clientes y Flujo de Ventas (Clientes completado - Ventas pendiente).
4. **Sprint 4:** Cobranzas y Documentación.



                                                                                                                                                  
 🔍 DIAGNÓSTICO COMPLETO - AgenciaVDV                                                                                                             
                                                                                                                                                   
 📊 RESUMEN EJECUTIVO                                                                                                                              
                                                                                                                                                   
 ┌────────────────────┬─────────────────────┬──────────────┐                                                                                       
 │ Aspecto            │ Estado              │ % Completado │                                                                                       
 ├────────────────────┼─────────────────────┼──────────────┤                                                                                       
 │ Backend            │ Funcional           │ ~70%         │                                                                                       
 ├────────────────────┼─────────────────────┼──────────────┤                                                                                       
 │ Frontend           │ Funcional           │ ~65%         │                                                                                       
 ├────────────────────┼─────────────────────┼──────────────┤                                                                                       
 │ Módulos Core       │ Implementados       │ 4/7          │                                                                                       
 ├────────────────────┼─────────────────────┼──────────────┤                                                                                       
 │ Módulos Pendientes │ Placeholders vacíos │ 3/7          │                                                                                       
 └────────────────────┴─────────────────────┴──────────────┘                                                                                       
                                                                                                                                                   
 ────────────────────────────────────────────────────────────────────────────────                                                                  
                                                                                                                                                   
 ✅ LO QUE TENEMOS (FUNCIONAL)                                                                                                                     
                                                                                                                                                   
 ### BACKEND                                                                                                                                       
                                                                                                                                                   
 #### Apps Implementadas (6/6 core)                                                                                                                
                                                                                                                                                   
 ┌───────────────────┬──────────────────────────────────────────────────────────┬───────────────────────────────┬────────────┬──────┬────────────┐ 
 │ App               │ Modelos                                                  │ ViewSet                       │ Serializer │ URLs │ Auditoría  │ 
 ├───────────────────┼──────────────────────────────────────────────────────────┼───────────────────────────────┼────────────┼──────┼────────────┤ 
 │ usuario           │ Usuario, Rol                                             │ ✅ UsuarioViewSet             │ ✅         │ ✅   │ ❌         │ 
 ├───────────────────┼──────────────────────────────────────────────────────────┼───────────────────────────────┼────────────┼──────┼────────────┤ 
 │ sucursal          │ Sucursal                                                 │ ✅ SucursalViewSet            │ ✅         │ ✅   │ ❌         │ 
 ├───────────────────┼──────────────────────────────────────────────────────────┼───────────────────────────────┼────────────┼──────┼────────────┤ 
 │ inventario        │ Marca, Modelo, Vehiculo, Fotografia_Vehiculo, Taller,    │ ✅ 7 ViewSets                 │ ✅         │ ✅   │ ✅         │ 
 │                   │ VehiculoUsado, TrasladoVehiculo                          │                               │            │      │ (parcial)  │ 
 ├───────────────────┼──────────────────────────────────────────────────────────┼───────────────────────────────┼────────────┼──────┼────────────┤ 
 │ clientes          │ Cliente                                                  │ ✅ ClienteViewSet             │ ✅         │ ✅   │ ✅         │ 
 ├───────────────────┼──────────────────────────────────────────────────────────┼───────────────────────────────┼────────────┼──────┼────────────┤ 
 │ auditoria         │ LogAuditoria                                             │ ✅ LogAuditoriaViewSet        │ ✅         │ ✅   │ N/A        │ 
 │                   │                                                          │ (ReadOnly)                    │            │      │            │ 
 ├───────────────────┼──────────────────────────────────────────────────────────┼───────────────────────────────┼────────────┼──────┼────────────┤ 
 │ parametro_sistema │ ParametroSistema                                         │ ✅ ParametroSistemaViewSet    │ ✅         │ ✅   │ ❌         │ 
 └───────────────────┴──────────────────────────────────────────────────────────┴───────────────────────────────┴────────────┴──────┴────────────┘ 
                                                                                                                                                   
 #### Características Backend Funcionales:                                                                                                         
                                                                                                                                                   
 - ✅ Autenticación JWT (SimpleJWT)                                                                                                                
 - ✅ Paginación estándar (StandardResultsSetPagination)                                                                                           
 - ✅ Auditoría automática (AuditMixin en Clientes e Inventario)                                                                                   
 - ✅ Filtros y búsqueda (DjangoFilterBackend + SearchFilter)                                                                                      
 - ✅ Borrado lógico (Clientes, Vehículos)                                                                                                         
 - ✅ Validaciones de modelo (VIN, patente, DNI/CUIT)                                                                                              
 - ✅ Documentación API (drf-spectacular/Swagger)                                                                                                  
 - ✅ CORS configurado                                                                                                                             
                                                                                                                                                   
 ### FRONTEND                                                                                                                                      
                                                                                                                                                   
 #### Estructura de Carpetas (128 archivos JS/JSX)                                                                                                 
                                                                                                                                                   
 ┌─────────────┬──────────────┬────────────────────────────────────────────────────┐                                                               
 │ Carpeta     │ Archivos     │ Estado                                             │                                                               
 ├─────────────┼──────────────┼────────────────────────────────────────────────────┤                                                               
 │ api/        │ 14 archivos  │ 6 implementados, 4 vacíos                          │                                                               
 ├─────────────┼──────────────┼────────────────────────────────────────────────────┤                                                               
 │ hooks/      │ 18 archivos  │ 14 implementados, 4 vacíos                         │                                                               
 ├─────────────┼──────────────┼────────────────────────────────────────────────────┤                                                               
 │ pages/      │ 25 archivos  │ 17 implementados, 8 vacíos                         │                                                               
 ├─────────────┼──────────────┼────────────────────────────────────────────────────┤                                                               
 │ components/ │ ~50 archivos │ ~35 implementados, ~15 vacíos                      │                                                               
 ├─────────────┼──────────────┼────────────────────────────────────────────────────┤                                                               
 │ context/    │ 1 archivo    │ ✅ AuthContext                                     │                                                               
 ├─────────────┼──────────────┼────────────────────────────────────────────────────┤                                                               
 │ routes/     │ 2 archivos   │ 1 implementado (PrivateRoute), 1 vacío (RoleRoute) │                                                               
 ├─────────────┼──────────────┼────────────────────────────────────────────────────┤                                                               
 │ styles/     │ 3 archivos   │ ✅                                                 │                                                               
 ├─────────────┼──────────────┼────────────────────────────────────────────────────┤                                                               
 │ utils/      │ 4 archivos   │ ✅                                                 │                                                               
 └─────────────┴──────────────┴────────────────────────────────────────────────────┘                                                               
                                                                                                                                                   
 #### Páginas Implementadas (17/25)                                                                                                                
                                                                                                                                                   
 ┌─────────────────┬───────────────────────┬─────────────────┐                                                                                     
 │ Página          │ Ruta                  │ Estado          │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Login           │ /login                │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Dashboard       │ /dashboard            │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Stock Vehículos │ /inventario           │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Nuevo Vehículo  │ /inventario/nuevo     │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Vehículo Usado  │ /inventario/usados    │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Traslados       │ /inventario/traslados │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Talleres        │ /inventario/talleres  │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Sucursales      │ /gestion/sucursales   │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Clientes        │ /clientes             │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Parámetros      │ /admin/parametros     │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Auditoría       │ /admin/auditoria      │ ✅              │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Usuarios        │ /admin/usuarios       │ ⚠️ Solo lectura │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Ventas          │ /ventas               │ ❌ Vacío        │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Cobranzas       │ /cobranzas            │ ❌ Vacío        │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Documentación   │ /documentacion        │ ❌ Vacío        │                                                                                     
 ├─────────────────┼───────────────────────┼─────────────────┤                                                                                     
 │ Reportes        │ /reportes             │ ❌ Vacío        │                                                                                     
 └─────────────────┴───────────────────────┴─────────────────┘                                                                                     
                                                                                                                                                   
 #### Hooks Implementados (14/18)                                                                                                                  
                                                                                                                                                   
 ┌───────────────────┬──────────┐                                                                                                                  
 │ Hook              │ Estado   │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useAuth           │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useClientes       │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useVehiculos      │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useVehiculoUsados │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useTraslados      │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useTalleres       │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useSucursales     │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useParametros     │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useAuditoria      │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useUsuarios       │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ usePermisos       │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useSucursal       │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useVehiculoForm   │ ✅       │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useAlertas        │ ❌ Vacío │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useCobranzas      │ ❌ Vacío │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useDocumentacion  │ ❌ Vacío │                                                                                                                  
 ├───────────────────┼──────────┤                                                                                                                  
 │ useOperaciones    │ ❌ Vacío │                                                                                                                  
 └───────────────────┴──────────┘                                                                                                                  
                                                                                                                                                   
 #### APIs Implementadas (6/10)                                                                                                                    
                                                                                                                                                   
 ┌─────────────────────┬───────────────────────────────┐                                                                                           
 │ API                 │ Estado                        │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ axiosConfig.js      │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ authApi.js          │ ✅ (implícito en axiosConfig) │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ clientesApi.js      │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ inventarioApi.js    │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ sucursalesApi.js    │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ usuariosApi.js      │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ vehiculoUsadoApi.js │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ trasladosApi.js     │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ auditoriaApi.js     │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ parametrosApi.js    │ ✅                            │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ ventasApi.js        │ ❌ Vacío                      │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ cobranzasApi.js     │ ❌ Vacío                      │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ documentacionApi.js │ ❌ Vacío                      │                                                                                           
 ├─────────────────────┼───────────────────────────────┤                                                                                           
 │ reportesApi.js      │ ❌ Vacío                      │                                                                                           
 └─────────────────────┴───────────────────────────────┘                                                                                           
                                                                                                                                                   
 ────────────────────────────────────────────────────────────────────────────────                                                                  
                                                                                                                                                   
 ❌ LO QUE NOS FALTA                                                                                                                               
                                                                                                                                                   
 ### 1. BACKEND - Apps Faltantes (CRÍTICO)                                                                                                         
                                                                                                                                                   
 ┌───────────────┬──────────────────────────────────────────────┬────────────────────┐                                                             
 │ App           │ Modelos Necesarios                           │ Endpoints          │                                                             
 ├───────────────┼──────────────────────────────────────────────┼────────────────────┤                                                             
 │ ventas        │ OperacionVenta, FormaPago, Anticipo, Boleto  │ CRUD completo      │                                                             
 ├───────────────┼──────────────────────────────────────────────┼────────────────────┤                                                             
 │ cobranzas     │ Titulo, CreditoInterno, Cuota, RegistroCobro │ CRUD + alertas     │                                                             
 ├───────────────┼──────────────────────────────────────────────┼────────────────────┤                                                             
 │ documentacion │ Documento, Gestor, EstadoDocumental          │ CRUD + seguimiento │                                                             
 └───────────────┴──────────────────────────────────────────────┴────────────────────┘                                                             
                                                                                                                                                   
 ### 2. BACKEND - Mejoras Pendientes                                                                                                               
                                                                                                                                                   
 ┌───────────────────────────────────┬────────────────────────────┬───────────┐                                                                    
 │ Problema                          │ Archivo                    │ Prioridad │                                                                    
 ├───────────────────────────────────┼────────────────────────────┼───────────┤                                                                    
 │ Normalización de teléfonos        │ clientes/models.py         │ 🔴 Alta   │                                                                    
 ├───────────────────────────────────┼────────────────────────────┼───────────┤                                                                    
 │ Auditoría en Usuarios             │ usuario/views.py           │ 🟡 Media  │                                                                    
 ├───────────────────────────────────┼────────────────────────────┼───────────┤                                                                    
 │ Auditoría en Parámetros           │ parametro_sistema/views.py │ 🟡 Media  │                                                                    
 ├───────────────────────────────────┼────────────────────────────┼───────────┤                                                                    
 │ Auditoría en Sucursales           │ sucursal/views.py          │ 🟡 Media  │                                                                    
 ├───────────────────────────────────┼────────────────────────────┼───────────┤                                                                    
 │ Asignación automática de sucursal │ inventario/views.py        │ 🟡 Media  │                                                                    
 ├───────────────────────────────────┼────────────────────────────┼───────────┤                                                                    
 │ Permisos por rol                  │ Todos los ViewSets         │ 🟡 Media  │                                                                    
 └───────────────────────────────────┴────────────────────────────┴───────────┘                                                                    
                                                                                                                                                   
 ### 3. FRONTEND - Páginas Vacías (8 archivos)                                                                                                     
                                                                                                                                                   
 ┌──────────────────────────┬─────────────────────────┬───────────────────────┐                                                                    
 │ Página                   │ Ruta                    │ Dependencias          │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ NuevaVentaPage.jsx       │ /ventas/nueva           │ Backend ventas        │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ OperacionesPage.jsx      │ /ventas                 │ Backend ventas        │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ VentaDetallePage.jsx     │ /ventas/:id             │ Backend ventas        │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ AnticiposPage.jsx        │ /ventas/anticipos       │ Backend ventas        │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ TitulosPage.jsx          │ /cobranzas              │ Backend cobranzas     │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ CreditosInternosPage.jsx │ /cobranzas/creditos     │ Backend cobranzas     │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ AlertasPage.jsx          │ /cobranzas/alertas      │ Backend cobranzas     │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ DocumentacionPage.jsx    │ /documentacion          │ Backend documentacion │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ GestoresPage.jsx         │ /documentacion/gestores │ Backend documentacion │                                                                    
 ├──────────────────────────┼─────────────────────────┼───────────────────────┤                                                                    
 │ ReportesPage.jsx         │ /reportes               │ Backend reportes      │                                                                    
 └──────────────────────────┴─────────────────────────┴───────────────────────┘                                                                    
                                                                                                                                                   
 ### 4. FRONTEND - Componentes Vacíos (24 archivos)                                                                                                
                                                                                                                                                   
 ┌───────────────────┬───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐ 
 │ Módulo            │ Componentes Faltantes                                                                                                     │ 
 ├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
 │ ventas (7)        │ AnticipoBadge, AnticipoForm, BoletoPDF, FormasPagoForm, OperacionForm, OperacionTabla, ResumenOperacion                   │ 
 ├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
 │ cobranzas (7)     │ AlertasVencimiento, CreditoInternoForm, CreditoInternoTabla, CuotaTabla, PagoCuotaForm, RegistroCobroForm, TituloDetalle, │ 
 │                   │ TituloTabla                                                                                                               │ 
 ├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
 │ documentacion (3) │ DocumentacionTabla, DocumentoForm, GestorForm, GestorTabla                                                                │ 
 ├───────────────────┼───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤ 
 │ reportes (5)      │ ReporteCheques, ReporteConsolidado, ReporteDeudores, ReporteStock, ReporteVentas                                          │ 
 └───────────────────┴───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘ 
                                                                                                                                                   
 ### 5. FRONTEND - Rutas Faltantes                                                                                                                 
                                                                                                                                                   
 ┌─────────────────────────┬──────────────────────┬──────────────────┐                                                                             
 │ Ruta                    │ Página               │ Estado           │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /ventas                 │ OperacionesPage      │ ❌ No registrada │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /ventas/nueva           │ NuevaVentaPage       │ ❌ No registrada │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /ventas/:id             │ VentaDetallePage     │ ❌ No registrada │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /cobranzas              │ TitulosPage          │ ❌ No registrada │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /cobranzas/creditos     │ CreditosInternosPage │ ❌ No registrada │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /cobranzas/alertas      │ AlertasPage          │ ❌ No registrada │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /documentacion          │ DocumentacionPage    │ ❌ No registrada │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /documentacion/gestores │ GestoresPage         │ ❌ No registrada │                                                                             
 ├─────────────────────────┼──────────────────────┼──────────────────┤                                                                             
 │ /reportes               │ ReportesPage         │ ❌ No registrada │                                                                             
 └─────────────────────────┴──────────────────────┴──────────────────┘                                                                             
                                                                                                                                                   
 ### 6. FRONTEND - Funcionalidades Incompletas                                                                                                     
                                                                                                                                                   
 ┌──────────────────┬─────────────────────────────────────────────────────────────────────┐                                                        
 │ Componente       │ Problema                                                            │                                                        
 ├──────────────────┼─────────────────────────────────────────────────────────────────────┤                                                        
 │ UsuariosPage.jsx │ Botón "Nuevo Usuario" no tiene funcionalidad (solo lectura)         │                                                        
 ├──────────────────┼─────────────────────────────────────────────────────────────────────┤                                                        
 │ Navbar.jsx       │ Menú hamburguesa no se visualiza correctamente                      │                                                        
 ├──────────────────┼─────────────────────────────────────────────────────────────────────┤                                                        
 │ RoleRoute.jsx    │ Archivo vacío - No hay protección por roles                         │                                                        
 ├──────────────────┼─────────────────────────────────────────────────────────────────────┤                                                        
 │ Sidebar.jsx      │ Links a Ventas/Cobranzas/Documentos/Reportes rotos (páginas vacías) │                                                        
 └──────────────────┴─────────────────────────────────────────────────────────────────────┘                                                        
                                                                                                                                                   
 ────────────────────────────────────────────────────────────────────────────────                                                                  
                                                                                                                                                   
 ⚠️ PROBLEMAS CRÍTICOS DETECTADOS                                                                                                                  
                                                                                                                                                   
 ### 1. 🔴 Búsqueda por Teléfono No Funciona                                                                                                       
                                                                                                                                                   
 Causa: Los teléfonos se guardan con formato (381-220-334) pero la búsqueda usa icontains que no coincide.                                         
 Solución: Normalizar teléfonos en clean() del modelo (como se hace con DNI/CUIT).                                                                 
                                                                                                                                                   
 ### 2. 🔴 Sin Protección por Roles                                                                                                                
                                                                                                                                                   
 Causa: RoleRoute.jsx está vacío. Solo existe PrivateRoute (verifica autenticación).                                                               
 Impacto: Cualquier usuario autenticado puede acceder a cualquier ruta.                                                                            
                                                                                                                                                   
 ### 3. 🟡 Auditoría Incompleta                                                                                                                    
                                                                                                                                                   
 Causa: AuditMixin no está aplicado en:                                                                                                            
 - UsuarioViewSet                                                                                                                                  
 - SucursalViewSet                                                                                                                                 
 - ParametroSistemaViewSet                                                                                                                         
                                                                                                                                                   
 ### 4. 🟡 Usuarios Solo Lectura                                                                                                                   
                                                                                                                                                   
 Causa: UsuariosPage.jsx no tiene modal de creación/edición.                                                                                       
 Impacto: No se pueden crear nuevos usuarios desde el frontend.                                                                                    
                                                                                                                                                   
 ### 5. 🟡 Sidebar con Links Rotos                                                                                                                 
                                                                                                                                                   
 Causa: Links a Ventas, Cobranzas, Documentación, Reportes apuntan a páginas vacías.                                                               
                                                                                                                                                   
 ────────────────────────────────────────────────────────────────────────────────                                                                  
                                                                                                                                                   
 📈 MÉTRICAS DEL PROYECTO                                                                                                                          
                                                                                                                                                   
 ┌───────────────────────┬───────────────────────┐                                                                                                 
 │ Métrica               │ Valor                 │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ Total archivos Python │ ~40                   │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ Total archivos JS/JSX │ ~128                  │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ Líneas de CSS         │ ~800+ (erp-theme.css) │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ Modelos Django        │ 12                    │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ ViewSets              │ 10                    │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ Endpoints API         │ ~30                   │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ Páginas React         │ 17/25 (68%)           │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ Hooks                 │ 14/18 (78%)           │                                                                                                 
 ├───────────────────────┼───────────────────────┤                                                                                                 
 │ Componentes           │ ~35/50 (70%)          │                                                                                                 
 └───────────────────────┴───────────────────────┘                                                                                                 
                                                                                                                                                   
 ────────────────────────────────────────────────────────────────────────────────                                                                  
                                                                                                                                                   
 🎯 RECOMENDACIONES DE PRIORIDAD                                                                                                                   
                                                                                                                                                   
 ### Prioridad 1 (Crítica - Bloqueadores)                                                                                                          
                                                                                                                                                   
 1. Normalizar teléfonos en backend                                                                                                                
 2. Implementar RoleRoute para seguridad                                                                                                           
 3. Completar módulo de Ventas (backend + frontend)                                                                                                
                                                                                                                                                   
 ### Prioridad 2 (Alta - Funcionalidad)                                                                                                            
                                                                                                                                                   
 4. Completar módulo de Cobranzas                                                                                                                  
 5. Completar módulo de Documentación                                                                                                              
 6. Implementar CRUD de Usuarios en frontend                                                                                                       
                                                                                                                                                   
 ### Prioridad 3 (Media - Mejoras)                                                                                                                 
                                                                                                                                                   
 7. Agregar auditoría a Usuarios, Sucursales, Parámetros                                                                                           
 8. Implementar Reportes                                                                                                                           
 9. Arreglar menú hamburguesa del Navbar                                                                                                           
                                                                                                                                                   
 ### Prioridad 4 (Baja - Polish)                                                                                                                   
                                                                                                                                                   
 10. Tests (todos los tests.py están vacíos)                                                                                                       
 11. Documentación de API (Swagger está configurado pero incompleto)                                                                               
 12. Manejo de errores más robusto en frontend                                                                                                     
                                                                                                                                                   
 ────────────────────────────────────────────────────────────────────────────────   

# 🚗 Del Valle Automotores — Documento Técnico Frontend
## React + Vite SaaS para Concesionaria Multisucursal

---

## 1. Stack Tecnológico

| Capa | Tecnología | Versión sugerida |
|------|-----------|-----------------|
| Framework | React + Vite | React 18 / Vite 5 |
| Estilos | Bootstrap 5 (sin librería integrada) | 5.3.x |
| Íconos | Bootstrap Icons | 1.11.x |
| Rutas | React Router Dom | v6 |
| HTTP Client | Axios + interceptores JWT | 1.x |
| Tablas | TanStack Table v8 | 8.x |
| Estado global | Context API (solo AuthContext) | — |
| Formularios | HTML controlado + validación manual | — |
| Variables de entorno | Vite `.env` | — |

> **Decisión de arquitectura:** Se usa un único `AuthContext` en lugar de múltiples contextos.
> `AppContext` fue descartado para reducir complejidad. Todo el estado global necesario
> (sucursal activa, usuario, rol) vive en `AuthContext`.

---

## 2. Roles y Permisos

Basado en **RF02** y **RN-22** del documento:

| Rol | Nivel | Acceso |
|-----|-------|--------|
| `superadministrador` | 4 | Todo el sistema. Las 3 sucursales. Configuración y usuarios |
| `gerente` | 3 | Módulos operativos de su sucursal. Reportes gerenciales |
| `administrativo` | 2 | Stock, ventas, clientes, cobranzas, documentación de su sucursal |
| `vendedor` | 1 | Solo lectura de stock de su sucursal. Sin datos financieros |

> Cada usuario opera únicamente en su sucursal asignada, salvo el superadministrador.

---

## 3. División de Tareas por Perfil

### Ariel (lógica y arquitectura)
- Configuración inicial del proyecto (Vite, Router, Axios, Context)
- `axiosConfig.js` con interceptores JWT
- `AuthContext.jsx` y todos los custom hooks
- TanStack Table (configuración server-side)
- Rutas protegidas por rol
- Validaciones de negocio (RN-08, RN-13, RN-21, etc.)
- Conexión de componentes con la API

### Sol (vistas y componentes visuales)
- Layout base: Navbar, Sidebar, Footer con Bootstrap 5
- Formularios HTML (Ariel le pasa los handlers y el estado)
- Páginas estáticas: estructura de tablas, cards, badges de estado
- Estilos y overrides de Bootstrap en `custom.css`
- Maquetado de páginas una vez que la lógica está conectada

### Flujo de trabajo entre los dos
```
Ariel arma el hook (ej: useVehiculos.js)
    ↓
Ariel define la interfaz del componente (qué props recibe)
    ↓
Sol arma el HTML/Bootstrap del componente
    ↓
Ariel conecta la lógica al componente de Sol
```

---

## 4. Estructura de Carpetas

```
frontend/
│
├── public/
│   └── favicon.ico
│
├── src/
│   │
│   ├── api/                              # Capa de comunicación con Django REST — ARIEL
│   │   ├── axiosConfig.js                # Instancia base + interceptores JWT
│   │   ├── authApi.js                    # login, logout, refresh token
│   │   ├── usuariosApi.js                # CRUD usuarios
│   │   ├── sucursalesApi.js              # CRUD sucursales, parámetros del sistema
│   │   ├── inventarioApi.js              # Vehículos, marcas, modelos, fotos, traslados
│   │   ├── clientesApi.js                # CRUD clientes (físicos y jurídicos)
│   │   ├── ventasApi.js                  # Operaciones, formas de pago, anticipos
│   │   ├── cobranzasApi.js               # Títulos de crédito, crédito interno, cuotas
│   │   ├── documentacionApi.js           # Documentación vehicular, gestores
│   │   └── reportesApi.js                # Reportes gerenciales y operativos
│   │
│   ├── context/                          # Estado global — ARIEL
│   │   └── AuthContext.jsx               # user, token, rol, sucursal, login(), logout()
│   │                                     # ⚠️ AppContext descartado: todo vive acá
│   │
│   ├── hooks/                            # Custom Hooks por dominio — ARIEL
│   │   ├── useAuth.js                    # Consume AuthContext
│   │   ├── useSucursal.js                # Sucursal activa del usuario
│   │   ├── useVehiculos.js               # Paginación server-side, filtros de stock
│   │   ├── useClientes.js                # Búsqueda por DNI/CUIT, historial
│   │   ├── useOperaciones.js             # Ciclo de vida de ventas
│   │   ├── useCobranzas.js               # Títulos, cuotas, mora
│   │   ├── useDocumentacion.js           # Estado documental por vehículo
│   │   ├── useAlertas.js                 # Cheques/cuotas próximas a vencer
│   │   └── usePermisos.js                # Verificación de permisos por rol
│   │
│   ├── components/                       # Componentes reutilizables
│   │   │
│   │   ├── common/                       # Componentes globales — SOL (estructura) + ARIEL (lógica)
│   │   │   ├── Navbar.jsx                # Navbar con sucursal activa y usuario
│   │   │   ├── Sidebar.jsx               # Menú lateral dinámico según rol
│   │   │   ├── Footer.jsx
│   │   │   ├── Spinner.jsx               # Loading global
│   │   │   ├── Alerta.jsx                # Mensajes success / error / warning
│   │   │   ├── ModalConfirmar.jsx        # Modal genérico de confirmación
│   │   │   ├── BadgeEstado.jsx           # Badge para estados (en_stock, vendido, etc.)
│   │   │   ├── SucursalSelector.jsx      # Solo visible para superadministrador
│   │   │   └── PaginadorTabla.jsx        # Paginación server-side reutilizable
│   │   │
│   │   ├── inventario/                   # SOL (HTML/Bootstrap) + ARIEL (lógica)
│   │   │   ├── VehiculoTabla.jsx         # TanStack Table con filtros y paginación
│   │   │   ├── VehiculoForm.jsx          # Alta/edición vehículo (0km y usado)
│   │   │   ├── VehiculoCard.jsx          # Card con foto portada
│   │   │   ├── VehiculoFotos.jsx         # Upload y orden de hasta 10 fotos
│   │   │   ├── VehiculoUsadoForm.jsx     # Evaluación técnica con estados de componentes
│   │   │   ├── TrasladoForm.jsx          # Traslado entre sucursales
│   │   │   └── FiltrosStock.jsx          # Filtros por marca/modelo/estado/sucursal
│   │   │
│   │   ├── clientes/                     # SOL (HTML/Bootstrap) + ARIEL (lógica)
│   │   │   ├── ClienteTabla.jsx          # TanStack Table con búsqueda DNI/CUIT
│   │   │   ├── ClienteForm.jsx           # Alta/edición persona física y jurídica
│   │   │   ├── ClienteHistorial.jsx      # Historial de operaciones del cliente
│   │   │   └── ClienteBuscador.jsx       # Buscador rápido para usar en ventas
│   │   │
│   │   ├── ventas/                       # SOL (HTML/Bootstrap) + ARIEL (lógica)
│   │   │   ├── OperacionTabla.jsx        # TanStack Table con estados y filtros
│   │   │   ├── OperacionForm.jsx         # Formulario multi-paso de nueva venta
│   │   │   ├── FormasPagoForm.jsx        # Selector de formas de pago combinadas
│   │   │   ├── ResumenOperacion.jsx      # Resumen antes de confirmar
│   │   │   ├── AnticipoBadge.jsx         # Indicador de seña/anticipo previo
│   │   │   ├── AnticipoForm.jsx          # Registro de señas y anticipos
│   │   │   └── BoletoPDF.jsx             # Visualización del boleto generado en PDF
│   │   │
│   │   ├── cobranzas/                    # SOL (HTML/Bootstrap) + ARIEL (lógica)
│   │   │   ├── TituloTabla.jsx           # TanStack Table cheques y pagarés
│   │   │   ├── TituloDetalle.jsx         # Detalle con historial de cobros
│   │   │   ├── RegistroCobroForm.jsx     # Registro de pago de título
│   │   │   ├── CreditoInternoTabla.jsx   # TanStack Table créditos internos
│   │   │   ├── CreditoInternoForm.jsx    # Alta con plan de cuotas automático
│   │   │   ├── CuotaTabla.jsx            # Cuotas con estado de mora
│   │   │   ├── PagoCuotaForm.jsx         # Registro de pago de cuota
│   │   │   └── AlertasVencimiento.jsx    # Panel de cheques/cuotas próximas a vencer
│   │   │
│   │   ├── documentacion/                # SOL (HTML/Bootstrap) + ARIEL (lógica)
│   │   │   ├── DocumentacionTabla.jsx    # Estado documental de un vehículo
│   │   │   ├── DocumentoForm.jsx         # Alta/edición con upload PDF
│   │   │   ├── GestorForm.jsx            # Alta/edición gestor externo
│   │   │   └── GestorTabla.jsx           # Lista de gestores activos
│   │   │
│   │   └── reportes/                     # SOL (HTML/Bootstrap) + ARIEL (lógica)
│   │       ├── ReporteVentas.jsx
│   │       ├── ReporteStock.jsx
│   │       ├── ReporteDeudores.jsx
│   │       ├── ReporteCheques.jsx
│   │       └── ReporteConsolidado.jsx    # Solo superadministrador
│   │
│   ├── pages/                            # SOL arma estructura, ARIEL conecta datos
│   │   │
│   │   ├── auth/
│   │   │   └── Login.jsx                 # Login con bloqueo por 3 intentos (RN-21)
│   │   │
│   │   ├── dashboard/
│   │   │   └── DashboardPage.jsx         # KPIs según rol y sucursal activa
│   │   │
│   │   ├── inventario/
│   │   │   ├── StockPage.jsx
│   │   │   ├── VehiculoDetallePage.jsx
│   │   │   ├── NuevoVehiculoPage.jsx
│   │   │   └── TrasladosPage.jsx
│   │   │
│   │   ├── clientes/
│   │   │   ├── ClientesPage.jsx
│   │   │   └── ClienteDetallePage.jsx
│   │   │
│   │   ├── ventas/
│   │   │   ├── OperacionesPage.jsx
│   │   │   ├── NuevaVentaPage.jsx
│   │   │   ├── VentaDetallePage.jsx
│   │   │   └── AnticiposPage.jsx
│   │   │
│   │   ├── cobranzas/
│   │   │   ├── TitulosPage.jsx
│   │   │   ├── CreditosInternosPage.jsx
│   │   │   └── AlertasPage.jsx
│   │   │
│   │   ├── documentacion/
│   │   │   ├── DocumentacionPage.jsx
│   │   │   └── GestoresPage.jsx
│   │   │
│   │   ├── reportes/
│   │   │   └── ReportesPage.jsx
│   │   │
│   │   └── admin/                        # Solo superadministrador — ARIEL
│   │       ├── UsuariosPage.jsx
│   │       ├── SucursalesPage.jsx
│   │       ├── ParametrosPage.jsx
│   │       └── AuditoriaPage.jsx
│   │
│   ├── routes/                           # ARIEL
│   │   ├── AppRouter.jsx                 # Router principal
│   │   ├── PrivateRoute.jsx              # Verifica token válido
│   │   ├── RoleRoute.jsx                 # Verifica rol mínimo requerido
│   │   └── routesConfig.js               # Mapa de rutas con rol requerido
│   │
│   ├── utils/                            # ARIEL
│   │   ├── validaciones.js               # VIN, patente AR, DNI, CUIT, año, pagos
│   │   ├── formatters.js                 # Fechas, moneda ARS/USD, porcentajes
│   │   ├── constants.js                  # Enums del modelo de datos
│   │   └── pdfHelpers.js                 # Helpers para boleto PDF
│   │
│   ├── styles/
│   │   └── custom.css                    # Overrides Bootstrap 5 — SOL
│   │
│   ├── App.jsx
│   └── main.jsx
│
├── .env
├── .env.example
├── .gitignore
├── index.html
├── vite.config.js
└── package.json
```

---

## 5. AuthContext — Único Contexto Global

```javascript
// src/context/AuthContext.jsx

// Estado:
// - user: { id, nombre, apellido, email, rol, sucursal: { id, nombre } }
// - accessToken
// - isAuthenticated
// - intentosFallidos  ← RN-21: bloqueo tras 3 intentos fallidos

// Métodos:
// - login(email, password)   → POST /api/token/
// - logout()                 → limpia estado, redirige a /login
// - refreshToken()           → POST /api/token/refresh/ (llamado por interceptor)
// - tienePermiso(rolMinimo)  → boolean, usa NIVEL_ROL de constants.js
// - esSuperAdmin()           → boolean, shortcut frecuente
// - sucursalActiva           → shortcut a user.sucursal (superadmin puede cambiarlo)
// - setSucursalActiva(id)    → solo habilitado si rol === 'superadministrador'
```

> **¿Por qué no AppContext?** Todo lo que AppContext haría (sucursal activa, alertas)
> puede vivir en AuthContext o en hooks locales de cada página. Menos contextos = menos
> re-renders y menos complejidad para el equipo.

---

## 6. Configuración Axios con JWT

```javascript
// src/api/axiosConfig.js

// 1. Instancia base con VITE_API_URL
// 2. Interceptor de REQUEST:
//    - Adjunta Authorization: Bearer {accessToken}
//    - Adjunta X-Sucursal-ID para filtrado server-side
// 3. Interceptor de RESPONSE:
//    - Si 401 → intenta refresh automático con refreshToken()
//    - Si refresh falla → logout() y redirect /login
//    - Si otro error → rechaza con mensaje legible
```

---

## 7. Rutas Protegidas por Rol

```
/login                     → público
/                          → redirige según rol al dashboard

/dashboard                 → todos los autenticados
/inventario/stock          → vendedor (lectura), administrativo, gerente, superadmin
/inventario/nuevo          → administrativo, gerente, superadmin
/inventario/:id            → todos
/inventario/traslados      → gerente, superadmin
/clientes                  → administrativo, gerente, superadmin
/clientes/:id              → administrativo, gerente, superadmin
/ventas                    → vendedor (borrador), administrativo, gerente, superadmin
/ventas/nueva              → todos los autenticados
/ventas/:id                → administrativo, gerente, superadmin
/ventas/anticipos          → administrativo, gerente, superadmin
/cobranzas/titulos         → administrativo, gerente, superadmin
/cobranzas/creditos        → administrativo, gerente, superadmin
/cobranzas/alertas         → administrativo, gerente, superadmin
/documentacion             → vendedor (lectura), administrativo, gerente, superadmin
/documentacion/gestores    → administrativo, gerente, superadmin
/reportes                  → gerente, superadmin (administrativo: solo operativos)
/admin/usuarios            → superadmin
/admin/sucursales          → superadmin
/admin/parametros          → superadmin
/admin/auditoria           → superadmin
```

---

## 8. TanStack Table — Server-Side

Aplica a todas las tablas. Paginación y ordenamiento resueltos en Django REST:

```javascript
// Parámetros enviados al backend en cada cambio de tabla:
// ?page=1&page_size=20&ordering=-fecha_alta&search=toyota&estado=en_stock&sucursal=1

// VehiculoTabla:    patente/VIN | marca | modelo | año | condición | precio | estado | acciones
// OperacionTabla:   ID | cliente | vehículo | fecha | precio final | estado | vendedor | acciones
// TituloTabla:      tipo | número | banco | fecha cobro | monto | estado | días para vencer | acciones
// CuotaTabla:       N° cuota | vencimiento | monto | estado | días mora | mora acumulada | acciones
```

---

## 9. Lógica de Negocio Clave en Frontend

### Login con bloqueo (RN-21 / CU01)
- Contador local de intentos en `AuthContext`
- Tras 3 intentos → deshabilitar botón + mensaje + timer 15 minutos
- El backend también bloquea; el frontend lo refleja

### Nueva Venta — Flujo multi-paso (CU05 / RF05)
```
Paso 1: Seleccionar cliente (búsqueda por DNI/CUIT o alta rápida)
Paso 2: Seleccionar vehículo (solo en_stock o reservado, misma sucursal)
Paso 3: Formas de pago combinadas (validación en tiempo real: suma = precio_final)
Paso 4: Datos adicionales (vendedor, descuento si aplica RN-11)
Paso 5: Resumen y confirmación → genera boleto PDF
```
> **RN-08 crítico:** El botón "Confirmar" se deshabilita si la suma de formas de pago
> no es exactamente igual al precio final. Validación en tiempo real en `FormasPagoForm`.

### Filtros de stock por sucursal (RN-05 / RF03)
- Vendedor/Administrativo/Gerente: solo ven su sucursal, sin selector visible
- Superadministrador: `SucursalSelector` visible + opción "Todas"

### Alertas de vencimiento (RF06 / RF07 / RN-17)
- Badge en Navbar con contador
- Panel `/cobranzas/alertas` con tres secciones: vencidos hoy, próximos 7 días, en término
- Aplica a cheques, pagarés y cuotas de crédito interno

---

## 10. Constantes y Enums

```javascript
// src/utils/constants.js — basado en ENUMs del modelo de datos

export const ESTADO_VEHICULO = {
  EN_STOCK: 'en_stock', RESERVADO: 'reservado', VENDIDO: 'vendido'
}
export const TIPO_VEHICULO = { CERO_KM: '0km', USADO: 'usado' }
export const TIPO_PAGO = {
  EFECTIVO: 'efectivo', CHEQUE: 'cheque', PAGARE: 'pagare',
  FINANCIAMIENTO_EXTERNO: 'financiamiento_externo',
  CREDITO_INTERNO: 'credito_interno', DOLARES: 'dolares'
}
export const ESTADO_TITULO = {
  PENDIENTE: 'pendiente', HABILITADO: 'habilitado', VENCIDO: 'vencido',
  COBRADO: 'cobrado', RECHAZADO: 'rechazado', EN_GESTION: 'en_gestion'
}
export const ESTADO_OPERACION = {
  BORRADOR: 'borrador', CONFIRMADA: 'confirmada',
  COMPLETADA: 'completada', CANCELADA: 'cancelada'
}
export const ROLES = {
  SUPERADMIN: 'superadministrador', GERENTE: 'gerente',
  ADMINISTRATIVO: 'administrativo', VENDEDOR: 'vendedor'
}
export const NIVEL_ROL = {
  vendedor: 1, administrativo: 2, gerente: 3, superadministrador: 4
}
```

---

## 11. Validaciones Frontend

```javascript
// src/utils/validaciones.js

// VIN: exactamente 17 caracteres alfanuméricos (RN-01)
export const validarVIN = (vin) => /^[A-HJ-NPR-Z0-9]{17}$/.test(vin)

// Patente argentina: AAA-000 o AA-000-AA (RN-01)
export const validarPatente = (p) => /^[A-Z]{3}-\d{3}$|^[A-Z]{2}-\d{3}-[A-Z]{2}$/.test(p)

// Año vehículo entre 1990 y año actual + 1 (RN-23)
export const validarAnio = (anio) => anio >= 1990 && anio <= new Date().getFullYear() + 1

// DNI: 7 u 8 dígitos
export const validarDNI = (dni) => /^\d{7,8}$/.test(dni)

// CUIT: formato XX-XXXXXXXX-X
export const validarCUIT = (cuit) => /^\d{2}-\d{8}-\d{1}$/.test(cuit)

// Cheque: plazo máximo 90 días (RN-13)
export const validarPlazoCheque = (dias) => [0, 30, 60, 90].includes(dias)

// Suma de pagos exacta al precio final (RN-08)
export const validarSumaPagos = (pagos, precioFinal) =>
  pagos.reduce((acc, p) => acc + parseFloat(p.monto || 0), 0) === parseFloat(precioFinal)
```

---

## 12. Dependencias

```json
{
  "dependencies": {
    "react": "^18.3.0",
    "react-dom": "^18.3.0",
    "react-router-dom": "^6.26.0",
    "axios": "^1.7.0",
    "@tanstack/react-table": "^8.20.0",
    "bootstrap": "^5.3.3"
  },
  "devDependencies": {
    "vite": "^5.4.0",
    "@vitejs/plugin-react": "^4.3.0"
  }
}
```

---

## 13. Orden de Desarrollo Sugerido

### Fase 1 — Base (ambos)
| Tarea | Responsable |
|-------|------------|
| Setup Vite + Bootstrap 5 + React Router | Ariel |
| `axiosConfig.js` con interceptores JWT | Ariel |
| `AuthContext.jsx` + `useAuth.js` | Ariel |
| `Login.jsx` — estructura HTML/Bootstrap | Sol |
| Lógica de login + bloqueo en `Login.jsx` | Ariel |
| Layout base: `Navbar` + `Sidebar` HTML | Sol |
| Lógica dinámica del Sidebar por rol | Ariel |

### Fase 2 — Inventario (módulo central)
| Tarea | Responsable |
|-------|------------|
| `inventarioApi.js` + `useVehiculos.js` | Ariel |
| `VehiculoTabla.jsx` HTML/Bootstrap | Sol |
| TanStack Table server-side en `VehiculoTabla` | Ariel |
| `FiltrosStock.jsx` HTML | Sol |
| Lógica de filtros por sucursal/rol | Ariel |
| `VehiculoForm.jsx` HTML | Sol |
| Validaciones VIN, patente, año en form | Ariel |
| `StockPage.jsx` + `NuevoVehiculoPage.jsx` | Ambos |

### Fase 3 — Clientes
| Tarea | Responsable |
|-------|------------|
| `clientesApi.js` + `useClientes.js` | Ariel |
| `ClienteForm.jsx` HTML (física y jurídica) | Sol |
| Lógica condicional física/jurídica | Ariel |
| `ClienteTabla.jsx` + `ClientesPage.jsx` | Ambos |

### Fase 4 — Ventas
| Tarea | Responsable |
|-------|------------|
| `ventasApi.js` + `useOperaciones.js` | Ariel |
| `FormasPagoForm.jsx` HTML | Sol |
| Validación RN-08 en tiempo real | Ariel |
| `OperacionForm.jsx` multi-paso HTML | Sol |
| Lógica del flujo multi-paso | Ariel |
| `NuevaVentaPage.jsx` + `OperacionesPage.jsx` | Ambos |

### Fase 5 — Cobranzas
| Tarea | Responsable |
|-------|------------|
| `cobranzasApi.js` + `useCobranzas.js` | Ariel |
| Tablas HTML: títulos, cuotas | Sol |
| TanStack Table + lógica de mora | Ariel |
| `AlertasVencimiento.jsx` HTML | Sol |
| Lógica de alertas + `useAlertas.js` | Ariel |

### Fase 6 — Documentación
| Tarea | Responsable |
|-------|------------|
| `documentacionApi.js` + `useDocumentacion.js` | Ariel |
| `DocumentacionTabla.jsx` + `DocumentoForm.jsx` HTML | Sol |
| Upload PDF + lógica de estados | Ariel |

### Fase 7 — Reportes y Admin (al final)
| Tarea | Responsable |
|-------|------------|
| Páginas de reportes HTML | Sol |
| Conexión con `reportesApi.js` | Ariel |
| Páginas admin: usuarios, sucursales, parámetros | Ambos |
| `AuditoriaPage.jsx` | Ariel |

---

## 14. Mapeo Frontend ↔ Backend

| App Django | Módulo React |
|-----------|-------------|
| `usuarios` | `pages/admin/UsuariosPage`, `context/AuthContext` |
| `sucursales` | `pages/admin/SucursalesPage`, `pages/admin/ParametrosPage` |
| `inventario` | `pages/inventario/*`, `components/inventario/*` |
| `clientes` | `pages/clientes/*`, `components/clientes/*` |
| `ventas` | `pages/ventas/*`, `components/ventas/*`, `components/cobranzas/*` |
| `documentacion` | `pages/documentacion/*`, `components/documentacion/*` |
| `auditoria` | `pages/admin/AuditoriaPage` |
| `reportes` | `pages/reportes/*`, `components/reportes/*` |

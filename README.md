# 🚗 Agencia VDV

Sistema de gestión (SaaS) para concesionaria de vehículos con soporte para múltiples sucursales. Control de inventario, ventas, cobranzas, clientes y auditoría.

---

## 🛠️ Stack Tecnológico

| Capa | Tecnología |
|------|------------|
| **Backend** | Django + Django REST Framework |
| **Base de Datos** | MySQL |
| **Autenticación** | SimpleJWT (JSON Web Tokens) |
| **Documentación API** | drf-spectacular (OpenAPI 3) |
| **Frontend** | React 18 + Vite |
| **Estilos** | Bootstrap 5 + CSS personalizado |
| **Tablas** | TanStack Table v8 (Server-Side) |
| **Estado Global** | AuthContext |

---

## 📁 Estructura del Proyecto

```
agencia-vdv/
├── backend/                    # API Django
│   ├── config/                 # Configuración global
│   │   ├── settings.py         # Settings de Django
│   │   ├── urls.py             # URLs principales
│   │   ├── mixins.py           # AuditMixin, etc.
│   │   └── pagination.py       # Paginación estándar
│   ├── clientes/               # App de Clientes
│   ├── inventario/             # App de Inventario (Vehículos)
│   ├── sucursal/               # App de Sucursales
│   ├── usuario/                # App de Usuarios y Roles
│   ├── auditoria/              # App de Auditoría
│   ├── parametro_sistema/     # App de Parámetros
│   ├── manage.py
│   └── requirements.txt
│
├── frontend/                   # Cliente React + Vite
│   ├── src/
│   │   ├── api/                # Instancias Axios por módulo
│   │   ├── components/         # Componentes reutilizables
│   │   │   ├── common/         # Navbar, Sidebar, Spinner, etc.
│   │   │   ├── clientes/       # Componentes de Clientes
│   │   │   └── inventario/     # Componentes de Inventario
│   │   ├── pages/              # Páginas por módulo
│   │   │   ├── auth/           # Login
│   │   │   ├── clientes/       # ClientesPage
│   │   │   ├── inventario/     # StockPage, NuevoVehiculo, etc.
│   │   │   ├── administracion/ # Admin pages
│   │   │   └── dashboard/      # Dashboard
│   │   ├── hooks/              # Custom hooks (useAuth, useClientes, etc.)
│   │   ├── context/            # AuthContext
│   │   ├── routes/             # Rutas (PrivateRoute, RoleRoute)
│   │   ├── styles/             # CSS personalizado
│   │   └── utils/              # Utilidades y formateadores
│   ├── package.json
│   └── vite.config.js
│
├── vehiculos_data.json         # Datos de vehículos de ejemplo
└── README.md                   # Este archivo
```

---

## 🔐 Roles y Permisos

| Rol | Nivel | Permisos |
|-----|-------|----------|
| **Vendedor** | 1 | Lectura de stock, borradores de venta |
| **Administrativo** | 2 | Gestión de stock, ventas, clientes, cobranzas |
| **Gerente** | 3 | Todo lo anterior + reportes gerenciales |
| **Superadmin** | 4 | Acceso total a todas las sucursales |

---

## 🧩 Módulos Implementados

### Backend
| App | Estado | Funcionalidades |
|-----|--------|-----------------|
| `clientes` | ✅ Completo | CRUD, validaciones (DNI/CUIT/CUIL), borrado lógico, auditoría |
| `inventario` | ✅ Completo | Vehículos, usados, traslados, talleres, fotos, auditoría |
| `sucursal` | ✅ Completo | CRUD de sucursales |
| `usuario` | ✅ Completo | Usuarios, roles, autenticación JWT |
| `auditoria` | ✅ Completo | Log de acciones automático |
| `parametro_sistema` | ✅ Completo | Configuración del sistema |
| `ventas` | ❌ Pendiente | - |
| `cobranzas` | ❌ Pendiente | - |
| `documentacion` | ❌ Pendiente | - |

### Frontend
| Módulo | Estado |
|--------|--------|
| Login / Auth | ✅ |
| Dashboard | ✅ |
| Clientes | ✅ |
| Inventario | ✅ |
| Sucursales | ✅ |
| Usuarios | ✅ |
| Auditoría | ✅ |
| Parámetros | ✅ |
| Ventas | ❌ Pendiente |
| Cobranzas | ❌ Pendiente |
| Documentación | ❌ Pendiente |

---

## 🚀 Cómo Levantar el Proyecto

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 📊 Estado General

- **Backend:** ~70% completo (core implementado, faltan ventas/cobranzas/documentación)
- **Frontend:** ~65% completo (UI y lógica de módulos core terminada)
- **Próximos pasos:** Implementar ventas, cobranzas y documentación

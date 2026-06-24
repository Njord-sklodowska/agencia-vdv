# 🛠️ Manual de Sincronización: Git & Django REST Framework

Esta guía documenta el proceso completo para integrar cambios de equipo, resolver conflictos de ramas y solucionar desincronizaciones de la base de datos en el proyecto Agencia VDV.

---

## 📑 1. Sincronización de Código (Git)

### Flujo Estándar de Actualización
Cuando un compañero sube cambios, sigue este orden para evitar errores:

1. **Actualizar referencias:** `git fetch origin`
2. **Inspeccionar commits:** `git log HEAD..origin/main --oneline` (cambia `main` por la rama correspondiente).
3. **Fusionar cambios:** `git pull origin main`

### 🚨 Solución a "Ramas Divergentes"
Si al hacer `pull` recibes un error indicando que las ramas han divergido, es porque ambos hicieron commits en el mismo punto de la historia.

**Solución:** Configura la estrategia de fusión (Merge) y vuelve a intentar el pull.
```bash
git config pull.rebase false
git pull origin <nombre-de-la-rama>
```

### ⚔️ Resolución de Conflictos de Fusión
Si Git indica `CONFLICT (content)`, significa que dos personas editaron la misma línea.

1. **Abrir el archivo en VS Code:** Busca las marcas `<<<<<<< HEAD` y `>>>>>>>`.
2. **Decidir:** Elige entre *"Accept Current Change"* (tuyo), *"Accept Incoming Change"* (compañero) o *"Accept Both Changes"*.
3. **Finalizar:**
   ```bash
   git add <archivo_resuelto>
   git commit -m "Resolviendo conflictos en <archivo>"
   ```

---

## 🗄️ 2. Gestión de Base de Datos (Django Migrations)

### Conceptos Fundamentales
Django usa un sistema de "planos" para modificar la base de datos:

- **`makemigrations` (El Plano):** Analiza los cambios en `models.py` y crea un archivo `.py` en la carpeta `migrations/`. **Solo se usa cuando TÚ creas o cambias un modelo.**
- **`migrate` (La Construcción):** Lee los archivos `.py` de las migraciones y ejecuta el SQL real en MySQL. **Se usa siempre que descargues cambios de otros o después de hacer un makemigrations.**

### 🔍 Verificación de Estado
Para saber qué migraciones se han aplicado y cuáles faltan:
```bash
python manage.py showmigrations
```
- `[X]` $\rightarrow$ Aplicada.
- `[ ]` $\rightarrow$ Pendiente.

---

## 🆘 3. Solución de Errores Comunes de Migración

### Error: `Table already exists` o `Duplicate column name`
Esto ocurre cuando la base de datos ya tiene la tabla/columna, pero Django no tiene el registro de que la migración se ejecutó (desincronización).

**La Solución: El comando `--fake`**
Le dice a Django: *"Marca esta migración como hecha, pero NO intentes ejecutar el código SQL"*.

- **Para una migración específica:**
  `python manage.py migrate <app> <nombre_migracion> --fake`
- **Para TODA la aplicación (limpieza total):**
  `python manage.py migrate <app> --fake`

---

## ☢️ 4. La "Opción Nuclear" (Reinicio Total)

Si las migraciones están demasiado corruptas o hay demasiados errores de "Duplicate column", lo más rápido en desarrollo es reiniciar la base de datos.

### Procedimiento de Limpieza Total:

1. **Borrar y recrear la BD en MySQL:**
   ```sql
   DROP DATABASE agencia_vdv;
   CREATE DATABASE agencia_vdv;
   ```

2. **Aplicar migraciones desde cero:**
   ```bash
   python manage.py migrate
   ```

3. **Cargar datos de prueba (Seed):**
   Como la BD está vacía, debes cargar los usuarios y sucursales predefinidos:
   ```bash
   python manage.py load_usuarios
   ```

---

## ⚡ Resumen de Comandos Rápidos

| Situación | Comando |
| :--- | :--- |
| **Sincronizar código** | `git pull origin <rama>` |
| **Error de ramas divergentes** | `git config pull.rebase false` $\rightarrow$ `git pull` |
| **Crear migración propia** | `python manage.py makemigrations` |
| **Aplicar cambios BD** | `python manage.py migrate` |
| **Sincronizar BD sin ejecutar SQL** | `python manage.py migrate <app> --fake` |
| **Ver estado de migraciones** | `python manage.py showmigrations` |
| **Cargar datos iniciales** | `python manage.py load_usuarios` |

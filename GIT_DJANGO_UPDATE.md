# 🔄 Guía de Actualización de Proyecto: Git & Django

Esta guía detalla el procedimiento correcto para integrar cambios realizados por otros miembros del equipo en un proyecto basado en **Django REST Framework**, asegurando que tanto el código como la base de datos se mantengan sincronizados.

---

## 📋 Flujo de Actualización Paso a Paso

### 1. Actualizar Referencias Remotas
Primero, informamos a Git sobre los cambios que existen en el servidor sin alterar nuestros archivos locales.

```bash
git fetch origin
```

### 2. Inspección de Cambios (Opcional pero Recomendado)
Antes de fusionar, es útil saber qué se modificó para evitar sorpresas.

**Ver los mensajes de los nuevos commits:**
```bash
# Cambia 'main' por la rama correspondiente (ej. develop)
git log HEAD..origin/main --oneline
```

**Ver las diferencias exactas en el código:**
```bash
git diff HEAD..origin/main
```

### 3. Descarga y Fusión de Código
Descargamos los cambios y los unimos con nuestro trabajo actual.

```bash
git pull origin main
```

> [!IMPORTANT]
> **Conflictos de Fusión (Merge Conflicts):**
> Si Git indica que hay conflictos, deberás:
> 1. Abrir los archivos en conflicto.
> 2. Resolver manualmente qué líneas de código conservar.
> 3. Ejecutar: `git add <archivo_resuelto>` $\rightarrow$ `git commit -m "Resolviendo conflictos"`.

### 4. Actualización de la Base de Datos (Crucial)
En Django, los cambios en los modelos (nuevas tablas o campos) se registran en archivos de migración. Si no ejecutas este paso, el sistema fallará al no encontrar las tablas en MySQL.

```bash
# 1. Entrar a la carpeta del backend
cd backend

# 2. Activar el entorno virtual
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Aplicar las migraciones descargadas
python manage.py migrate
```

#### 💡 Diferencia clave: `makemigrations` vs `migrate`

Es común confundir estos comandos, pero tienen propósitos totalmente distintos:

- **`python manage.py makemigrations`**: 
  - **¿Qué hace?** Analiza tus modelos en `models.py` y **crea el archivo de instrucciones** (el "plano") en la carpeta `migrations/`.
  - **¿Cuándo usarlo?** ÚNICAMENTE cuando **tú** has modificado el código de un modelo y quieres preparar el cambio para la base de datos.
  - **En este flujo:** No se usa al descargar cambios de compañeros porque ellos ya crearon el archivo y tú ya lo descargaste vía Git.

- **`python manage.py migrate`**: 
  - **¿Qué hace?** Lee los archivos de la carpeta `migrations/` y **ejecuta los cambios reales** en la base de datos MySQL.
  - **¿Cuándo usarlo?** Siempre que quieras aplicar cambios, ya sean tuyos (después de un `makemigrations`) o los de tus compañeros (después de un `git pull`).


### 5. Verificación Final
Levantamos el servidor para comprobar que la integración fue exitosa.

```bash
python manage.py runserver
```

---

## ⚡ Resumen Rápido (Cheat Sheet)

| Acción | Comando | Objetivo |
| :--- | :--- | :--- |
| **Sincronizar** | `git fetch origin` | Ver qué hay de nuevo en el servidor. |
| **Fusionar** | `git pull origin main` | Traer los archivos al local. |
| **Migrar** | `python manage.py migrate` | Crear tablas/campos en la BD. |
| **Probar** | `python manage.py runserver` | Verificar funcionamiento. |

---

## 💡 Tips Adicionales
- **Antes del Pull:** Si tienes cambios sin guardar, haz un `git commit` o usa `git stash` para limpiar tu área de trabajo.
- **Dudas con la BD:** Si notas que las tablas no se crearon correctamente, verifica que los archivos en la carpeta `migrations/` de las apps hayan sido descargados efectivamente.

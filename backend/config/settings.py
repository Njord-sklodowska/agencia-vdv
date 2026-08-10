from pathlib import Path
import os
<<<<<<< HEAD
<<<<<<< HEAD
=======
from dotenv import load_dotenv
>>>>>>> origin/feature/frontend-pardinho10
=======
from dotenv import load_dotenv
>>>>>>> origin/feature/frontend-pardinho10

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-demo-key')

DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',') if os.getenv('ALLOWED_HOSTS') else []

INSTALLED_APPS = [
<<<<<<< HEAD
=======
    'sucursal',
    'usuario',
    'clientes',
    'inventario',
    'auditoria',

    'rest_framework',
    'drf_spectacular',
    'corsheaders',
    'parametro_sistema',

>>>>>>> origin/feature/frontend-pardinho10
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'sucursal',
    'usuario',
    'clientes',
    'inventario',
    'ventas',
    'auditoria',
    'rest_framework',
    'corsheaders',
    'parametro_sistema',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication', 
    ),
<<<<<<< HEAD
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
=======
>>>>>>> origin/feature/frontend-pardinho10
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

AUTH_USER_MODEL = 'usuario.Usuario'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-requested-with",
    "x-sucursal-id",
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
<<<<<<< HEAD
<<<<<<< HEAD
        'NAME': 'agencia_vdv',
        'USER': 'root',
        'PASSWORD': '',       
        'HOST': '127.0.0.1',
        'PORT': '3306',
=======
=======
>>>>>>> origin/feature/frontend-pardinho10
        'NAME': os.getenv('DB_NAME', 'agencia_vdv'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'agencia123654'),
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
<<<<<<< HEAD
>>>>>>> origin/feature/frontend-pardinho10
=======
>>>>>>> origin/feature/frontend-pardinho10
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
<<<<<<< HEAD
=======

<<<<<<< HEAD
>>>>>>> origin/feature/frontend-pardinho10
=======
>>>>>>> origin/feature/frontend-pardinho10
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
import os
from pathlib import Path
from decouple import config
import environ
import logging 

# Configuración de rutas
BASE_DIR = Path(__file__).resolve().parent.parent

# Utilizar django-environ para establecer las variables de entorno
env = environ.Env()
environ.Env.read_env(BASE_DIR / '.env')

# Configuraciones de seguridad
SECRET_KEY = env('DJANGO_SECRET_KEY')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = ['*']

# Configuraciones de Stripe y PayPal
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
STRIPE_PUBLISHABLE_KEY = env('STRIPE_PUBLISHABLE_KEY')
PAYPAL_CLIENT_ID = env('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = env('PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = env('PAYPAL_MODE')

# Configuraciones de seguridad adicionales para producción
if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Configuración de registros logs
LOGGING_DIR = BASE_DIR / 'logs'
os.makedirs(LOGGING_DIR, exist_ok=True)

LOGIN_URL = 'login_form'
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR / 'debug.log',
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR / 'errors.log',
        },
        'info_file': {
            'level': 'INFO',    # Puedes ajustar el nivel según tus necesidades (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            'class': 'logging.FileHandler',
            'filename': LOGGING_DIR / 'info.log',
            'formatter': 'verbose',
        },
    },
    'formatters': {
        'verbose': {
            'format': '{asctime} {levelname} {message} ({pathname}:{lineno})',
            'style': '{',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'error_file', 'info_file'], # Agrega 'info_file' aquí
            'level': 'DEBUG',
            'propagate': True,
        },
        'Lucky': {  # Replace 'app_name' with the name of your Django app
            'handlers': ['file', 'error_file', 'info_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


# Configuración de manejo de credenciales y cookies al cerrar sesión

# Asegúrate de tener estas configuraciones
SESSION_COOKIE_AGE = 0  # La sesión se expira inmediatamente cuando el navegador se cierra
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # La sesión se expira cuando el navegador se cierra
# Si quieres que la sesión expire después de un tiempo de inactividad, puedes configurar esto:
SESSION_COOKIE_AGE = 300  # Expira en 5 minutos (300 segundos) de inactividad
SESSION_SAVE_EVERY_REQUEST = True  # Renueva la sesión en cada solicitud




# Configuración de archivos estáticos y de medios
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'staticfiles']
STATIC_ROOT = BASE_DIR / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de aplicaciones instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Lucky',
]

# Configuración de middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'Lucky.middleware.AdminAccessMiddleware',  # Middleware personalizado si lo tienes
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

# Configuración de URLs
ROOT_URLCONF = 'Lucky.urls'

# Configuración de templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Configuración de WSGI
WSGI_APPLICATION = 'Lucky.wsgi.application'

# Configuración de la base de datos
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'LuckyCart.db',
    }
}

# Validadores de contraseñas
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Configuración del modelo de usuario personalizado
AUTH_USER_MODEL = 'Lucky.CustomUser'

# Configuración del modelo personalizado de autenticación en el login con el uso del email y no del username
AUTHENTICATION_BACKENDS: [
    'django.contrib.auth.backends.ModelBackend',  # Keep the default
    'Lucky.backends.EmailBackend',  # Add your custom backend
]




# Configuración de internacionalización
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuración de búsqueda de archivos estáticos
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Configuración del campo de clave primaria por defecto
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

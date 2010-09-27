import os

import utils

DEBUG = True
TEMPLATE_DEBUG = DEBUG

# Mostly used to control things like static file serving options.
DEV_MODE = True

ADMINS = (
)

MANAGERS = ADMINS

# Directory location of the settings file. Useful when needing absolute file
# paths that are in a known location relative to settings.
FILE_ROOT = os.path.abspath(os.path.join(os.path.realpath(
    os.path.dirname(__file__))))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(FILE_ROOT, 'main_db.sqlite'),
    }
}

TIME_ZONE = 'Australia/Sydney'
LANGUAGE_CODE = 'en-us'

# Disabled for now; no i18n support available yet.
USE_I18N = False
USE_L10N = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '-t&^kge1q$s%1wtf7zthorsyrr3_rzn^f_g95eap25iekqiztc'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

ROOT_URLCONF = 'remember_me_urls'

TEMPLATE_DIRS = (
    os.path.join(FILE_ROOT, "templates"),
)

TEMPLATE_CONTEXT_PROCESSORS = (
        "django.contrib.auth.context_processors.auth",
        "django.core.context_processors.debug",
        "django.core.context_processors.media",
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.admindocs',
    'django.contrib.admin',
    'south',
    'minerva',
    'user_management',
    'debug_toolbar',
    'general',
)

LOGIN_REDIRECT_URL = "/"
AUTH_PROFILE_MODULE = "minerva.UserProfile"

DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
}

# Cache period, in seconds, for language data (which hardly ever changes)
LANG_CACHE_TIMEOUT = 10800

utils.load_external_settings("host_settings", globals())


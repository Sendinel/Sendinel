import logging
from datetime import timedelta
from os.path import abspath, dirname

# Django settings for sendinel project.

DEBUG = True        #for scheduling set to false
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = dirname(abspath(__file__))

LOGGING_LEVEL = logging.INFO
LOGGING_LEVEL_TEST = logging.CRITICAL

ADMINS = (
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'           # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = PROJECT_PATH + '/sendinel.db'             # Or path to database file if using sqlite3.
DATABASE_USER = ''             # Not used with sqlite3.
DATABASE_PASSWORD = ''         # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Berlin'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


_ = lambda s: s

#LANGUAGES = (
#  ('de', _('German')),
#  ('en', _('English')),
#  ('ts', _('Shangaan')),
#  ('zh', _('Test Language')),
#)

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = PROJECT_PATH + '/media'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/mediaweb/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin_media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = '4ztf1p=e9d*ns^d*f@bs3mu#37p)$jp(%lzo2a+-%j8^=eq852'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = ("django.core.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.contrib.messages.context_processors.messages")


MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.csrf.middleware.CsrfMiddleware'
)



ROOT_URLCONF = 'sendinel.urls'

TEMPLATE_DIRS = (
    PROJECT_PATH + "/templates",
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'sendinel',
    'sendinel.web',
    'sendinel.backend',
    'sendinel.staff',
)

####################################
# Sendinel Configuration
REMINDER_TIME_BEFORE_APPOINTMENT = timedelta(days = 1)
DEFAULT_APPOINTMENT_DURATION = timedelta(minutes = 60)
DEFAULT_HOSPITAL_NAME = 'your hospital'
DEFAULT_SEND_TIME = '12:00' #hh:mm in 24-hours format

COUNTRY_CODE_PHONE = "0049" #"0027" for South Africa
START_MOBILE_PHONE = "0" # "0" for South Africa (07/08..), "01" for Germany
# see http://en.wikipedia.org/wiki/Telephone_numbers_in_South_Africa
# TODO multiple mobile prefixes

ASTERISK_USER = "root"
ASTERISK_GROUP = "root"
ASTERISK_SPOOL_DIR = "/var/spool/asterisk/outgoing/"
ASTERISK_DATACARD = True

ASTERISK_EXTENSION = "s"
ASTERISK_SIP_ACCOUNT = "datacard0"
#ASTERISK_SIP_ACCOUNT = "ext-sip-account"

FESTIVAL_CACHE = "/lib/init/rw"
#FESTIVAL_CACHE = "/tmp"

# Phonenumber to authenticate against the system
AUTH_NUMBER = "CHANGE ME"
# time a user has to call the system to authenticate
AUTHENTICATION_CALL_TIMEOUT = timedelta(minutes = 3)


# True or False to turn authentication on or off
AUTH = True

# Specify a COM Port for SMS
# for windows maybe it starts at 0
SERIALPORTSMS = '/dev/rfcomm0'

# IP address to bluetooth server
BLUETOOTH_SERVER_ADDRESS = '127.0.0.1'

# used for marking the vcal uid
VCAL_UID_SLUG = 'sendinel.org'
####################################

# Setup Local_Settings if present
try:
    from local_settings import *
except ImportError:
    pass

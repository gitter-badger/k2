# Django settings for k2 project.
import os.path

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        # 'ENGINE': 'django.contrib.gis.db.backends.mysql',
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Warsaw'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'pl'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = False

# Date formats
DATE_FORMAT = 'j N Y'
DATETIME_FORMAT = 'j N Y H:i'

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "static")

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/site_media/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
#SECRET_KEY = 'qs0r*xv(i7#d&5+j3#xestq2eg#1w4v9o-j7@2l%d5ubnigjjf'

# DjangoBB change
if not hasattr(globals(), 'SECRET_KEY'):
    SECRET_FILE = os.path.join(PROJECT_ROOT, 'secret.txt')
    try:
        SECRET_KEY = open(SECRET_FILE).read().strip()
    except IOError:
        try:
            from random import choice
            import string
            symbols = ''.join((string.lowercase, string.digits, string.punctuation ))
            SECRET_KEY = ''.join([choice(symbols) for i in range(50)])
            secret = file(SECRET_FILE, 'w')
            secret.write(SECRET_KEY)
            secret.close()
        except IOError:
            raise Exception('Please create a %s file with random characters to generate your secret key!' % SECRET_FILE)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
# For version => 1.2
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
# For version <= 1.1
#   'django.core.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django_authopenid.context_processors.authopenid',
    'djangobb_forum.context_processors.forum_settings',
    "announcements.context_processors.site_wide_announcements",
    'k2.utils.django.core.context_processors.site',
    'k2.styles.context_processors.styles',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.csrf.CsrfResponseMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_authopenid.middleware.OpenIDMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'k2.stories.middleware.UserPrefMiddleware',
    'k2.utils.django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'k2.utils.django.middleware.html.SpacelessMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'djangobb_forum.middleware.LastLoginMiddleware',
    'djangobb_forum.middleware.UsersOnline',
)

ROOT_URLCONF = 'k2.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_ROOT, "templates"),
)

INSTALLED_APPS = (
    # Django
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.comments',
    'django.contrib.markup',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.flatpages',
    #'django.contrib.gis',
    'django.contrib.humanize',
    # External
    #'gravatar',
    'oembed',
    'tagging',
    'threadedcomments',
    'registration',
    'invitation',
    'django_authopenid',
    'djangobb_forum',
    'haystack',
    'announcements',
    'south',
    'chronograph',
    # Apps
    # @todo: inject templatetags to oembed module
    'k2.utils.django.contrib.flatpages',
    'k2.utils.oembed',
    'k2.utils.voting',
    'k2.utils.google_analytics',
    #'k2.map',
    'k2.profiles',
    'k2.styles',
    'k2.stories',
)

# Threadedcomments
COMMENTS_APP = 'threadedcomments'

# Groups
ADMIN_GROUP_ID = 1
MOD_GROUP_ID = 6
BANNED_GROUP_ID = 7

# Profile
AUTH_PROFILE_MODULE = 'profiles.UserProfile'
AUTH_PREF_MODULE = 'stories.UserPref'
LOGIN_URL = '/logowanie/'
LOGOUT_URL = '/'
LOGIN_REDIRECT_URL = '/'

# E-mail settings
#EMAIL_HOST = 'localhost'
EMAIL_PORT = '587'
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = 0
DEFAULT_FROM_EMAIL = 'noreply@klid.pl'

# Files
FILE_UPLOAD_MAX_MEMORY_SIZE = 1024000

# Cache
CACHE_BACKEND = 'locmem://?timeout=60&max_entries=400'
CACHE_MIDDLEWARE_SECONDS = 60
CACHE_MIDDLEWARE_KEY_PREFIX = 'k2'

# GeoDjango
#GEOS_LIBRARY_PATH="/usr/lib/libgeos_c.so"
#GDAL_LIBRARY_PATH="/usr/lib/libgdal.so"

# Google Maps
GOOGLE_MAPS_KEY='ABQIAAAANRcMfC_cyoA3QdUOo_Hu5hTQAu85EtnTZTzCCgC_HtAMXZ3pxBTahN958SX-8H5LbiYHW6TGxvNEwg'

# Google Analytics
GOOGLE_ANALYTICS_ID='UA-16617701-1'

# Registration
ACCOUNT_ACTIVATION_DAYS=7

# Invitation
INVITE_MODE=False
ACCOUNT_INVITATION_DAYS=7
INVITATIONS_PER_USER=1

# Haystack settings
HAYSTACK_SITECONF = 'search_sites'
HAYSTACK_SEARCH_ENGINE = 'whoosh'
HAYSTACK_WHOOSH_PATH = os.path.join(PROJECT_ROOT, 'djangobb_index')

try:
    execfile(os.path.join(PROJECT_ROOT, 'settings_local.py'))
except:
    pass

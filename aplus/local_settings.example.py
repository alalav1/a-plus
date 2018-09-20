#BASE_URL = 'http://localhost:8000/'
#DEBUG = True
#SECRET_KEY = '' # will be autogenerated in secret_key.py if not specified here
#ADMINS = (
#    ('Your Name', 'your_email@domain.com'),
#)
#SERVER_EMAIL = 'your_email@domain.com'

## Database
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql',
#        'NAME': 'your_db_name',
#        # use ident auth for local servers
#        # and add passwd&hostname etc for remote
#    }
#}

## Caches
#CACHES = {
#    'default': {
#        # prefer memcached with unix socket
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': 'unix:/tmp/memcached.sock',
#
#        # Database cache, if memcached is not possible
#        # remember to run `./manage.py createcachetable`
#        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#        'LOCATION': 'django_cache_default',
#
#        # Local testing with max size
#        'BACKEND': 'lib.cache.LocMemCache',
#        'LOCATION': 'unique-snowflake',
#        'OPTIONS': {'MAX_SIZE': 1000000}, # simulate memcached value limit
#
#        # or dummy
#        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
#    }
#}

## Logging
# For debugging purposes
#from .settings import LOGGING
#LOGGING['loggers'].update({
#    '': {
#        'level': 'INFO',
#        'handlers': ['debug_console'],
#        'propagate': True,
#    },
#    'django.db.backends': {
#        'level': 'DEBUG',
#    },
#})

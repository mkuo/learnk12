from .base import *
try:
    from .local import *
except ImportError:
    pass

DEBUG = False

ALLOWED_HOSTS = ['learnk12.org', 'www.learnk12.org']

DATABASES['default']['PASSWORD'] = DATABASE_PASSWORD

try:
    from .local import *
except ImportError:
    pass

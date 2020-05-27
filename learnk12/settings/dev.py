from .base import *
try:
    from .local import *
except ImportError:
    pass

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SQL statement logging, can be noisy
# LOGGING['handlers']['console'] = {'class': 'logging.StreamHandler'}
# LOGGING['loggers']['django.db.backends'] = {'level': 'DEBUG'}
# LOGGING['root'] = {'handlers': ['console']}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yk*+79g^z#6g5w!o)5)g3c743-+(&k=jh_yn=za3=y5xgt4!xj'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*'] 

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

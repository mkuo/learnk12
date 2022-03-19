from .base import *
try:
    from .local import *
except ImportError:
    pass

# Variables to include in local.py
# DATABASE_PASSWORD
# SECRET_KEY
# SENDGRID_API_KEY

DEBUG = False

ALLOWED_HOSTS = [
    'learnk12.org',
    'www.learnk12.org',
    '64.225.44.184',
]

DATABASES['default']['PASSWORD'] = DATABASE_PASSWORD

# SECURITY SETTINGS
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REFERRER_POLICY = 'same-origin'
SECURE_SSL_REDIRECT = True

# EMAIL
LOGGING['loggers']['django']['handlers'].append('mail_admins')
LOGGING['handlers']['mail_admins'] = {
    'level': 'ERROR',
    'class': 'django.utils.log.AdminEmailHandler',
}
DEFAULT_FROM_EMAIL = 'info@learnk12.org'
SERVER_EMAIL = 'info@learnk12.org'

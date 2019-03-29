"""
    settings for develop environment
"""

from .base import *


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Send email to stdout
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

"""
    settings for develop environment
"""

from .base import *

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DEBUG = True

DATABASES = {
    # By default it is run as docker image
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'HOST': 'db',
        'PORT': 5432,
    }
}

# Send email to stdout
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

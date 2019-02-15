from .base import *
from .local_secret import *

DEBUG = False

ALLOWED_HOSTS = ['www.ta2milab.com']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = '/usr/share/nginx/html/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/usr/share/nginx/html/media'

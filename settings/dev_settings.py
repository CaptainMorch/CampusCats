# The entrypoint of project settings.
# 
# Set your settings here INSTEAD of in the stock file.
# See https://github.com/CaptainMorch/CampusCats/blob/main/doc/deploy.md#%E4%B8%8B%E8%BD%BD%E5%B9%B6%E8%AE%BE%E7%BD%AE%E9%A1%B9%E7%9B%AE


# Import django stock settings.
import sys
PRJ_DIR = '/path/to/your/directory/holding/manage.py'
sys.path.append(PRJ_DIR)

from campuscats.settings import *


# Overwrite django default settings below.

SECRET_KEY = 'this_is_a_key_for_local_test'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.dummy',
    }
}

DEBUG = True
ALLOWED_HOSTS = ['localhost', '0.0.0.0', '127.0.0.1']


# Overwrite project settings, or add your own below:
SITE_NAME = '测试'

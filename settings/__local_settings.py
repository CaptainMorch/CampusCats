# The entrypoint of project settings.
# 
# Set your settings here INSTEAD of in the stock file.
# See https://github.com/CaptainMorch/CampusCats/blob/main/docs/deploy.md#%E4%B8%8B%E8%BD%BD%E5%B9%B6%E8%AE%BE%E7%BD%AE%E9%A1%B9%E7%9B%AE


# Import django stock settings.
import sys
PRJ_DIR = '/home/app/web'
sys.path.append(PRJ_DIR)

from campuscats.settings import *


# Overwrite django default settings below.

import os

with open('/run/secrets/site_secret_key') as key, \
        open('/run/secrets/mysql_password') as pwd:
    SECRET_KEY = key.read().strip()
    DATABASE_PASSWORD = pwd.read().strip()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'mysql',
        'PORT': 3306,
        'NAME': 'campuscats',    # you should also edit ./docker-compose.yaml
        'USER': 'app',           # if you need to edit these two arguments
        'PASSWORD': DATABASE_PASSWORD
    }
}

DEBUG = False    # DO NOT TURN ON IN PRODUCTION
ALLOWED_HOSTS = ['example.com']    # YOU MUST EDIT THIS IN PRODUCTION


# Overwrite project settings, or add your own below:
SITE_NAME = '网站名称'

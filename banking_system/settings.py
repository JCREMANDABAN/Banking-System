import os
import pymysql
pymysql.install_as_MySQLdb()
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'your-secret-key-change-in-production'
DEBUG = True
ALLOWED_HOSTS = []
INSTALLED_APPS = [
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.messages',
         'django.contrib.staticfiles',
         'banking_app',
     ]
MIDDLEWARE = [
         'django.middleware.security.SecurityMiddleware',
         'django.contrib.sessions.middleware.SessionMiddleware',
         'django.middleware.common.CommonMiddleware',
         'django.middleware.csrf.CsrfViewMiddleware',
         'django.contrib.auth.middleware.AuthenticationMiddleware',
         'django.contrib.messages.middleware.MessageMiddleware',
         'django.middleware.clickjacking.XFrameOptionsMiddleware',
     ]
ROOT_URLCONF = 'banking_system.urls'

TEMPLATES = [
         {
             'BACKEND': 'django.template.backends.django.DjangoTemplates',
             'DIRS': [os.path.join(BASE_DIR, 'templates')],
             'APP_DIRS': True,
             'OPTIONS': {
                 'context_processors': [
                     'django.template.context_processors.debug',
                     'django.template.context_processors.request',
                     'django.contrib.auth.context_processors.auth',
                     'django.contrib.messages.context_processors.messages',
                 ],
             },
         },
     ]

DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.mysql',
             'NAME': 'banking_system',
             'USER': 'root',
             'PASSWORD': '',  # Empty for default XAMPP
             'HOST': '127.0.0.1',
             'PORT': '3306',
         }
     }
AUTH_PASSWORD_VALIDATORS = [
         {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
         {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
         {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
         {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
     ]
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
     # Email/SMS settings
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'
SENDGRID_API_KEY = 'your-sendgrid-api-key'
TWILIO_ACCOUNT_SID = 'your-twilio-sid'
TWILIO_AUTH_TOKEN = 'your-twilio-token'
TWILIO_PHONE_NUMBER = '+1234567890'

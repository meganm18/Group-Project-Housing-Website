"""
Django settings for housing_project project.

Generated by 'django-admin startproject' using Django 1.11.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see 
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import django_heroku

import dj_database_url

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/




ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'housing_app',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'housing_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'housing_project.wsgi.application'


AUTHENTICATION_BACKENDS = (
     'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.google.GooglePlusAuth',
)
#SOCIAL_AUTH_USER_MODEL = 'housing_app.User'

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'



SOCIAL_AUTH_URL_NAMESPACE = 'social'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY ='535339961837-l9ngaeh17ug9v113taq3mi53sddh21bl.apps.googleusercontent.com'  
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'dpN6_6aOyOXk1Zn831u9zPHt' 

# SOCIAL_AUTH_GOOGLE_PLUS_KEY = '535339961837-r6tcfcts3n2vt4gmqlkfnbo4jvomkulq.apps.googleusercontent.com'
# SOCIAL_AUTH_GOOGLE_PLUS_SECRET = '5qaHv1fV7jf0xUBO0Vkbjt17'

# SOCIAL_AUTH_GOOGLE_PLUS_AUTH_EXTRA_ARGUMENTS = {
#       'access_type': 'offline'
# }

#SOCIAL_AUTH_ADMIN_USER_SEARCH_FIELDS = ['username', 'first_name', 'email']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'housing_app.pipeline.get_avatar'
)

SOCIAL_AUTH_DISCONNECT_REDIRECT_URL = 'apartments'


SOCIAL_AUTH_DISCONNECT_PIPELINE = (
    'social_core.pipeline.disconnect.get_entries',
    'social_core.pipeline.disconnect.revoke_tokens',
    'social_core.pipeline.disconnect.disconnect'
)

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'nb-ca=7ye7+1czyslwf88k4b!cdnk4&tn%(p)yu=eg_v2sb#tm'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

#Use the following live settings to build on Travis CI
# if os.getenv('BUILD_ON_TRAVIS', None):
#     SECRET_KEY = "vXd06OqF+f6vybaiGljYpTqnD0Xl6Yjs4mlO7SwcAOVKzPtJ9A3nx5jBF2RZyNq+E0Nk4e1Wioh5cl2x3jv1UQ2sCmyDEqY6n4s54sc0J2CQGnEI1hnuE9V90kCzptRzI+hmNHljUFxwMraQqZZFho5i/mOtLu3u6XrTajhyP4fLiwwLGUGBWUwI7Xia6AHVgEAba1Y5h7HVw49hnejL/vEu4uLY7c+2XKQfz170mwNi9Gs5MdZ54+olKVWUWRD/AuLixISIrljfsWva1gmwpcAFy4rGz639CJ2FheUV7Ruc7yLybJ+AEKdH6t5HUStjhHvLht+8UjomdpdlX5VyjcasKXLeOkgpIw0ToyAZtAx54mV+H2a0BYWcjzYevlwFFqJe3+7OZvyJpfqRTEpCXmYXV0I0pL6CAVF5dqMhaiO0AFOLjjyJoyYl4xeZwmczS8/plW2SxF9t4nvVR1YlqwFtdyRkj88e/swoT3faXT+7Jqh8D0HDdXdOql7oBtgPP3wgMksvK02Ewfr32aZZFNGHzJHKCbarp+GqWci8zU08QAysk4u9hlqqOhm828b4zcyttt6OkC3bEMkCtnz3XYAOyhp1MDkG63yRvO+OJg6YPuO8GNfY9SJc4hiMqoTQCPFNh7ir0iV7p1OhJdojopsU+DEOqYTIXwS/1VFgweY="
#     DEBUG = False
#     TEMPLATE_DEBUG = True

#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': 'travis_ci_db',
#             'USER': 'travis',
#             'PASSWORD': '',
#             'HOST': '127.0.0.1',
#         }
#     }
# else:

if os.getenv('BUILD_ON_TRAVIS', None):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'travis_ci_db',
            'USER': 'postgres',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': os.getenv('PGPORT'),
        }
    }
else: 
    DATABASES = {
        'default': {
        #     'ENGINE': 'django.db.backends.sqlite3',
        #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'apartment_database',
        'USER': 'miracle_worker',
        'PASSWORD': 'miracleworkers',
        'HOST': 'localhost',
        'PORT': '5432',
        }
    }
    DATABASES['default'] = dj_database_url.config(default='postgres://usdczwzpqgyqbb:c1f02655a959155db474e6057b713e113a3ba63efbbee6e61e183759f251ab62@ec2-107-20-185-27.compute-1.amazonaws.com:5432/da8eubmr4a4ge9')


# Password validations
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# Activate Django-Heroku.
django_heroku.settings(locals())




"""
Django settings for embeddia project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from corsheaders.defaults import default_headers
from utils import parse_list_env_headers
import os


from embeddia.analyzers.analyzers import (
    HSDAnalyzer,
    KWEAnalyzer,
    HybridTaggerAnalyzer,
    MultiTagAnalyzer
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# EMBEDDIA SERVICE HOSTNAMES & OTHER PARAMS
HSD_HOST = os.getenv("EMBEDDIA_HSD_HOST", "http://localhost:5001")
KWE_HOST = os.getenv("EMBEDDIA_KWE_HOST", "http://localhost:5003")
NLG_HOST = os.getenv("EMBEDDIA_NLG_HOST", "http://localhost:5002")

TEXTA_HOST = os.getenv("EMBEDDIA_TEXTA_HOST", "http://dev.texta.ee:8000")
TEXTA_TOKEN = os.getenv("EMBEDDIA_TEXTA_TOKEN", "d44736b2d645eaeb8979b9aaff85c00ce90cd86b")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd064bgxe^08n5@ubx80azgo7paxzj&!p251(nzoxa6q%v_*ny4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'embeddia'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

ROOT_URLCONF = 'embeddia_toolkit.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'embeddia_toolkit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


# For corsheaders/external frontend
CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_NAME = "XSRF-TOKEN"
# For accessing a live backend server locally.
CORS_ORIGIN_WHITELIST = parse_list_env_headers("TEXTA_CORS_ORIGIN_WHITELIST", ["http://localhost:4200"])
CORS_ALLOW_HEADERS = list(default_headers) + ["x-xsrf-token"]



EMBEDDIA_ANALYZERS = {
    "KeywordExtractor": KWEAnalyzer(host=KWE_HOST),
    "BERTHatespeech": HSDAnalyzer(host=HSD_HOST),
    "HybridTagger": HybridTaggerAnalyzer(host=TEXTA_HOST, auth_token=TEXTA_TOKEN, project=1, tagger_group=5, use_ner=True, lemmatize=True),
    "HatespeechTagger": MultiTagAnalyzer(host=TEXTA_HOST, auth_token=TEXTA_TOKEN, project=2, lemmatize=True)
}

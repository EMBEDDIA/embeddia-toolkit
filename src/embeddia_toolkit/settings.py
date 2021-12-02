"""
Django settings for embeddia project.

Generated by 'django-admin startproject' using Django 2.1.15.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
from corsheaders.defaults import default_headers
from kombu import Exchange, Queue
#from utils import parse_list_env_headers
import os

from texta_mlp.mlp import MLP

from embeddia_toolkit.embeddia.analyzers.article_analyzer import (
    KWEAnalyzer,
    HybridTaggerAnalyzer,
    NERAnalyzer
)
from embeddia_toolkit.embeddia.analyzers.comment_analyzer import (
    QMULAnalyzer,
    MultiTagAnalyzer,
    BERTTaggerAnalyzer
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# data dir is located next to base dir
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")


# EMBEDDIA SERVICE HOSTNAMES & OTHER PARAMS
NLG_HOST = os.getenv("EMBEDDIA_NLG_HOST", "http://localhost:5000")

HSD_1_HOST = os.getenv("EMBEDDIA_HSD_HOST", "http://localhost:5001")
HSD_2_HOST = os.getenv("EMBEDDIA_HSD_MBERT_HOST", "http://localhost:5001")
HSD_3_HOST = os.getenv("EMBEDDIA_HSD_MBERT_ENEE_HOST", "http://localhost:5001")
HSD_4_HOST = os.getenv("EMBEDDIA_HSD_CSE_HOST", "http://localhost:5001")

KWE_ET_HOST = os.getenv("EMBEDDIA_KWE_ET_HOST", "http://localhost:5002")
KWE_HR_HOST = os.getenv("EMBEDDIA_KWE_HR_HOST", "http://localhost:5003")
KWE_LV_HOST = os.getenv("EMBEDDIA_KWE_LV_HOST", "http://localhost:5004")
KWE_EN_HOST = os.getenv("EMBEDDIA_KWE_EN_HOST", "http://localhost:5007")
KWE_RAKUN_HOST = os.getenv("EMBEDDIA_KWE_RAKUN_HOST", "http://localhost:5005")
NER_HOST = os.getenv("EMBEDDIA_NER_HOST", "http://localhost:5006")

TEXTA_HOST = os.getenv("EMBEDDIA_TEXTA_HOST", "https://rest-dev.texta.ee")
TEXTA_TOKEN = os.getenv("EMBEDDIA_TEXTA_TOKEN", "")

TEXTA_HT_PROJECT = int(os.getenv("EMBEDDIA_TEXTA_HT_PROJECT", 1))
TEXTA_HT_TAGGER = int(os.getenv("EMBEDDIA_TEXTA_HT_TAGGER", 5))
TEXTA_HS_PROJECT = int(os.getenv("EMBEDDIA_TEXTA_HS_PROJECT", 2))
TEXTA_BERT_PROJECT = int(os.getenv("EMBEDDIA_TEXTA_BERT_PROJECT", 310))
TEXTA_BERT_TAGGER = int(os.getenv("EMBEDDIA_TEXTA_BERT_TAGGER", 310))

REQUEST_THROTTLE = os.getenv("EMBEDDIA_REQUEST_THROTTLE", "100/day")

# SSL verification
SSL_VERIFY = True if os.getenv("EMBEDDIA_TEXTA_SSL_VERIFY", "True") == "True" else False

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd064bgxe^08n5@ubx80azgo7paxzj&!p251(nzoxa6q%v_*ny4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


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
    'embeddia_toolkit.embeddia'
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': REQUEST_THROTTLE
    }
}

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
        'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
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

# CELERY OPTIONS
BROKER_URL = os.getenv("EMBEDDIA_REDIS_URL", "redis://localhost:6379/1")
CELERY_RESULT_BACKEND = BROKER_URL
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_ALWAYS_EAGER = False if os.getenv("DOCPARSER_CELERY_ALWAYS_EAGER", "false").lower() == "false" else True
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_QUEUE = "embeddia_queue"
CELERY_QUEUES = (
    Queue(CELERY_TASK_QUEUE, exchange=CELERY_TASK_QUEUE, routing_key=CELERY_TASK_QUEUE),
)
CELERY_DEFAULT_QUEUE = CELERY_TASK_QUEUE
CELERY_DEFAULT_EXCHANGE = CELERY_TASK_QUEUE
CELERY_DEFAULT_ROUTING_KEY = CELERY_TASK_QUEUE

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")


# For corsheaders/external frontend
CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_NAME = "XSRF-TOKEN"
# For accessing a live backend server locally.
#CORS_ORIGIN_WHITELIST = parse_list_env_headers("TEXTA_CORS_ORIGIN_WHITELIST", ["http://localhost:4200"])
CORS_ALLOW_HEADERS = list(default_headers) + ["x-xsrf-token"]

# set MLP languages
MLP_LANGS = os.getenv("EMBEDDIA_MLP_LANGS", "et,en,ru").split(",")

MLP_NAME = "Named Entity Extractor - TEXTA MLP (Multilingual)"

# DECLARE EMBEDDIA ANALYZERS
ARTICLE_ANALYZERS = {
    "Keyword Extractor - TNT-KID (Estonian)": KWEAnalyzer(host=KWE_ET_HOST, ssl_verify=SSL_VERIFY),
    "Keyword Extractor - TNT-KID (Croatian)": KWEAnalyzer(host=KWE_HR_HOST, ssl_verify=SSL_VERIFY),
    "Keyword Extractor - TNT-KID (Latvian)": KWEAnalyzer(host=KWE_LV_HOST, ssl_verify=SSL_VERIFY),
    "Keyword Extractor - TNT-KID (English)": KWEAnalyzer(host=KWE_EN_HOST, ssl_verify=SSL_VERIFY),
    "Keyword Extractor - RaKUn (Multilingual)": KWEAnalyzer(host=KWE_RAKUN_HOST, ssl_verify=SSL_VERIFY),
    "Named Entity Extractor - BiLSTM (Croatian)": NERAnalyzer(host=NER_HOST, ssl_verify=SSL_VERIFY, language="hr"),
    "Named Entity Extractor - BiLSTM (Estonian)": NERAnalyzer(host=NER_HOST, ssl_verify=SSL_VERIFY, language="et"),
    "Named Entity Extractor - BiLSTM (Slovenian)": NERAnalyzer(host=NER_HOST, ssl_verify=SSL_VERIFY, language="sl"),
    "Named Entity Extractor - BiLSTM (Russian)": NERAnalyzer(host=NER_HOST, ssl_verify=SSL_VERIFY, language="ru"),
    MLP_NAME: MLP(language_codes=MLP_LANGS, resource_dir=DATA_DIR)
}

COMMENT_ANALYZERS = {
    "Comment Moderator BERT (Cross-lingual)": QMULAnalyzer(host=HSD_1_HOST, ssl_verify=SSL_VERIFY),
    "Comment Moderator MBERT (Cross-lingual)": QMULAnalyzer(host=HSD_2_HOST, ssl_verify=SSL_VERIFY),
    "Comment Moderator MBERT (English & Estonian)": QMULAnalyzer(host=HSD_3_HOST, ssl_verify=SSL_VERIFY),
    "Comment Moderator CSEBERT (English, Slovenian & Croatian)": QMULAnalyzer(host=HSD_4_HOST, ssl_verify=SSL_VERIFY),
    "Comment Moderator BERT (Estonian)": BERTTaggerAnalyzer(host=TEXTA_HOST, auth_token=TEXTA_TOKEN, project=TEXTA_BERT_PROJECT, tagger=TEXTA_BERT_TAGGER, ssl_verify=SSL_VERIFY)
}

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
from texta_mlp.mlp import MLP
import os

from embeddia.analyzers.article_analyzer import (
    KWEAnalyzer,
    HybridTaggerAnalyzer,
    NERAnalyzer,
    ArticleAnalyzer
)
from embeddia.analyzers.comment_analyzer import (
    QMULAnalyzer,
    MultiTagAnalyzer,
    CommentAnalyzer
)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# data dir is located next to base dir
DATA_DIR = os.path.join(os.path.dirname(BASE_DIR), "data")


# EMBEDDIA SERVICE HOSTNAMES & OTHER PARAMS
NLG_HOST = os.getenv("EMBEDDIA_NLG_HOST", "http://localhost:5000")
HSD_HOST = os.getenv("EMBEDDIA_HSD_HOST", "http://localhost:5001")
KWE_ET_HOST = os.getenv("EMBEDDIA_KWE_ET_HOST", "http://localhost:5002")
KWE_HR_HOST = os.getenv("EMBEDDIA_KWE_HR_HOST", "http://localhost:5003")
NER_HOST = os.getenv("EMBEDDIA_NER_HOST", "http://localhost:5004")

TEXTA_HOST = os.getenv("EMBEDDIA_TEXTA_HOST", "https://rest-dev.texta.ee")
TEXTA_TOKEN = os.getenv("EMBEDDIA_TEXTA_TOKEN", "d44736b2d645eaeb8979b9aaff85c00ce90cd86b")

TEXTA_HT_PROJECT = int(os.getenv("EMBEDDIA_TEXTA_HT_PROJECT", 1))
TEXTA_HT_TAGGER = int(os.getenv("EMBEDDIA_TEXTA_HT_TAGGER", 5))
TEXTA_HS_PROJECT = int(os.getenv("EMBEDDIA_TEXTA_HS_PROJECT", 2))

# SSL verification
SSL_VERIFY = bool(os.getenv("EMBEDDIA_TEXTA_SSL_VERIFY", False))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd064bgxe^08n5@ubx80azgo7paxzj&!p251(nzoxa6q%v_*ny4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static")


# For corsheaders/external frontend
CSRF_HEADER_NAME = "HTTP_X_XSRF_TOKEN"
CSRF_COOKIE_NAME = "XSRF-TOKEN"
# For accessing a live backend server locally.
CORS_ORIGIN_WHITELIST = parse_list_env_headers("TEXTA_CORS_ORIGIN_WHITELIST", ["http://localhost:4200"])
CORS_ALLOW_HEADERS = list(default_headers) + ["x-xsrf-token"]

# DECLARE EMBEDDIA ANALYZERS & GENERATORS
MLP_LANGS = os.getenv("EMBEDDIA_MLP_LANGS", "et,en,ru").split(",")

mlp_analyzer = MLP(language_codes=MLP_LANGS, resource_dir=DATA_DIR)
#ner_analyzer = NERAnalyzer(host=NER_HOST, ssl_verify=SSL_VERIFY)
kwe_et_analyzer = KWEAnalyzer(host=KWE_ET_HOST, ssl_verify=SSL_VERIFY)
kwe_hr_analyzer = KWEAnalyzer(host=KWE_HR_HOST, ssl_verify=SSL_VERIFY)
hybrid_tagger_analyzer = HybridTaggerAnalyzer(
    host=TEXTA_HOST,
    auth_token=TEXTA_TOKEN,
    project=TEXTA_HT_PROJECT,
    tagger_group=TEXTA_HT_TAGGER,
    use_ner=True,
    lemmatize=False,
    ssl_verify=SSL_VERIFY
)
qmul_analyzer = QMULAnalyzer(host=HSD_HOST, ssl_verify=SSL_VERIFY)
mtag_analyzer = MultiTagAnalyzer(host=TEXTA_HOST, auth_token=TEXTA_TOKEN, project=TEXTA_HS_PROJECT, lemmatize=True, ssl_verify=SSL_VERIFY)


EMBEDDIA_ARTICLE_ANALYZER = ArticleAnalyzer(
    mlp_analyzer,
    {
        "Hybrid Tagger Analyzer": hybrid_tagger_analyzer,
        "TNT-KID ET Analyzer": kwe_et_analyzer,
        "TNT-KID HR Analyzer": kwe_hr_analyzer
    }
)
EMBEDDIA_COMMENT_ANALYZER = CommentAnalyzer(
    {
        "EMBEDDIA Cross-lingual Comment Model": qmul_analyzer,
        "Monolingual Comment Model": mtag_analyzer
    }
)

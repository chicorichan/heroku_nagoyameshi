
"""
Django settings for myproject project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6=-z^47-j(htc()ir7x%_*6%@d&a8o4r%!_yifkkzd(q-hp=d^'

# SECURITY WARNING: don't run with debug turned on in production!
# 開発中は DEBUG=True とする
# デプロイをする時、DEBUG=False
DEBUG = False

# DEBUG = True の場合。ページにエラーメッセージが表示される。
# DEBUG = False の場合。エラーメッセージは表示されない(エラーメッセージが部外者に確認できると、セキュリティ上問題あり。)


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "nagoyameshi",
    "accounts",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

#↓↓↓↓↓追記↓↓↓↓↓
#DEBUGがTrueのとき、メールの内容は全て端末に表示させる
if DEBUG:
    EMAIL_BACKEND   = "django.core.mail.backends.console.EmailBackend"
else:
    EMAIL_BACKEND   = "django.core.mail.backends.console.EmailBackend"
    """
    # Sendgridというメール送信サービスを使う。
    EMAIL_BACKEND       = "sendgrid_backend.SendgridBackend"
    DEFAULT_FROM_EMAIL  = "example@example.com" # Sendgrid送信用のメールアドレス。
    SENDGRID_API_KEY    = "ここにsendgridのAPIkeyを記述する" # 環境変数でも可
    SENDGRID_SANDBOX_MODE_IN_DEBUG = False
    """

# ログイン・ログアウトのリダイレクト先。
LOGIN_REDIRECT_URL  = "/"
LOGOUT_REDIRECT_URL = "login" # urls.pyのnameを参照している。

# 使用するユーザーモデルの指定。accounts/models.py の CustomUserモデルを使う。
AUTH_USER_MODEL = 'accounts.CustomUser'
# 会員登録時のバリデーション用のフォーム。新規作成用のフォームを用意する。
ACCOUNT_FORMS   = { "signup":"accounts.forms.SignupForm"}

#↑↑↑↑↑追記↑↑↑↑↑

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

#↓追加
if DEBUG:
    STATICFILES_DIRS = [ BASE_DIR / "static" ]

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 画像関連の設定
# MEDIA_URLは配信先のURL
MEDIA_URL = '/media/'   #←極端に言うと何でもよい
# MEDIA_ROOTは保存先の場所
MEDIA_ROOT = BASE_DIR / 'media'

#Stripe
"""
from .local_settings import *
"""


# APIキーは、環境変数を使って呼び出す。
import os

if "STRIPE_PUBLISHABLE_KEY" in os.environ and "STRIPE_API_KEY" in os.environ and "STRIPE_PRICE_ID" in os.environ:
    STRIPE_PUBLISHABLE_KEY  = os.environ["STRIPE_PUBLISHABLE_KEY"]
    STRIPE_API_KEY          = os.environ["STRIPE_API_KEY"]
    STRIPE_PRICE_ID         = os.environ["STRIPE_PRICE_ID"]


# Herokuデプロイ仕様の設定
if not DEBUG:

    #INSTALLED_APPSにcloudinaryの追加
    INSTALLED_APPS.append('cloudinary')
    INSTALLED_APPS.append('cloudinary_storage')

    # ALLOWED_HOSTSにホスト名)を入力
    ALLOWED_HOSTS = [ os.environ["HOST"] ]

    SECRET_KEY = os.environ["SECRETKEY"]
    
    # 静的ファイル配信ミドルウェア、whitenoiseを使用。※ 順番不一致だと動かない
    MIDDLEWARE = [ 
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        ]

    # 静的ファイル(static)の存在場所を指定する。
    STATIC_ROOT = BASE_DIR / 'static'

    # DBの設定
    DATABASES = { 
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME'    : os.environ["DB_NAME"],
                'USER'    : os.environ["DB_USER"],
                'PASSWORD': os.environ["DB_PASSWORD"],
                'HOST'    : os.environ["DB_HOST"],
                'PORT': '5432',
                }
            }
    

    #DBのアクセス設定
    import dj_database_url

    db_from_env = dj_database_url.config(conn_max_age=600, ssl_require=True)
    DATABASES['default'].update(db_from_env)

    #cloudinaryの設定
    CLOUDINARY_STORAGE = { 
            'CLOUD_NAME': os.environ["CLOUD_NAME"], 
            'API_KEY'   : os.environ["API_KEY"], 
            'API_SECRET': os.environ["API_SECRET"],
            "SECURE"    : True,
            }

    #これで全てのファイルがアップロード可能(上限20MB。ビュー側でアップロードファイル制限するなら基本これでいい)
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.RawMediaCloudinaryStorage'

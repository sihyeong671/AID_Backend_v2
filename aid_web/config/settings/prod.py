# flake8: noqa
from .base import *  # noqa

# TODO: production용 allowed host 설정
# ALLOWED_HOSTS = []

DEBUG = False
SESSION_COOKIE_SECURE = True

dotenv_path = BASE_DIR / ".prod.env"
DATABASES = set_db(dotenv_path)

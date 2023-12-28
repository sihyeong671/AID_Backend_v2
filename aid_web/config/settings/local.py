# flake8: noqa
from .base import *  # noqa

ALLOWED_HOSTS = []

dotenv_path = BASE_DIR / ".local.env"
DATABASES = set_db(dotenv_path)

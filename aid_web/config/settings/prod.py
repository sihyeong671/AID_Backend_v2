# flake8: noqa
from .base import *  # noqa

# ALLOWED_HOSTS = []

DEBUG = False

dotenv_path = BASE_DIR / ".prod.env"
DATABASES = set_db(dotenv_path)

from .base import BASE_DIR, set_db

# ALLOWED_HOSTS = []

DEBUG = False

dotenv_path = BASE_DIR / ".prod.env"
DATABASES = set_db(dotenv_path)

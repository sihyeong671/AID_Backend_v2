# flake8: noqa
from .base import *  # noqa

# TODO: production용 allowed host 설정
# TODO: user uploaded media file. https://docs.djangoproject.com/en/4.1/topics/security/#user-uploaded-content
ALLOWED_HOSTS = []

DEBUG = False
SESSION_COOKIE_SECURE = True

dotenv_path = BASE_DIR / ".prod.env"
DATABASES = set_db(dotenv_path)

# https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/#s3-bucket
AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
AWS_SECRET_ACCESS_KEY = os.environ["AWS_SECRET_ACCESS_KEY"]
AWS_STORAGE_BUCKET_NAME = os.environ["AWS_STORAGE_BUCKET_NAME"]
AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
# s3 static settings
STATIC_LOCATION = "static"
STATIC_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/"
STATICFILES_STORAGE = "config.storage_backends.StaticStorage"
# s3 public media settings
PUBLIC_MEDIA_LOCATION = "media"
MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/"
DEFAULT_FILE_STORAGE = "config.storage_backends.PublicMediaStorage"

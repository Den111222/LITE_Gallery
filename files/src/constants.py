import os

ENV = os.environ.get("ENV", "dev")
APP_VERSION = "1.0.0"
APP_PREFIX = "FILES API"
APP_NAME = "FILES API"
APP_DESCRIPTION = "API для файлов"
APP_API_DOCS_TITLE = f"{APP_NAME} ({ENV.upper()})" if ENV != "dev" else APP_NAME

DEFAULT_ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

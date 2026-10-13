import os
import string

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

DEFAULT_CATEGORY_ID = -1
DEFAULT_CATEGORY_NAME = "Miscellaneous"
ALLOWED_PASSWORD_CHARACTERS = string.ascii_letters + string.digits + string.punctuation

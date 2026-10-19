import os
import string

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")
SESSION_TTL_SECONDS=6_04_800

DEFAULT_CATEGORY_ID = -1
DEFAULT_CATEGORY_NAME = "Miscellaneous"
OWED_TO_ME_CATEGORY_ID = -2
OWED_TO_ME_CATEGORY_NAME = "Owed to me"
I_OWE_CATEGORY_ID = -3
I_OWE_CATEGORY_NAME = "I owe"
ALLOWED_PASSWORD_CHARACTERS = string.ascii_letters + string.digits + string.punctuation

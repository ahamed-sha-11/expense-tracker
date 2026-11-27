import os
import string
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.environ["DATABASE_URL"]
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/1")
FRONTEND_ORIGINS = os.getenv("FRONTEND_ORIGINS", "http://localhost:5173").split(",")
SESSION_TTL_SECONDS=6_04_800

DEFAULT_CATEGORY_ID = -1
DEFAULT_CATEGORY_NAME = "Miscellaneous"
OWED_TO_ME_CATEGORY_ID = -2
OWED_TO_ME_CATEGORY_NAME = "Owed to me"
I_OWE_CATEGORY_ID = -3
I_OWE_CATEGORY_NAME = "I owe"
ALLOWED_PASSWORD_CHARACTERS = string.ascii_letters + string.digits + string.punctuation

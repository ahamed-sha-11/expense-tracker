from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite:///./test.db"


class Base(DeclarativeBase):
    pass

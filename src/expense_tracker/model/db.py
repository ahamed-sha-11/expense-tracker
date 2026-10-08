from sqlalchemy import Column, Integer
from sqlalchemy.orm import DeclarativeBase

DATABASE_URL = "sqlite+aiosqlite:///./test.db"


class Base(DeclarativeBase):
    pass

class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    
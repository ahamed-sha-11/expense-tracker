from sqlalchemy import Column, Integer, String

from expense_tracker.core.database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = {"sqlite_autoincrement": True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)

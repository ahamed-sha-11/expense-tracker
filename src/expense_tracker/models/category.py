from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint

from expense_tracker.core.database import Base


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("user_id", "name", name="uq_category_user_name"),
        {"sqlite_autoincrement": True},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    @property
    def is_default(self) -> bool:
        return self.user_id is None
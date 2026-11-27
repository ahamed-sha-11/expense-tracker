
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
    UniqueConstraint,
)

from expense_tracker.core.database import Base


class LLMCredentials(Base):
    __tablename__ = "llm_credentials"
    __table_args__ = (
        UniqueConstraint("user_id"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=True,
        unique=True,
    )

    encrypted_api_key = Column(LargeBinary, nullable=False)
    nonce = Column(LargeBinary, nullable=False)
    key_version = Column(Integer, nullable=False, default=1)

    model = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)

    @property
    def is_default(self) -> bool:
        return self.user_id is None
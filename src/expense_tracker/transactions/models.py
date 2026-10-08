from sqlalchemy.orm import Mapped, mapped_column

from ..db import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)

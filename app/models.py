from __future__ import annotations
from datetime import datetime
from advanced_alchemy.base import UUIDBase
from sqlalchemy import BigInteger, String, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

class User(UUIDBase):
  __tablename__ = "user"

  id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String, nullable=False)
  surname: Mapped[str] = mapped_column(String, nullable=False)
  password: Mapped[str] = mapped_column(String, nullable=False)
  created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
  updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())

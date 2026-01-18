# app/models/user.py
from __future__ import annotations

from sqlalchemy import String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.base import Base


class User(Base):
    __tablename__ = "user"
    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
    )

    user_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    uploads: Mapped[list["UploadedBy"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    history_entries: Mapped[list["History"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


from backend.app.models.uploaded_by import UploadedBy  # noqa: E402
from backend.app.models.history import History  # noqa: E402

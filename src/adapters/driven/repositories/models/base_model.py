from datetime import datetime
from typing import Type, TypeVar, Generic
from sqlalchemy import Column, DateTime, Integer, text, func
from sqlalchemy.orm import DeclarativeBase, Mapped

from src.core.domain.entities.base_entity import T

M = TypeVar("M", bound="BaseModel")

class BaseModel(DeclarativeBase, Generic[M]):

    __abstract__ = True

    # Primary Key: Auto-incrementing integer ID
    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)

    # Timestamp: Record creation time (default: current UTC time)
    created_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )

    # Timestamp: Record last update time (auto-updated on modification)
    updated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=func.now(), nullable=False
    )

    # Timestamp: Record inactivation time
    inactivated_at: Mapped[datetime] = Column(
        DateTime(timezone=True), nullable=True
    )

__all__ = ["BaseModel"]

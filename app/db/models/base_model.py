#!/usr/bin/python3
"""Base Model module"""

from sqlmodel import SQLModel, Field
from uuid import UUID, uuid4
from datetime import datetime, UTC
from sqlalchemy import Column, DateTime

def utcnow():
    """Return a timezone-aware UTC datetime."""
    return datetime.now(UTC)

class BaseModel(SQLModel):
    """Base model with UUID primary key and timestamp fields."""

    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)
    created_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=utcnow)
    )
    updated_at: datetime = Field(
        sa_column=Column(DateTime(timezone=True), nullable=False, default=utcnow, onupdate=utcnow)
    )

"""
Base model class with common fields and methods.
"""

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.db.base import Base


class BaseModel(Base):
    """
    Base model class with common fields.
    
    Attributes:
        id: Primary key
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) 
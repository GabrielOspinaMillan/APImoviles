from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.sql import func
from database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now())

    @property
    def updatedAt(self):
        """Provide camelCase attribute for Pydantic `updatedAt` field (ORM response)."""
        return self.updated_at

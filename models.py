from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class Document(Base):
    """Represents an uploaded and processed administrative document."""

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_text = Column(Text, nullable=True)
    summary = Column(Text, nullable=True)
    category = Column(String(50), nullable=True)
    upload_date = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}', category='{self.category}')>"

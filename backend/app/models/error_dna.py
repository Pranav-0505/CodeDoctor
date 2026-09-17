import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class ErrorHistory(Base):
    __tablename__ = "error_histories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    category = Column(String, nullable=False)
    rule_id = Column(String, nullable=False)
    language = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    resolved = Column(Boolean, default=False)
    time_to_fix_seconds = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class ErrorDNA(Base):
    __tablename__ = "error_dnas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    top_error_categories = Column(JSON, default=dict)  # {"SYNTAX": 12, "TYPE": 5}
    most_improved_category = Column(String, nullable=True)
    repeated_mistakes_count = Column(Integer, default=0)
    avg_fix_time_seconds = Column(Float, default=0.0)
    severity_distribution = Column(JSON, default=dict)  # {"HIGH": 5, "CRITICAL": 2}
    language_weaknesses = Column(JSON, default=dict)  # {"python": ["IndexError", "UndefinedVar"]}
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="error_dna")

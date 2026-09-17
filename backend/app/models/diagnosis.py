import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Diagnosis(Base):
    __tablename__ = "diagnoses"

    id = Column(Integer, primary_key=True, index=True)
    scan_id = Column(Integer, ForeignKey("file_scans.id"), nullable=False)
    rule_id = Column(String, nullable=False)
    language = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    line = Column(Integer, default=1)
    column = Column(Integer, default=1)
    severity = Column(String, nullable=False)  # CRITICAL, HIGH, MEDIUM, LOW, INFO
    category = Column(String, nullable=False)  # SYNTAX, TYPE, LOGIC, RUNTIME, MEMORY, SECURITY, PERFORMANCE, STYLE, DEPENDENCY, CONFIGURATION, UNKNOWN
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    root_cause = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    impact = Column(Text, nullable=True)
    confidence = Column(Float, default=1.0)
    suggested_fix = Column(Text, nullable=True)
    corrected_code = Column(Text, nullable=True)
    is_root_cause = Column(Boolean, default=True)
    parent_issue_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    scan = relationship("FileScan", back_populates="diagnoses")
    fix_attempts = relationship("FixAttempt", back_populates="diagnosis", cascade="all, delete-orphan")

import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class FixAttempt(Base):
    __tablename__ = "fix_attempts"

    id = Column(Integer, primary_key=True, index=True)
    diagnosis_id = Column(Integer, ForeignKey("diagnoses.id"), nullable=False)
    original_code = Column(Text, nullable=False)
    patched_code = Column(Text, nullable=False)
    diff_patch = Column(Text, nullable=False)
    status = Column(String, default="PENDING")  # PENDING, VERIFIED, REJECTED, APPLIED, ROLLED_BACK
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    diagnosis = relationship("Diagnosis", back_populates="fix_attempts")
    verification_results = relationship("VerificationResult", back_populates="fix_attempt", cascade="all, delete-orphan")

class VerificationResult(Base):
    __tablename__ = "verification_results"

    id = Column(Integer, primary_key=True, index=True)
    fix_attempt_id = Column(Integer, ForeignKey("fix_attempts.id"), nullable=False)
    passed = Column(Boolean, default=False)
    verification_mode = Column(String, default="static_syntax")  # static_syntax, lint, unit_test, sandbox
    output_log = Column(Text, nullable=True)
    error_details = Column(Text, nullable=True)
    executed_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    fix_attempt = relationship("FixAttempt", back_populates="verification_results")

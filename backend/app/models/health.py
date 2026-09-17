import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class HealthReport(Base):
    __tablename__ = "health_reports"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    overall_score = Column(Float, nullable=False)
    correctness_score = Column(Float, nullable=False)   # Weight: 30%
    security_score = Column(Float, nullable=False)      # Weight: 20%
    maintainability_score = Column(Float, nullable=False) # Weight: 20%
    performance_score = Column(Float, nullable=False)   # Weight: 15%
    quality_score = Column(Float, nullable=False)       # Weight: 15%
    metrics_breakdown = Column(JSON, default=dict)
    scanned_files_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="health_reports")

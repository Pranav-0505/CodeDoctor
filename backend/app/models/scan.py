import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class FileScan(Base):
    __tablename__ = "file_scans"

    id = Column(Integer, primary_key=True, index=True)
    scan_uuid = Column(String, unique=True, index=True, nullable=False)
    file_path = Column(String, nullable=False)
    language = Column(String, nullable=False, default="python")
    code_content = Column(Text, nullable=True)
    total_issues = Column(Integer, default=0)
    critical_issues = Column(Integer, default=0)
    security_issues = Column(Integer, default=0)
    performance_issues = Column(Integer, default=0)
    health_score = Column(Float, default=100.0)
    platform = Column(String, default="web")  # web, cli, vscode, ci_cd
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="scans")
    project = relationship("Project", back_populates="scans")
    diagnoses = relationship("Diagnosis", back_populates="scan", cascade="all, delete-orphan")

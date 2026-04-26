"""Analysis model for storing health analysis results."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.extensions import db


class Analysis(db.Model):
    """Analysis model to store lab analysis results."""

    __tablename__ = 'analyses'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Analysis metadata
    analysis_type = Column(String(100), nullable=False)  # 'lab_report', 'health_assessment', etc.
    status = Column(String(50), default='completed', nullable=False)  # 'pending', 'completed', 'failed'

    # Original uploaded files info
    lab_report_filename = Column(String(255), nullable=True)
    health_assessment_filename = Column(String(255), nullable=True)

    # Analysis results (stored as JSON)
    lab_analysis = Column(JSON, nullable=True)  # Biomarkers data
    four_pillars = Column(JSON, nullable=True)  # Four pillars analysis
    supplements = Column(JSON, nullable=True)  # Supplements recommendations

    # Summary fields for quick access
    biomarkers_count = Column(Integer, nullable=True)
    overall_summary = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship('User', back_populates='analyses')

    def __repr__(self):
        return f'<Analysis {self.id} - User {self.user_id}>'

    def to_dict(self):
        """Convert analysis to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'analysis_type': self.analysis_type,
            'status': self.status,
            'lab_report_filename': self.lab_report_filename,
            'health_assessment_filename': self.health_assessment_filename,
            'lab_analysis': self.lab_analysis,
            'four_pillars': self.four_pillars,
            'supplements': self.supplements,
            'biomarkers_count': self.biomarkers_count,
            'overall_summary': self.overall_summary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

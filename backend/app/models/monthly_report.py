"""Monthly Report model for storing monthly health reports."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from app.extensions import db


class MonthlyReport(db.Model):
    """MonthlyReport model to store monthly health reports."""

    __tablename__ = 'monthly_reports'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Report metadata
    report_month = Column(String(7), nullable=False, index=True)  # Format: 'YYYY-MM'
    status = Column(String(50), default='completed', nullable=False)  # 'pending', 'completed', 'failed'

    # Report data (stored as JSON)
    monthly_overview_summary = Column(JSON, nullable=True)
    hormonal_balance_insight = Column(JSON, nullable=True)
    logged_patterns = Column(JSON, nullable=True)
    root_cause_tags = Column(JSON, nullable=True)
    actionable_next_steps = Column(JSON, nullable=True)
    radar_chart_data = Column(JSON, nullable=True)

    # Summary fields
    top_symptoms = Column(Text, nullable=True)  # Comma-separated
    health_reflection = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship('User', back_populates='monthly_reports')

    def __repr__(self):
        return f'<MonthlyReport {self.id} - {self.report_month} - User {self.user_id}>'

    def to_dict(self):
        """Convert monthly report to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'report_month': self.report_month,
            'status': self.status,
            'monthly_overview_summary': self.monthly_overview_summary,
            'hormonal_balance_insight': self.hormonal_balance_insight,
            'logged_patterns': self.logged_patterns,
            'root_cause_tags': self.root_cause_tags,
            'actionable_next_steps': self.actionable_next_steps,
            'radar_chart_data': self.radar_chart_data,
            'top_symptoms': self.top_symptoms,
            'health_reflection': self.health_reflection,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

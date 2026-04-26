"""User model for HealthAI application."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.extensions import db


class User(db.Model):
    """User model to store user information."""

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)

    # Auth fields
    password_hash = Column(String(512), nullable=True)
    email_verified = Column(Boolean, default=False, nullable=False)
    email_verification_token = Column(String(512), nullable=True)
    verification_token_expires = Column(DateTime, nullable=True)
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    locked_until = Column(DateTime, nullable=True)

    # User preferences
    age = Column(Integer, nullable=True)
    gender = Column(String(50), nullable=True)
    health_goals = Column(String(500), nullable=True)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)

    # Relationships
    analyses = relationship('Analysis', back_populates='user', cascade='all, delete-orphan')
    monthly_reports = relationship('MonthlyReport', back_populates='user', cascade='all, delete-orphan')
    chat_messages = relationship('ChatMessage', back_populates='user', cascade='all, delete-orphan')
    daily_logs = relationship('DailyLog', back_populates='user', cascade='all, delete-orphan')
    refresh_tokens = relationship('RefreshToken', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'

    def is_locked(self):
        if self.locked_until and self.locked_until > datetime.utcnow():
            return True
        return False

    def to_dict(self):
        """Convert user to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'health_goals': self.health_goals,
            'is_active': self.is_active,
            'email_verified': self.email_verified,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None
        }

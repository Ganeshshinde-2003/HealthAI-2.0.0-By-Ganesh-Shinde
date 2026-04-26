"""LoginAttempt model for audit logging and brute-force detection."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from app.extensions import db


class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='SET NULL'), nullable=True)
    email = Column(String(255), nullable=False, index=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(512), nullable=True)
    success = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

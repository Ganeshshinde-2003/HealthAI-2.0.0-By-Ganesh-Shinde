"""RefreshToken model for secure session management."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class RefreshToken(db.Model):
    __tablename__ = 'refresh_tokens'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    token_hash = Column(String(512), nullable=False, unique=True)
    expires_at = Column(DateTime, nullable=False)
    revoked = Column(Boolean, default=False, nullable=False)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(512), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship('User', back_populates='refresh_tokens')

    def is_valid(self):
        return not self.revoked and self.expires_at > datetime.utcnow()

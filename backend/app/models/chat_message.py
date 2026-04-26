"""Chat Message model for storing chat history."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.extensions import db


class ChatMessage(db.Model):
    """ChatMessage model to store chat conversation history."""

    __tablename__ = 'chat_messages'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Message details
    role = Column(String(50), nullable=False)  # 'user' or 'assistant'
    message = Column(Text, nullable=False)

    # Optional context/metadata
    session_id = Column(String(255), nullable=True, index=True)  # Group messages by session
    context_type = Column(String(100), nullable=True)  # 'lab_analysis', 'monthly_report', 'general'

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    # Relationships
    user = relationship('User', back_populates='chat_messages')

    def __repr__(self):
        return f'<ChatMessage {self.id} - {self.role} - User {self.user_id}>'

    def to_dict(self):
        """Convert chat message to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'role': self.role,
            'message': self.message,
            'session_id': self.session_id,
            'context_type': self.context_type,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

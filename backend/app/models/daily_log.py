"""Daily Log model for storing daily health logs."""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Float, JSON
from sqlalchemy.orm import relationship
from app.extensions import db


class DailyLog(db.Model):
    """DailyLog model to store daily health tracking logs."""

    __tablename__ = 'daily_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    # Log date
    log_date = Column(DateTime, nullable=False, index=True)

    # Four Pillars tracking
    # Eat Well
    meals = Column(JSON, nullable=True)  # List of meals with details
    meal_satisfaction_score = Column(Float, nullable=True)  # 1-10 scale
    processed_food = Column(String(50), nullable=True)  # 'yes', 'no', 'moderate'

    # Sleep Well
    sleep_hours = Column(Float, nullable=True)
    sleep_quality = Column(Float, nullable=True)  # 1-10 scale
    sleep_notes = Column(Text, nullable=True)

    # Move Well
    exercise_type = Column(String(255), nullable=True)
    exercise_duration_minutes = Column(Integer, nullable=True)
    exercise_intensity = Column(String(50), nullable=True)  # 'low', 'moderate', 'high'
    steps = Column(Integer, nullable=True)

    # Recover Well
    stress_level = Column(Float, nullable=True)  # 1-10 scale
    mood = Column(String(100), nullable=True)
    recovery_activities = Column(JSON, nullable=True)  # List of recovery activities
    menstrual_cycle_day = Column(Integer, nullable=True)  # Day of cycle
    symptoms = Column(JSON, nullable=True)  # List of symptoms

    # General notes
    notes = Column(Text, nullable=True)
    energy_level = Column(Float, nullable=True)  # 1-10 scale

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship('User', back_populates='daily_logs')

    def __repr__(self):
        return f'<DailyLog {self.id} - {self.log_date} - User {self.user_id}>'

    def to_dict(self):
        """Convert daily log to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'log_date': self.log_date.isoformat() if self.log_date else None,
            'meals': self.meals,
            'meal_satisfaction_score': self.meal_satisfaction_score,
            'processed_food': self.processed_food,
            'sleep_hours': self.sleep_hours,
            'sleep_quality': self.sleep_quality,
            'sleep_notes': self.sleep_notes,
            'exercise_type': self.exercise_type,
            'exercise_duration_minutes': self.exercise_duration_minutes,
            'exercise_intensity': self.exercise_intensity,
            'steps': self.steps,
            'stress_level': self.stress_level,
            'mood': self.mood,
            'recovery_activities': self.recovery_activities,
            'menstrual_cycle_day': self.menstrual_cycle_day,
            'symptoms': self.symptoms,
            'notes': self.notes,
            'energy_level': self.energy_level,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

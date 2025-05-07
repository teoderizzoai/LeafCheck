"""
Expanded database models for the LeafCheck application.
This file defines User, Image, Prediction, and AnalysisHistory tables with all required fields and relationships.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship, declarative_base

# The declarative base is the foundation for all ORM models.
Base = declarative_base()

class User(Base):
    """
    User model: represents a user in the system.
    Includes authentication and audit fields.
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # One-to-many relationship: a user can have many images.
    images = relationship("Image", back_populates="user", cascade="all, delete-orphan")
    analysis_history = relationship("AnalysisHistory", back_populates="user", cascade="all, delete-orphan")

class Image(Base):
    """
    Image model: represents an uploaded image.
    Each image is linked to a user via user_id.
    """
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Nullable for anonymous uploads
    filename = Column(String(255), nullable=False)
    file_path = Column(String(512), nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)
    image_metadata = Column(JSON)  # Store image metadata (size, format, etc.)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Many-to-one relationship: each image belongs to one user.
    user = relationship("User", back_populates="images")
    predictions = relationship("Prediction", back_populates="image", cascade="all, delete-orphan")
    analysis_history = relationship("AnalysisHistory", back_populates="image", cascade="all, delete-orphan")

class Prediction(Base):
    """
    Prediction model: stores analysis results for an image.
    Each prediction is linked to an image.
    """
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id'), nullable=False)
    prediction_type = Column(String(50), nullable=False)  # e.g., 'health', 'disease'
    result_data = Column(JSON, nullable=False)  # Store prediction details
    confidence_score = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Many-to-one relationship: each prediction belongs to one image.
    image = relationship("Image", back_populates="predictions")
    analysis_history = relationship("AnalysisHistory", back_populates="prediction", cascade="all, delete-orphan")

class AnalysisHistory(Base):
    """
    AnalysisHistory model: tracks user interactions and predictions.
    Can be used for both authenticated and anonymous users.
    """
    __tablename__ = 'analysis_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)  # Nullable for anonymous users
    image_id = Column(Integer, ForeignKey('images.id'), nullable=False)
    prediction_id = Column(Integer, ForeignKey('predictions.id'), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="analysis_history")
    image = relationship("Image", back_populates="analysis_history")
    prediction = relationship("Prediction", back_populates="analysis_history") 
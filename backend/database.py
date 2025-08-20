from sqlalchemy import create_engine, Column, Integer, String, DateTime, LargeBinary, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Database configuration
DATABASE_URL = "sqlite:///./mirror_app.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to selfies
    selfies = relationship("Selfie", back_populates="user")


class Selfie(Base):
    __tablename__ = "selfies"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_filename = Column(String, nullable=False)
    file_data = Column(LargeBinary, nullable=False)  # Store binary data directly
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationship to user
    user = relationship("User", back_populates="selfies")


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create tables
def create_tables():
    Base.metadata.create_all(bind=engine)
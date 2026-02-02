from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class Chart(Base):
    __tablename__ = "charts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    week = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    region = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    entries = relationship("ChartEntry", back_populates="chart")


class ChartEntry(Base):
    __tablename__ = "chart_entries"
    
    id = Column(Integer, primary_key=True, index=True)
    chart_id = Column(Integer, ForeignKey("charts.id"), nullable=False)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    rank = Column(Integer, nullable=False)
    previous_rank = Column(Integer)
    trend = Column(String(50))  # "up", "down", "stable", "new"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    chart = relationship("Chart", back_populates="entries")
    song = relationship("Song", back_populates="chart_entries")

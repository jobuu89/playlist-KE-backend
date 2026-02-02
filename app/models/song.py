from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    artist_id = Column(Integer, ForeignKey("artists.id"), nullable=False)
    album = Column(String(255))
    duration_seconds = Column(Integer)
    release_date = Column(DateTime(timezone=True))
    genre = Column(String(100))
    region = Column(String(100))
    stream_count = Column(Integer, default=0)
    rating = Column(Integer, default=0)
    cover_url = Column(String(500))
    audio_url = Column(String(500))
    is_explicit = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    artist = relationship("Artist", back_populates="songs")
    playlist_songs = relationship("PlaylistSong", back_populates="song")
    chart_entries = relationship("ChartEntry", back_populates="song")
    analytics = relationship("Analytics", back_populates="song")

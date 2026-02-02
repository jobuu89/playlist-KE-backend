from pydantic import BaseModel
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.artist import ArtistResponse


class SongBase(BaseModel):
    title: str
    artist_id: int
    genre: Optional[str] = None
    region: Optional[str] = None


class SongCreate(SongBase):
    album: Optional[str] = None
    duration_seconds: Optional[int] = None
    release_date: Optional[datetime] = None
    cover_url: Optional[str] = None
    audio_url: Optional[str] = None
    is_explicit: Optional[bool] = False


class SongUpdate(BaseModel):
    title: Optional[str] = None
    album: Optional[str] = None
    duration_seconds: Optional[int] = None
    release_date: Optional[datetime] = None
    genre: Optional[str] = None
    region: Optional[str] = None
    cover_url: Optional[str] = None
    audio_url: Optional[str] = None
    is_explicit: Optional[bool] = None
    stream_count: Optional[int] = None
    rating: Optional[int] = None


class SongResponse(SongBase):
    id: int
    album: Optional[str] = None
    duration_seconds: Optional[int] = None
    release_date: Optional[datetime] = None
    stream_count: int
    rating: int
    cover_url: Optional[str] = None
    audio_url: Optional[str] = None
    is_explicit: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


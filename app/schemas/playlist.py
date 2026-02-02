from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.schemas.song import SongResponse


class PlaylistBase(BaseModel):
    name: str
    is_public: bool = True


class PlaylistCreate(PlaylistBase):
    description: Optional[str] = None
    cover_url: Optional[str] = None


class PlaylistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_public: Optional[bool] = None
    cover_url: Optional[str] = None


class PlaylistResponse(PlaylistBase):
    id: int
    description: Optional[str] = None
    user_id: int
    cover_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PlaylistSongAdd(BaseModel):
    song_id: int
    order: Optional[int] = None


class PlaylistSongResponse(BaseModel):
    id: int
    playlist_id: int
    song_id: int
    order: int
    added_at: datetime
    song: Optional["SongResponse"] = None
    
    class Config:
        from_attributes = True


class PlaylistDetailResponse(PlaylistBase):
    id: int
    description: Optional[str] = None
    user_id: int
    cover_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    songs: List[PlaylistSongResponse] = []
    
    class Config:
        from_attributes = True

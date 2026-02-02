from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ArtistBase(BaseModel):
    name: str
    region: Optional[str] = None
    genre: Optional[str] = None


class ArtistCreate(ArtistBase):
    bio: Optional[str] = None
    image_url: Optional[str] = None


class ArtistUpdate(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None
    image_url: Optional[str] = None
    region: Optional[str] = None
    genre: Optional[str] = None
    monthly_listeners: Optional[int] = None


class ArtistResponse(ArtistBase):
    id: int
    bio: Optional[str] = None
    image_url: Optional[str] = None
    monthly_listeners: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database.connection import get_db
from app.models import Artist, Song
from app.schemas.artist import ArtistCreate, ArtistUpdate, ArtistResponse
from app.schemas.song import SongResponse
from app.services import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/artists", tags=["Artists"])


@router.get("/", response_model=List[ArtistResponse])
async def get_artists(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    genre: Optional[str] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get list of artists with optional filters"""
    query = db.query(Artist)
    
    if genre:
        query = query.filter(Artist.genre == genre)
    if region:
        query = query.filter(Artist.region == region)
    
    artists = query.offset(skip).limit(limit).all()
    return artists


@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist(artist_id: int, db: Session = Depends(get_db)):
    """Get artist details by ID"""
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    return artist


@router.get("/{artist_id}/songs", response_model=List[SongResponse])
async def get_artist_songs(
    artist_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all songs by an artist"""
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    
    songs = db.query(Song).filter(Song.artist_id == artist_id).offset(skip).limit(limit).all()
    return songs


@router.post("/", response_model=ArtistResponse)
async def create_artist(
    artist_data: ArtistCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new artist"""
    new_artist = Artist(**artist_data.model_dump())
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)
    
    return new_artist


@router.put("/{artist_id}", response_model=ArtistResponse)
async def update_artist(
    artist_id: int,
    artist_data: ArtistUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update an artist"""
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    
    update_data = artist_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(artist, field, value)
    
    db.commit()
    db.refresh(artist)
    
    return artist


@router.delete("/{artist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artist(
    artist_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete an artist"""
    artist = db.query(Artist).filter(Artist.id == artist_id).first()
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    
    db.delete(artist)
    db.commit()


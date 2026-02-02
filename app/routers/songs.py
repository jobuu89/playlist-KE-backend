from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from app.database.connection import get_db
from app.models import Song, Artist
from app.schemas.song import SongCreate, SongUpdate, SongResponse
from app.services import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/songs", tags=["Songs"])


@router.get("/", response_model=List[SongResponse])
async def get_songs(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    genre: Optional[str] = None,
    region: Optional[str] = None,
    artist_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get list of songs with optional filters"""
    query = db.query(Song)
    
    if genre:
        query = query.filter(Song.genre == genre)
    if region:
        query = query.filter(Song.region == region)
    if artist_id:
        query = query.filter(Song.artist_id == artist_id)
    
    songs = query.offset(skip).limit(limit).all()
    return songs


@router.get("/trending", response_model=List[SongResponse])
async def get_trending_songs(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get trending songs by stream count"""
    songs = db.query(Song).order_by(Song.stream_count.desc()).limit(limit).all()
    return songs


@router.get("/new-releases", response_model=List[SongResponse])
async def get_new_releases(
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get recently added songs"""
    songs = db.query(Song).order_by(Song.created_at.desc()).limit(limit).all()
    return songs


@router.get("/{song_id}", response_model=SongResponse)
async def get_song(song_id: int, db: Session = Depends(get_db)):
    """Get song details by ID"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )
    return song


@router.post("/", response_model=SongResponse)
async def create_song(
    song_data: SongCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new song (admin only)"""
    # Check if artist exists
    artist = db.query(Artist).filter(Artist.id == song_data.artist_id).first()
    if not artist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist not found"
        )
    
    new_song = Song(**song_data.model_dump())
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    
    return new_song


@router.put("/{song_id}", response_model=SongResponse)
async def update_song(
    song_id: int,
    song_data: SongUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )
    
    update_data = song_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(song, field, value)
    
    db.commit()
    db.refresh(song)
    
    return song


@router.delete("/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_song(
    song_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a song"""
    song = db.query(Song).filter(Song.id == song_id).first()
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )
    
    db.delete(song)
    db.commit()


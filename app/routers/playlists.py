from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from app.database.connection import get_db
from app.models import Playlist, PlaylistSong, User
from app.schemas.playlist import (
    PlaylistCreate, 
    PlaylistUpdate, 
    PlaylistResponse, 
    PlaylistDetailResponse,
    PlaylistSongAdd
)
from app.services import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/playlists", tags=["Playlists"])


@router.get("/", response_model=List[PlaylistResponse])
async def get_playlists(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get public playlists"""
    playlists = db.query(Playlist).filter(
        Playlist.is_public == True
    ).offset(skip).limit(limit).all()
    return playlists


@router.get("/{playlist_id}", response_model=PlaylistDetailResponse)
async def get_playlist(playlist_id: int, db: Session = Depends(get_db)):
    """Get playlist details by ID"""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    return playlist


@router.post("/", response_model=PlaylistResponse)
async def create_playlist(
    playlist_data: PlaylistCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new playlist"""
    new_playlist = Playlist(
        **playlist_data.model_dump(),
        user_id=current_user.id
    )
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    
    return new_playlist


@router.put("/{playlist_id}", response_model=PlaylistResponse)
async def update_playlist(
    playlist_id: int,
    playlist_data: PlaylistUpdate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update a playlist"""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    # Check ownership
    if playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this playlist"
        )
    
    update_data = playlist_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(playlist, field, value)
    
    db.commit()
    db.refresh(playlist)
    
    return playlist


@router.delete("/{playlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_playlist(
    playlist_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Delete a playlist"""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    # Check ownership
    if playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this playlist"
        )
    
    db.delete(playlist)
    db.commit()


@router.post("/{playlist_id}/songs", response_model=PlaylistDetailResponse)
async def add_song_to_playlist(
    playlist_id: int,
    song_data: PlaylistSongAdd,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add a song to playlist"""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    # Check ownership
    if playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this playlist"
        )
    
    # Get max order
    max_order = db.query(func.max(PlaylistSong.order)).filter(
        PlaylistSong.playlist_id == playlist_id
    ).scalar() or 0
    
    new_playlist_song = PlaylistSong(
        playlist_id=playlist_id,
        song_id=song_data.song_id,
        order=song_data.order or max_order + 1
    )
    db.add(new_playlist_song)
    db.commit()
    db.refresh(playlist)
    
    return playlist


@router.delete("/{playlist_id}/songs/{song_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_song_from_playlist(
    playlist_id: int,
    song_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Remove a song from playlist"""
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()
    if not playlist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Playlist not found"
        )
    
    # Check ownership
    if playlist.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to modify this playlist"
        )
    
    playlist_song = db.query(PlaylistSong).filter(
        PlaylistSong.playlist_id == playlist_id,
        PlaylistSong.song_id == song_id
    ).first()
    
    if not playlist_song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found in playlist"
        )
    
    db.delete(playlist_song)
    db.commit()


@router.get("/user/{user_id}", response_model=List[PlaylistResponse])
async def get_user_playlists(
    user_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get playlists by user (own playlists or public playlists)"""
    query = db.query(Playlist).filter(Playlist.user_id == user_id)
    
    # Non-owner can only see public playlists
    if user_id != current_user.id:
        query = query.filter(Playlist.is_public == True)
    
    playlists = query.offset(skip).limit(limit).all()
    return playlists


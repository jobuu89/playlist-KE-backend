# Import all models from individual files to avoid circular imports
from app.database.connection import Base

# Import models from individual files
from app.models.user import User
from app.models.artist import Artist
from app.models.song import Song
from app.models.playlist import Playlist, PlaylistSong
from app.models.chart import Chart, ChartEntry
from app.models.analytics import Analytics

__all__ = [
    "Base", "User", "Artist", "Song", "Playlist", "PlaylistSong", 
    "Chart", "ChartEntry", "Analytics"
]

# Routers module - import routers here
from app.routers.auth import router as auth_router
from app.routers.songs import router as songs_router
from app.routers.artists import router as artists_router
from app.routers.playlists import router as playlists_router
from app.routers.charts import router as charts_router
from app.routers.analytics import router as analytics_router
from app.routers.users import router as users_router

__all__ = [
    "auth_router",
    "songs_router",
    "artists_router",
    "playlists_router",
    "charts_router",
    "analytics_router",
    "users_router",
]


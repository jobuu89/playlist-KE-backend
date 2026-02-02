from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database.connection import init_db
from app.routers import auth_router, songs_router, artists_router, playlists_router, charts_router, analytics_router, users_router

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend API for Playlist-KE music streaming platform",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include routers
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(songs_router, prefix=settings.API_V1_PREFIX)
app.include_router(artists_router, prefix=settings.API_V1_PREFIX)
app.include_router(playlists_router, prefix=settings.API_V1_PREFIX)
app.include_router(charts_router, prefix=settings.API_V1_PREFIX)
app.include_router(analytics_router, prefix=settings.API_V1_PREFIX)
app.include_router(users_router, prefix=settings.API_V1_PREFIX)


# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()
    print(f"🚀 {settings.APP_NAME} is running!")
    print(f"📚 API Documentation: http://127.0.0.1:8000{settings.API_V1_PREFIX}/docs")


@app.get("/")
async def root():
    return {
        "message": "Welcome to Playlist-KE Backend",
        "version": "1.0.0",
        "docs": f"{settings.API_V1_PREFIX}/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


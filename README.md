# Playlist-KE Backend

A FastAPI-based backend for the Playlist-KE music streaming platform.

## Features

- **User Authentication**: JWT-based authentication with registration and login
- **Music Management**: Songs, artists, albums management
- **Playlists**: Create and manage personal playlists
- **Charts**: Weekly music charts with rankings
- **Analytics**: Streaming statistics and region-wise analytics
- **RESTful API**: Clean and documented API endpoints

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: JWT (JSON Web Tokens)
- **Validation**: Pydantic v2

## Project Structure

```
playlist-KE-backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # Application entry point
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py         # Configuration settings
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py       # Database connection and setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py             # User model
│   │   ├── artist.py           # Artist model
│   │   ├── song.py             # Song model
│   │   ├── playlist.py         # Playlist model
│   │   ├── chart.py            # Chart model
│   │   └── analytics.py        # Analytics model
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py             # User Pydantic schemas
│   │   ├── artist.py           # Artist Pydantic schemas
│   │   ├── song.py             # Song Pydantic schemas
│   │   ├── playlist.py         # Playlist Pydantic schemas
│   │   ├── chart.py            # Chart Pydantic schemas
│   │   └── analytics.py        # Analytics Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py             # Authentication endpoints
│   │   ├── songs.py            # Song endpoints
│   │   ├── artists.py          # Artist endpoints
│   │   ├── playlists.py        # Playlist endpoints
│   │   ├── charts.py           # Chart endpoints
│   │   ├── analytics.py        # Analytics endpoints
│   │   └── users.py            # User endpoints
│   └── services/
│       ├── __init__.py
│       ├── auth_service.py     # Authentication utilities
│       └── analytics_service.py # Analytics service
├── requirements.txt            # Python dependencies
├── README.md                   # This file
└── .env.example                # Environment variables template
```

## Setup

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment** (optional):
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at:
- **Base URL**: http://127.0.0.1:8000
- **Swagger Docs**: http://127.0.0.1:8000/api/v1/docs
- **ReDoc**: http://127.0.0.1:8000/api/v1/redoc

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get token
- `GET /api/v1/auth/me` - Get current user
- `PUT /api/v1/auth/me` - Update current user

### Songs
- `GET /api/v1/songs` - List songs (with filters)
- `GET /api/v1/songs/trending` - Get trending songs
- `GET /api/v1/songs/new-releases` - Get new releases
- `GET /api/v1/songs/{id}` - Get song details
- `POST /api/v1/songs` - Create song (auth required)
- `PUT /api/v1/songs/{id}` - Update song (auth required)
- `DELETE /api/v1/songs/{id}` - Delete song (auth required)

### Artists
- `GET /api/v1/artists` - List artists
- `GET /api/v1/artists/{id}` - Get artist details
- `GET /api/v1/artists/{id}/songs` - Get artist's songs
- `POST /api/v1/artists` - Create artist (auth required)
- `PUT /api/v1/artists/{id}` - Update artist (auth required)
- `DELETE /api/v1/artists/{id}` - Delete artist (auth required)

### Playlists
- `GET /api/v1/playlists` - List public playlists
- `GET /api/v1/playlists/{id}` - Get playlist details
- `POST /api/v1/playlists` - Create playlist
- `PUT /api/v1/playlists/{id}` - Update playlist
- `DELETE /api/v1/playlists/{id}` - Delete playlist
- `POST /api/v1/playlists/{id}/songs` - Add song to playlist
- `DELETE /api/v1/playlists/{id}/songs/{song_id}` - Remove song from playlist
- `GET /api/v1/playlists/user/{user_id}` - Get user's playlists

### Charts
- `GET /api/v1/charts` - List all charts
- `GET /api/v1/charts/weekly` - Get weekly chart
- `GET /api/v1/charts/{id}` - Get chart details
- `GET /api/v1/charts/history/{song_id}` - Get song chart history
- `POST /api/v1/charts` - Create chart (auth required)
- `POST /api/v1/charts/{id}/entries` - Add chart entry (auth required)

### Analytics
- `GET /api/v1/analytics/overview` - Get analytics overview
- `GET /api/v1/analytics/regions` - Get region analytics
- `GET /api/v1/analytics/songs/{song_id}` - Get song analytics

### Users
- `GET /api/v1/users/{id}` - Get user by ID
- `GET /api/v1/users/{id}/playlists` - Get user's playlists

## Environment Variables

Create a `.env` file with the following variables:

```env
# Application
APP_NAME="Playlist-KE Backend"
API_V1_PREFIX="/api/v1"

# Database
DATABASE_URL="sqlite:///./playlist_ke.db"

# Security
SECRET_KEY="your-secret-key-here"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:5173", "http://localhost:3000"]
```

## Testing

Run tests with pytest:
```bash
pytest
```

## License

MIT


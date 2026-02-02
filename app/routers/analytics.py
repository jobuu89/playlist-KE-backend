from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.services.analytics_service import AnalyticsService
from app.schemas.analytics import AnalyticsOverview, RegionAnalytics
from app.services import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/overview", response_model=AnalyticsOverview)
async def get_analytics_overview(
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get analytics overview"""
    service = AnalyticsService(db)
    return service.get_overview()


@router.get("/regions", response_model=List[RegionAnalytics])
async def get_region_analytics(
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get analytics grouped by region"""
    service = AnalyticsService(db)
    return service.get_region_analytics()


@router.get("/songs/{song_id}")
async def get_song_analytics(
    song_id: int,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get detailed analytics for a specific song"""
    service = AnalyticsService(db)
    result = service.get_song_analytics(song_id)
    
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )
    
    return result


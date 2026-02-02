from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Optional, List
from app.database.connection import get_db
from app.models import Chart, ChartEntry, Song
from app.schemas.chart import (
    ChartCreate, 
    ChartResponse, 
    ChartDetailResponse,
    ChartEntryCreate,
    ChartEntryResponse,
    WeeklyChartResponse
)
from app.services import get_current_active_user
from app.schemas.user import UserResponse

router = APIRouter(prefix="/charts", tags=["Charts"])


@router.get("/", response_model=List[ChartResponse])
async def get_charts(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """Get all charts"""
    charts = db.query(Chart).offset(skip).limit(limit).all()
    return charts


@router.get("/weekly", response_model=WeeklyChartResponse)
async def get_weekly_chart(
    week: Optional[int] = None,
    year: Optional[int] = None,
    region: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get weekly chart"""
    import datetime
    now = datetime.datetime.now()
    current_week = week or now.isocalendar()[1]
    current_year = year or now.year
    
    query = db.query(Chart).filter(
        Chart.week == current_week,
        Chart.year == current_year
    )
    
    if region:
        query = query.filter(Chart.region == region)
    
    chart = query.first()
    
    if not chart:
        return WeeklyChartResponse(
            week=current_week,
            year=current_year,
            region=region,
            entries=[]
        )
    
    entries = db.query(ChartEntry).filter(
        ChartEntry.chart_id == chart.id
    ).order_by(ChartEntry.rank).all()
    
    return WeeklyChartResponse(
        week=chart.week,
        year=chart.year,
        region=chart.region,
        entries=entries
    )


@router.get("/{chart_id}", response_model=ChartDetailResponse)
async def get_chart_details(chart_id: int, db: Session = Depends(get_db)):
    """Get chart details with entries"""
    chart = db.query(Chart).filter(Chart.id == chart_id).first()
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not found"
        )
    
    entries = db.query(ChartEntry).filter(
        ChartEntry.chart_id == chart_id
    ).order_by(ChartEntry.rank).all()
    
    return ChartDetailResponse(
        id=chart.id,
        name=chart.name,
        week=chart.week,
        year=chart.year,
        region=chart.region,
        created_at=chart.created_at,
        entries=entries
    )


@router.get("/history/{song_id}", response_model=List[ChartEntryResponse])
async def get_song_chart_history(
    song_id: int,
    limit: int = Query(50, ge=1, le=500),
    db: Session = Depends(get_db)
):
    """Get chart history for a song"""
    entries = db.query(ChartEntry).filter(
        ChartEntry.song_id == song_id
    ).order_by(ChartEntry.created_at.desc()).limit(limit).all()
    
    return entries


@router.post("/", response_model=ChartResponse)
async def create_chart(
    chart_data: ChartCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create a new chart"""
    new_chart = Chart(**chart_data.model_dump())
    db.add(new_chart)
    db.commit()
    db.refresh(new_chart)
    
    return new_chart


@router.post("/{chart_id}/entries", response_model=ChartEntryResponse)
async def add_chart_entry(
    chart_id: int,
    entry_data: ChartEntryCreate,
    current_user: UserResponse = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Add entry to chart"""
    # Verify chart exists
    chart = db.query(Chart).filter(Chart.id == chart_id).first()
    if not chart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chart not found"
        )
    
    # Verify song exists
    song = db.query(Song).filter(Song.id == entry_data.song_id).first()
    if not song:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Song not found"
        )
    
    new_entry = ChartEntry(
        chart_id=chart_id,
        song_id=entry_data.song_id,
        rank=entry_data.rank,
        previous_rank=entry_data.previous_rank,
        trend=entry_data.trend
    )
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    
    return new_entry


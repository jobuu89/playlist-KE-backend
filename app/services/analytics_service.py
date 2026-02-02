from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import Song, Analytics, Artist
from app.schemas.analytics import AnalyticsOverview, RegionAnalytics


class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_overview(self) -> AnalyticsOverview:
        """Get analytics overview"""
        total_streams = self.db.query(func.coalesce(func.sum(Analytics.stream_count), 0)).scalar() or 0
        total_unique = self.db.query(func.coalesce(func.sum(Analytics.unique_listeners), 0)).scalar() or 0
        total_likes = self.db.query(func.coalesce(func.sum(Analytics.likes_count), 0)).scalar() or 0
        total_shares = self.db.query(func.coalesce(func.sum(Analytics.shares_count), 0)).scalar() or 0
        
        # Get top songs by streams
        top_songs = self.db.query(Song).order_by(Song.stream_count.desc()).limit(10).all()
        
        # Get region breakdown
        region_data = (
            self.db.query(
                Analytics.region,
                func.sum(Analytics.stream_count).label('total_streams'),
                func.sum(Analytics.unique_listeners).label('total_listeners')
            )
            .group_by(Analytics.region)
            .all()
        )
        
        top_regions = [
            {
                "region": r.region or "Unknown",
                "total_streams": r.total_streams or 0,
                "unique_listeners": r.total_listeners or 0
            }
            for r in region_data
        ]
        
        return AnalyticsOverview(
            total_streams=total_streams,
            total_unique_listeners=total_unique,
            total_likes=total_likes,
            total_shares=total_shares,
            top_songs=top_songs,
            top_regions=top_regions
        )
    
    def get_region_analytics(self) -> list[RegionAnalytics]:
        """Get analytics grouped by region"""
        region_data = (
            self.db.query(
                Analytics.region,
                func.sum(Analytics.stream_count).label('total_streams'),
                func.sum(Analytics.unique_listeners).label('total_listeners')
            )
            .group_by(Analytics.region)
            .all()
        )
        
        total_streams = sum(r.total_streams or 0 for r in region_data)
        
        return [
            RegionAnalytics(
                region=r.region or "Unknown",
                total_streams=r.total_streams or 0,
                unique_listeners=r.total_listeners or 0,
                share_percentage=(r.total_streams or 0) / total_streams * 100 if total_streams > 0 else 0
            )
            for r in region_data
        ]
    
    def get_song_analytics(self, song_id: int):
        """Get detailed analytics for a specific song"""
        song = self.db.query(Song).filter(Song.id == song_id).first()
        if not song:
            return None
        
        total_streams = self.db.query(func.coalesce(func.sum(Analytics.stream_count), 0)).filter(
            Analytics.song_id == song_id
        ).scalar() or 0
        
        total_unique = self.db.query(func.coalesce(func.sum(Analytics.unique_listeners), 0)).filter(
            Analytics.song_id == song_id
        ).scalar() or 0
        
        region_data = (
            self.db.query(
                Analytics.region,
                func.sum(Analytics.stream_count).label('total_streams'),
                func.sum(Analytics.unique_listeners).label('total_listeners')
            )
            .filter(Analytics.song_id == song_id)
            .group_by(Analytics.region)
            .all()
        )
        
        daily_stats = self.db.query(Analytics).filter(
            Analytics.song_id == song_id
        ).order_by(Analytics.date.desc()).limit(30).all()
        
        region_breakdown = [
            RegionAnalytics(
                region=r.region or "Unknown",
                total_streams=r.total_streams or 0,
                unique_listeners=r.total_listeners or 0,
                share_percentage=0
            )
            for r in region_data
        ]
        
        return {
            "song": song,
            "total_streams": total_streams,
            "total_unique_listeners": total_unique,
            "region_breakdown": region_breakdown,
            "daily_stats": daily_stats
        }


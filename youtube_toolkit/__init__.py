"""
YouTube Toolkit - A comprehensive YouTube information and download toolkit.

Install with: uv add youtube-toolkit
Usage: from youtube_toolkit import YouTubeToolkit

Features:
- Extract video information from YouTube URLs
- Download audio and video in various formats
- Search YouTube videos with filters
- Extract captions and transcripts
- Fetch comments and rich metadata
- Anti-detection measures for reliable downloads
- Channel support: get all videos, shorts, streams (v0.3+)
- Video chapters and engagement data (v0.3+)
- Advanced search with native filters (v0.3+)

New Clean API (v0.1.0+):
    toolkit = YouTubeToolkit()

    # Get video info as dataclass
    video = toolkit.get_video(url)
    print(video.title, video.duration)

    # Download with DownloadResult
    result = toolkit.download(url, type='audio', format='mp3')
    if result.success:
        print(result.file_path)

    # Search with SearchResult
    results = toolkit.search('query', max_results=10)
    for item in results.items:
        print(item.title)

Channel Support (v0.3+):
    # Get channel videos (uses pytubefix)
    videos = toolkit.get_channel_videos("@Fireship", limit=50)

    # Get ALL channel videos (requires: pip install youtube-toolkit[scrapers])
    all_videos = toolkit.get_all_channel_videos("@Fireship")

    # Get channel info
    info = toolkit.get_channel_info("@Fireship")

    # Get video chapters
    chapters = toolkit.get_video_chapters(url)

    # Advanced search with filters (no API quota)
    results = toolkit.search_with_filters(
        "python tutorial",
        duration='medium',
        upload_date='month',
        sort_by='views'
    )
"""

from .api import YouTubeToolkit

__all__ = ["YouTubeToolkit"]
__version__ = "0.5.0"
__author__ = "Bo-Yu Chen"
__description__ = "A comprehensive YouTube information and download toolkit"

# Convenience imports for common use cases
from .core import VideoInfo, DownloadResult, SearchResult, PostProcessorFactory
from .core.search import SearchFilters, SearchResultItem, Thumbnails, Thumbnail, BooleanSearchQuery, YOUTUBE_CATEGORIES
from .core.comments import CommentFilters, CommentResult, Comment, CommentAuthor, CommentMetrics, CommentAnalytics, CommentSentimentAnalyzer, CommentOrder
from .core.captions import CaptionFilters, CaptionResult, CaptionTrack, CaptionContent, CaptionCue, CaptionAnalytics, CaptionFormatConverter, CaptionAnalyzer

# Make core classes available at package level for convenience
__all__.extend([
    "VideoInfo", "DownloadResult", "SearchResult", "PostProcessorFactory",
    "SearchFilters", "SearchResultItem", "Thumbnails", "Thumbnail",
    "BooleanSearchQuery", "YOUTUBE_CATEGORIES",
    "CommentFilters", "CommentResult", "Comment", "CommentAuthor",
    "CommentMetrics", "CommentAnalytics", "CommentSentimentAnalyzer", "CommentOrder",
    "CaptionFilters", "CaptionResult", "CaptionTrack", "CaptionContent",
    "CaptionCue", "CaptionAnalytics", "CaptionFormatConverter", "CaptionAnalyzer"
])

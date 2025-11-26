"""
Sub-API classes for action-based API design.

This module provides the three core action APIs:
- GetAPI: Retrieve information (video, channel, playlist, etc.)
- DownloadAPI: Save content to disk (audio, video, captions)
- SearchAPI: Find content (videos, channels, playlists)

Each sub-API is callable for smart defaults and has explicit methods for control.

The callable methods return the same types as the legacy API for backward compatibility:
- download() returns DownloadResult
- search() returns SearchResult
"""

from typing import Optional, List, Dict, Any, Union, TYPE_CHECKING
import os
import time

if TYPE_CHECKING:
    from .api import YouTubeToolkit


# =============================================================================
# GET API - Retrieve information
# =============================================================================

class ChannelGetAPI:
    """Sub-API for channel-related get operations."""

    def __init__(self, parent: 'GetAPI'):
        self._parent = parent
        self._toolkit = parent._toolkit

    def __call__(self, channel: str) -> Dict[str, Any]:
        """
        Get channel information.

        Args:
            channel: Channel URL, handle (@name), or ID

        Returns:
            Channel metadata dict
        """
        return self._toolkit.pytubefix.get_channel_info(channel)

    def videos(self, channel: str,
               limit: Optional[int] = None,
               sort_by: str = 'newest',
               use_scrapetube: bool = False) -> List[Dict[str, Any]]:
        """
        Get videos from a channel.

        Args:
            channel: Channel URL, handle, or ID
            limit: Maximum videos to return (None = all available)
            sort_by: 'newest', 'oldest', or 'popular'
            use_scrapetube: Use scrapetube for unlimited results

        Returns:
            List of video info dicts
        """
        if use_scrapetube:
            try:
                from .handlers.scrapetube_handler import ScrapeTubeHandler
                handler = ScrapeTubeHandler()
                return handler.get_channel_videos(channel, limit=limit, sort_by=sort_by)
            except ImportError:
                if self._toolkit.verbose:
                    print("⚠️ scrapetube not installed. Using pytubefix.")

        return self._toolkit.pytubefix.get_channel_videos(
            channel, content_type='videos', limit=limit, sort_by=sort_by
        )

    def shorts(self, channel: str,
               limit: Optional[int] = None,
               use_scrapetube: bool = False) -> List[Dict[str, Any]]:
        """
        Get shorts from a channel.

        Args:
            channel: Channel URL, handle, or ID
            limit: Maximum shorts to return
            use_scrapetube: Use scrapetube for unlimited results

        Returns:
            List of shorts info dicts
        """
        if use_scrapetube:
            try:
                from .handlers.scrapetube_handler import ScrapeTubeHandler
                handler = ScrapeTubeHandler()
                return handler.get_channel_shorts(channel, limit=limit)
            except ImportError:
                if self._toolkit.verbose:
                    print("⚠️ scrapetube not installed. Using pytubefix.")

        return self._toolkit.pytubefix.get_channel_videos(
            channel, content_type='shorts', limit=limit
        )

    def streams(self, channel: str,
                limit: Optional[int] = None,
                use_scrapetube: bool = False) -> List[Dict[str, Any]]:
        """
        Get live streams from a channel.

        Args:
            channel: Channel URL, handle, or ID
            limit: Maximum streams to return
            use_scrapetube: Use scrapetube for unlimited results

        Returns:
            List of stream info dicts
        """
        if use_scrapetube:
            try:
                from .handlers.scrapetube_handler import ScrapeTubeHandler
                handler = ScrapeTubeHandler()
                return handler.get_channel_streams(channel, limit=limit)
            except ImportError:
                if self._toolkit.verbose:
                    print("⚠️ scrapetube not installed. Using pytubefix.")

        return self._toolkit.pytubefix.get_channel_videos(
            channel, content_type='live', limit=limit
        )

    def all_videos(self, channel: str,
                   content_type: str = 'videos') -> List[Dict[str, Any]]:
        """
        Get ALL videos from a channel (unlimited) using scrapetube.

        Args:
            channel: Channel URL, handle, or ID
            content_type: 'videos', 'shorts', or 'streams'

        Returns:
            List of all video info dicts

        Raises:
            ImportError: If scrapetube is not installed
        """
        try:
            from .handlers.scrapetube_handler import ScrapeTubeHandler
            handler = ScrapeTubeHandler()

            if content_type == 'videos':
                return handler.get_channel_videos(channel, limit=None)
            elif content_type == 'shorts':
                return handler.get_channel_shorts(channel, limit=None)
            elif content_type == 'streams':
                return handler.get_channel_streams(channel, limit=None)
            else:
                raise ValueError(f"Invalid content_type: {content_type}")

        except ImportError:
            raise ImportError(
                "scrapetube is required for unlimited channel videos. "
                "Install with: pip install youtube-toolkit[scrapers]"
            )

    def playlists(self, channel: str,
                  limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Get playlists from a channel.

        Args:
            channel: Channel URL, handle, or ID
            limit: Maximum playlists to return

        Returns:
            List of playlist info dicts
        """
        return self._toolkit.pytubefix.get_channel_videos(
            channel, content_type='playlists', limit=limit
        )


class PlaylistGetAPI:
    """Sub-API for playlist-related get operations."""

    def __init__(self, parent: 'GetAPI'):
        self._parent = parent
        self._toolkit = parent._toolkit

    def __call__(self, url: str) -> Dict[str, Any]:
        """
        Get playlist information.

        Args:
            url: Playlist URL

        Returns:
            Playlist metadata dict
        """
        return self._toolkit.pytubefix.get_playlist_info(url)

    def urls(self, url: str) -> List[str]:
        """
        Get all video URLs from a playlist.

        Args:
            url: Playlist URL

        Returns:
            List of video URLs
        """
        return self._toolkit.pytubefix.get_playlist_urls(url)

    def videos(self, url: str,
               limit: Optional[int] = None,
               use_scrapetube: bool = False) -> List[Dict[str, Any]]:
        """
        Get video details from a playlist.

        Args:
            url: Playlist URL
            limit: Maximum videos to return
            use_scrapetube: Use scrapetube for scraping

        Returns:
            List of video info dicts
        """
        if use_scrapetube:
            try:
                from .handlers.scrapetube_handler import ScrapeTubeHandler
                handler = ScrapeTubeHandler()
                return handler.get_playlist_videos(url, limit=limit)
            except ImportError:
                if self._toolkit.verbose:
                    print("⚠️ scrapetube not installed. Getting URLs only.")

        # Fallback: get URLs and fetch info for each
        urls = self.urls(url)
        if limit:
            urls = urls[:limit]
        return urls  # Return URLs, user can fetch details if needed


class CommentsGetAPI:
    """Sub-API for comments-related get operations."""

    def __init__(self, parent: 'GetAPI'):
        self._parent = parent
        self._toolkit = parent._toolkit

    def __call__(self, url: str,
                 limit: int = 100,
                 order: str = 'relevance') -> Dict[str, Any]:
        """
        Get comments from a video.

        Args:
            url: Video URL
            limit: Maximum comments to return
            order: 'relevance' or 'time'

        Returns:
            CommentResult with comments and analytics
        """
        from .core.comments import CommentFilters, CommentOrder

        order_enum = CommentOrder.RELEVANCE if order == 'relevance' else CommentOrder.TIME
        filters = CommentFilters(order=order_enum, max_results=limit)

        return self._toolkit.comments(url, filters=filters)

    def replies(self, url: str, comment_id: str,
                limit: int = 50) -> List[Dict[str, Any]]:
        """
        Get replies to a comment.

        Args:
            url: Video URL
            comment_id: Parent comment ID
            limit: Maximum replies to return

        Returns:
            List of reply dicts
        """
        return self._toolkit.youtube_api.fetch_replies(
            self._toolkit.extract_video_id(url),
            comment_id,
            max_results=limit
        )

    def search(self, url: str, query: str,
               limit: int = 100) -> List[Dict[str, Any]]:
        """
        Search within video comments.

        Args:
            url: Video URL
            query: Search query
            limit: Maximum results

        Returns:
            List of matching comments
        """
        from .core.comments import CommentFilters

        filters = CommentFilters(search_terms=[query], max_results=limit)
        result = self._toolkit.comments(url, filters=filters)
        return result.comments if hasattr(result, 'comments') else []


class GetAPI:
    """
    GET API - Retrieve information from YouTube.

    Usage:
        toolkit.get(url)                    # Smart auto-detect
        toolkit.get.video(url)              # Explicit video info
        toolkit.get.channel("@Fireship")    # Channel info
        toolkit.get.channel.videos(...)     # Channel videos
        toolkit.get.playlist(url)           # Playlist info
        toolkit.get.chapters(url)           # Video chapters
        toolkit.get.transcript(url)         # Video transcript
        toolkit.get.comments(url)           # Video comments
        toolkit.get.captions(url)           # Caption tracks
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit
        self.channel = ChannelGetAPI(self)
        self.playlist = PlaylistGetAPI(self)
        self.comments = CommentsGetAPI(self)

    def __call__(self, url: str,
                 include: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Smart get - auto-detect URL type and return appropriate info.

        Args:
            url: YouTube URL (video, channel, or playlist)
            include: Extra data to include (for videos):
                     ['chapters', 'heatmap', 'key_moments', 'transcript']

        Returns:
            VideoInfo, ChannelInfo, or PlaylistInfo depending on URL type
        """
        # Detect URL type
        url_lower = url.lower()

        if '/playlist' in url_lower or 'list=' in url_lower:
            return self.playlist(url)
        elif '/@' in url_lower or '/channel/' in url_lower or '/c/' in url_lower:
            return self.channel(url)
        elif url.startswith('@'):
            return self.channel(url)
        else:
            return self.video(url, include=include)

    def video(self, url: str,
              include: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        Get video information.

        Args:
            url: Video URL
            include: Extra data to include:
                     ['chapters', 'heatmap', 'key_moments', 'transcript', 'lyrics']

        Returns:
            Video info dict with requested extras
        """
        # Get base info
        info = self._toolkit.pytubefix.get_video_info(url)

        # Add extras if requested
        if include:
            if 'chapters' in include:
                try:
                    info['chapters'] = self._toolkit.pytubefix.get_video_chapters(url)
                except Exception:
                    info['chapters'] = []

            if 'heatmap' in include:
                try:
                    info['heatmap'] = self._toolkit.pytubefix.get_replayed_heatmap(url)
                except Exception:
                    info['heatmap'] = []

            if 'key_moments' in include:
                try:
                    info['key_moments'] = self._toolkit.pytubefix.get_key_moments(url)
                except Exception:
                    info['key_moments'] = []

            if 'transcript' in include:
                try:
                    info['transcript'] = self._toolkit.ytdlp.get_transcript(url)
                except Exception:
                    info['transcript'] = None

            if 'lyrics' in include:
                try:
                    info['lyrics'] = self._toolkit.ytdlp.get_lyrics(url)
                except Exception:
                    info['lyrics'] = None

        return info

    def chapters(self, url: str) -> List[Dict[str, Any]]:
        """
        Get video chapters/timestamps.

        Args:
            url: Video URL

        Returns:
            List of chapter dicts with title, start_seconds, formatted_start
        """
        return self._toolkit.pytubefix.get_video_chapters(url)

    def key_moments(self, url: str) -> List[Dict[str, Any]]:
        """
        Get AI-generated key moments.

        Args:
            url: Video URL

        Returns:
            List of key moment dicts
        """
        return self._toolkit.pytubefix.get_key_moments(url)

    def heatmap(self, url: str) -> List[Dict[str, Any]]:
        """
        Get viewer engagement heatmap (most replayed sections).

        Args:
            url: Video URL

        Returns:
            List of heatmap segments with intensity
        """
        return self._toolkit.pytubefix.get_replayed_heatmap(url)

    def transcript(self, url: str, lang: str = 'en') -> Optional[str]:
        """
        Get auto-generated transcript.

        Args:
            url: Video URL
            lang: Language code

        Returns:
            Transcript text or None
        """
        return self._toolkit.ytdlp.get_transcript(url)

    def lyrics(self, url: str) -> Optional[str]:
        """
        Get lyrics from video (if available in description/metadata).

        Args:
            url: Video URL

        Returns:
            Lyrics text or None
        """
        return self._toolkit.ytdlp.get_lyrics(url)

    def captions(self, url: str) -> Dict[str, Any]:
        """
        Get available caption tracks.

        Args:
            url: Video URL

        Returns:
            CaptionResult with available tracks
        """
        return self._toolkit.captions(url)

    def metadata(self, url: str) -> Dict[str, Any]:
        """
        Get extended metadata via YouTube API.

        Args:
            url: Video URL

        Returns:
            Rich metadata dict
        """
        return self._toolkit.get_rich_metadata(url)


# =============================================================================
# DOWNLOAD API - Save content to disk
# =============================================================================

class DownloadAPI:
    """
    DOWNLOAD API - Save YouTube content to disk.

    Usage:
        toolkit.download(url)                           # Audio (default) -> DownloadResult
        toolkit.download.audio(url, format='mp3')       # Explicit audio -> str (path)
        toolkit.download.video(url, quality='1080p')    # Video -> str (path)
        toolkit.download.captions(url, lang='en')       # Captions -> str (path)
        toolkit.download.thumbnail(url)                 # Thumbnail image -> str (path)
        toolkit.download.playlist(url, type='audio')    # Batch download -> Dict
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def __call__(self, url: str,
                 type: str = 'audio',
                 format: str = 'wav',
                 quality: str = 'best',
                 output_path: Optional[str] = None,
                 bitrate: str = '128k',
                 progress: bool = True,
                 **kwargs):
        """
        Smart download - returns DownloadResult for backward compatibility.

        Args:
            url: Video URL
            type: 'audio' or 'video'
            format: For audio: 'wav', 'mp3', 'm4a'. For video: ignored
            quality: For video: 'best', '720p', '1080p', etc.
            output_path: Output directory or file path
            bitrate: Audio bitrate: 'best', '320k', '256k', '192k', '128k'
            progress: Show download progress

        Returns:
            DownloadResult object with file path and metadata
        """
        from .core.download import DownloadResult

        start_time = time.time()
        backend_used = None

        try:
            if type == 'audio':
                file_path = self.audio(
                    url,
                    format=format,
                    output_path=output_path,
                    bitrate=bitrate,
                    progress_callback=progress,
                )
                backend_used = 'pytubefix/yt-dlp'
                result_format = format
                result_quality = bitrate
            elif type == 'video':
                file_path = self.video(
                    url,
                    quality=quality,
                    output_path=output_path,
                    progress_callback=progress,
                )
                backend_used = 'yt-dlp/pytubefix'
                result_format = 'mp4'
                result_quality = quality
            else:
                raise ValueError(f"Invalid type: {type}. Must be 'audio' or 'video'")

            download_time = time.time() - start_time

            # Get file size if file exists
            file_size = None
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)

            return DownloadResult(
                file_path=file_path,
                success=True,
                file_size=file_size,
                download_time=download_time,
                format=result_format,
                quality=result_quality,
                backend_used=backend_used,
            )

        except Exception as e:
            download_time = time.time() - start_time
            return DownloadResult(
                file_path=output_path or '',
                success=False,
                error_message=str(e),
                download_time=download_time,
                backend_used=backend_used,
            )

    def audio(self, url: str,
              format: str = 'mp3',
              output_path: Optional[str] = None,
              bitrate: str = 'best',
              prefer_yt_dlp: bool = False,
              progress_callback: bool = True) -> str:
        """
        Download audio from a video.

        Args:
            url: Video URL
            format: Output format ('mp3', 'wav', 'm4a')
            output_path: Output directory or file path
            bitrate: Audio bitrate ('best', '320k', '256k', '192k', '128k')
            prefer_yt_dlp: Use yt-dlp instead of pytubefix
            progress_callback: Show download progress

        Returns:
            Path to downloaded audio file
        """
        return self._toolkit.download_audio(
            url,
            format=format,
            output_path=output_path,
            bitrate=bitrate,
            prefer_yt_dlp=prefer_yt_dlp,
            progress_callback=progress_callback
        )

    def video(self, url: str,
              quality: str = 'best',
              output_path: Optional[str] = None,
              prefer_yt_dlp: bool = False,
              progress_callback: bool = True) -> str:
        """
        Download video.

        Args:
            url: Video URL
            quality: Video quality ('best', '1080p', '720p', '480p', '360p')
            output_path: Output directory or file path
            prefer_yt_dlp: Use yt-dlp instead of pytubefix
            progress_callback: Show download progress

        Returns:
            Path to downloaded video file
        """
        return self._toolkit.download_video(
            url,
            quality=quality,
            output_path=output_path,
            prefer_yt_dlp=prefer_yt_dlp,
            progress_callback=progress_callback
        )

    def captions(self, url: str,
                 lang: str = 'en',
                 format: str = 'srt',
                 output_path: Optional[str] = None) -> str:
        """
        Download captions/subtitles.

        Args:
            url: Video URL
            lang: Language code ('en', 'es', 'ja', etc.)
            format: Caption format ('srt', 'vtt', 'txt', 'json')
            output_path: Output directory or file path

        Returns:
            Path to downloaded caption file
        """
        return self._toolkit.download_captions(
            url,
            lang=lang,
            format=format,
            output_path=output_path
        )

    def thumbnail(self, url: str,
                  output_path: Optional[str] = None,
                  quality: str = 'maxres') -> str:
        """
        Download video thumbnail.

        Args:
            url: Video URL
            output_path: Output directory or file path
            quality: Thumbnail quality ('maxres', 'high', 'medium', 'default')

        Returns:
            Path to downloaded thumbnail
        """
        import requests
        import os

        video_id = self._toolkit.extract_video_id(url)

        # Thumbnail URL patterns by quality
        quality_urls = {
            'maxres': f'https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg',
            'high': f'https://i.ytimg.com/vi/{video_id}/hqdefault.jpg',
            'medium': f'https://i.ytimg.com/vi/{video_id}/mqdefault.jpg',
            'default': f'https://i.ytimg.com/vi/{video_id}/default.jpg',
        }

        thumb_url = quality_urls.get(quality, quality_urls['high'])

        # Try to get thumbnail, fallback to lower quality if not available
        response = requests.get(thumb_url)
        if response.status_code != 200 and quality == 'maxres':
            thumb_url = quality_urls['high']
            response = requests.get(thumb_url)

        if response.status_code != 200:
            raise RuntimeError(f"Failed to download thumbnail: {response.status_code}")

        # Determine output path
        if output_path is None:
            output_path = f'{video_id}_thumbnail.jpg'
        elif os.path.isdir(output_path):
            output_path = os.path.join(output_path, f'{video_id}_thumbnail.jpg')

        with open(output_path, 'wb') as f:
            f.write(response.content)

        return output_path

    def playlist(self, url: str,
                 type: str = 'audio',
                 format: str = 'mp3',
                 output_path: Optional[str] = None,
                 **kwargs) -> Dict[str, Any]:
        """
        Download all videos from a playlist.

        Args:
            url: Playlist URL
            type: 'audio' or 'video'
            format: Output format
            output_path: Output directory
            **kwargs: Additional options

        Returns:
            Dict with download results and summary
        """
        return self._toolkit.download_playlist_media(
            url,
            media_type=type,
            format=format,
            output_path=output_path,
            **kwargs
        )


# =============================================================================
# SEARCH API - Find content
# =============================================================================

class SearchAPI:
    """
    SEARCH API - Find YouTube content.

    Usage:
        toolkit.search("query")                         # Videos (default) -> SearchResult
        toolkit.search.videos("query", limit=20)        # Explicit videos -> List[Dict]
        toolkit.search.channels("query")                # Channels -> List[Dict]
        toolkit.search.playlists("query")               # Playlists -> List[Dict]
        toolkit.search.with_filters("query", ...)       # Advanced filters -> Dict
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def __call__(self, query: str,
                 max_results: int = 20,
                 filters=None):
        """
        Smart search - returns SearchResult for backward compatibility.

        Args:
            query: Search query
            max_results: Maximum number of results (default: 20)
            filters: Optional SearchFilters for advanced filtering

        Returns:
            SearchResult object containing search results
        """
        from .core.search import SearchResult, SearchFilters, SearchResultItem

        if filters is None:
            filters = SearchFilters()

        filters.max_results = max_results

        # Use existing advanced_search which returns dict
        raw_result = self._toolkit.advanced_search(query, filters, max_results)

        # Convert to SearchResult
        items = []
        raw_items = raw_result.get('items', [])

        for item in raw_items:
            if isinstance(item, SearchResultItem):
                items.append(item)
            elif isinstance(item, dict):
                items.append(SearchResultItem(
                    kind=item.get('kind', 'youtube#video'),
                    etag=item.get('etag', ''),
                    video_id=item.get('video_id', item.get('id', {}).get('videoId', '')),
                    title=item.get('title', item.get('snippet', {}).get('title', '')),
                    description=item.get('description', item.get('snippet', {}).get('description', '')),
                    channel_title=item.get('channel_title', item.get('snippet', {}).get('channelTitle', '')),
                ))

        return SearchResult(
            items=items,
            total_results=raw_result.get('pageInfo', {}).get('totalResults', len(items)),
            query=query,
            filters_applied=filters,
            next_page_token=raw_result.get('nextPageToken'),
            prev_page_token=raw_result.get('prevPageToken'),
        )

    def videos(self, query: str,
               limit: int = 20,
               use_api: bool = False) -> List[Dict[str, Any]]:
        """
        Search for videos.

        Args:
            query: Search query
            limit: Maximum results
            use_api: Use YouTube API (requires API key, uses quota)

        Returns:
            List of video results
        """
        if use_api:
            return self._toolkit.youtube_api.search_videos(query, max_results=limit)

        # Try pytubefix first, then scrapetube
        try:
            results = self._toolkit.pytubefix.search_videos(query, max_results=limit)
            if results:
                return results
        except Exception:
            pass

        # Fallback to scrapetube
        try:
            from .handlers.scrapetube_handler import ScrapeTubeHandler
            handler = ScrapeTubeHandler()
            return handler.search(query, limit=limit)
        except ImportError:
            pass

        return []

    def channels(self, query: str,
                 limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search for channels.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of channel results
        """
        results = self._toolkit.pytubefix.advanced_search(
            query, result_type='channel', max_results=limit
        )
        return results.get('channels', [])

    def playlists(self, query: str,
                  limit: int = 20) -> List[Dict[str, Any]]:
        """
        Search for playlists.

        Args:
            query: Search query
            limit: Maximum results

        Returns:
            List of playlist results
        """
        results = self._toolkit.pytubefix.advanced_search(
            query, result_type='playlist', max_results=limit
        )
        return results.get('playlists', [])

    def with_filters(self, query: str,
                     duration: Optional[str] = None,
                     upload_date: Optional[str] = None,
                     sort_by: Optional[str] = None,
                     features: Optional[List[str]] = None,
                     result_type: str = 'video',
                     max_results: int = 20) -> Dict[str, Any]:
        """
        Search with advanced filters (no API quota).

        Args:
            query: Search query
            duration: 'short' (<4min), 'medium' (4-20min), 'long' (>20min)
            upload_date: 'hour', 'today', 'week', 'month', 'year'
            sort_by: 'relevance', 'date', 'views', 'rating'
            features: ['hd', '4k', 'live', 'cc', 'creative_commons', 'hdr']
            result_type: 'video', 'channel', 'playlist'
            max_results: Maximum results

        Returns:
            Dict with videos, shorts, channels, playlists, completion_suggestions
        """
        return self._toolkit.pytubefix.advanced_search(
            query=query,
            duration=duration,
            upload_date=upload_date,
            sort_by=sort_by,
            features=features,
            result_type=result_type,
            max_results=max_results
        )

    def suggestions(self, query: str) -> List[str]:
        """
        Get search autocomplete suggestions.

        Args:
            query: Partial search query

        Returns:
            List of suggested queries
        """
        results = self._toolkit.pytubefix.advanced_search(query, max_results=1)
        return results.get('completion_suggestions', [])


# ==================== ADVANCED API (v0.5+) ====================

class SponsorBlockAPI:
    """
    SponsorBlock API - Get and handle sponsored segments.

    Usage:
        segments = toolkit.sponsorblock.segments("url")
        toolkit.sponsorblock.download("url", action='remove')
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def segments(self, url: str) -> List[Dict[str, Any]]:
        """
        Get SponsorBlock segments for a video.

        Returns list of segments with:
        - category: 'sponsor', 'selfpromo', 'intro', 'outro', etc.
        - start_time, end_time, duration
        - description, votes

        Args:
            url: YouTube video URL

        Returns:
            List of segment dictionaries
        """
        return self._toolkit.get_sponsorblock_segments(url)

    def download(self, url: str, output_path: str = None,
                 action: str = 'remove',
                 categories: List[str] = None) -> str:
        """
        Download video with SponsorBlock segments handled.

        Args:
            url: YouTube video URL
            output_path: Output directory
            action: 'remove' (cut out), 'mark' (add as chapters)
            categories: Categories to handle. Default: ['sponsor', 'selfpromo', 'intro', 'outro']

        Returns:
            Path to downloaded file
        """
        return self._toolkit.download_with_sponsorblock(
            url, output_path, action, categories
        )


class LiveStreamAPI:
    """
    Live Stream API - Download and manage live streams.

    Usage:
        status = toolkit.live.status("url")
        toolkit.live.download("url", from_start=True)
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def status(self, url: str) -> Dict[str, Any]:
        """
        Get live stream status.

        Returns:
            Dict with is_live, was_live, live_status, release_timestamp
        """
        return self._toolkit.get_live_status(url)

    def download(self, url: str, output_path: str = None,
                 from_start: bool = False,
                 duration: int = None) -> str:
        """
        Download a live stream.

        Args:
            url: YouTube live stream URL
            output_path: Output directory
            from_start: Download from beginning of stream
            duration: Max duration in seconds

        Returns:
            Path to downloaded file
        """
        return self._toolkit.download_live_stream(
            url, output_path, from_start, duration
        )

    def is_live(self, url: str) -> bool:
        """Check if URL is currently live."""
        return self._toolkit.is_live(url)


class ArchiveAPI:
    """
    Archive API - Prevent re-downloads with archive tracking.

    Usage:
        path = toolkit.archive.download("url")  # Skips if already downloaded
        if toolkit.archive.contains("url"):
            print("Already downloaded")
    """

    def __init__(self, toolkit: 'YouTubeToolkit', archive_file: str = None):
        self._toolkit = toolkit
        self._archive_file = archive_file

    def download(self, url: str, output_path: str = None,
                 format: str = 'best') -> Optional[str]:
        """
        Download with archive tracking.

        Args:
            url: YouTube video URL
            output_path: Output directory
            format: Format specification

        Returns:
            Path to file, or None if already in archive
        """
        return self._toolkit.download_with_archive(
            url, output_path, self._archive_file, format
        )

    def contains(self, url: str) -> bool:
        """Check if URL is in archive."""
        if not self._archive_file:
            return False
        return self._toolkit.is_in_archive(url, self._archive_file)

    def set_archive_file(self, path: str):
        """Set the archive file path."""
        self._archive_file = path


class EngagementAPI:
    """
    Engagement API - Get viewer engagement data.

    Usage:
        heatmap = toolkit.engagement.heatmap("url")
        comments = toolkit.engagement.comments("url", max_comments=50)
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def heatmap(self, url: str) -> List[Dict[str, Any]]:
        """
        Get viewer engagement heatmap (most replayed sections).

        Returns list of segments with start_time, end_time, value (intensity 0-1).

        Args:
            url: YouTube video URL

        Returns:
            List of heatmap segments
        """
        return self._toolkit.get_heatmap(url)

    def comments(self, url: str, max_comments: int = 100,
                 sort: str = 'top') -> List[Dict[str, Any]]:
        """
        Get video comments with structured data.

        Args:
            url: YouTube video URL
            max_comments: Maximum comments to retrieve
            sort: 'top' or 'new'

        Returns:
            List of comment dicts with author, text, likes, etc.
        """
        return self._toolkit.get_comments_raw(url, max_comments, sort)

    def key_moments(self, url: str) -> List[Dict[str, Any]]:
        """
        Get AI-generated key moments.

        Args:
            url: YouTube video URL

        Returns:
            List of key moment dicts
        """
        return self._toolkit.get_key_moments(url)


class CookiesAPI:
    """
    Cookies API - Use browser cookies for authentication.

    Usage:
        info = toolkit.cookies.get_video("url", browser='chrome')
        toolkit.cookies.download_audio("url", browser='firefox')
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def get_video(self, url: str, browser: str = 'chrome') -> Dict[str, Any]:
        """
        Get video info using browser cookies.
        Useful for age-restricted or member-only content.

        Args:
            url: YouTube video URL
            browser: 'chrome', 'firefox', 'safari', 'edge', 'brave', etc.

        Returns:
            Video info dictionary
        """
        return self._toolkit.get_video_info_with_cookies(url, browser)

    def supported_browsers(self) -> List[str]:
        """Get list of supported browsers."""
        return self._toolkit.get_supported_browsers()


class SubtitlesAPI:
    """
    Subtitles API - Download and convert subtitles.

    Usage:
        path = toolkit.subtitles.download("url", lang='en')
        converted = toolkit.subtitles.convert("file.srt", to='vtt')
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def download(self, url: str, lang: str = 'en',
                 output_path: str = None) -> str:
        """
        Download subtitles.

        Args:
            url: YouTube video URL
            lang: Language code
            output_path: Output path

        Returns:
            Path to subtitle file
        """
        return self._toolkit.download_subtitles(url, lang, output_path)

    def convert(self, input_path: str, to: str = 'srt') -> str:
        """
        Convert subtitle format.

        Args:
            input_path: Path to subtitle file
            to: Output format ('srt', 'vtt', 'ass', 'json3', 'ttml')

        Returns:
            Path to converted file
        """
        return self._toolkit.convert_subtitles(input_path, to)

    def supported_formats(self) -> List[str]:
        """Get supported subtitle formats."""
        return self._toolkit.get_supported_subtitle_formats()


class ChapterAPI:
    """
    Chapter API - Get and split by chapters.

    Usage:
        chapters = toolkit.chapters.get("url")
        files = toolkit.chapters.split("url", format='mp3')
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def get(self, url: str) -> List[Dict[str, Any]]:
        """
        Get video chapters.

        Returns list with title, start_time, end_time, duration, formatted times.

        Args:
            url: YouTube video URL

        Returns:
            List of chapter dicts
        """
        return self._toolkit.get_chapters(url)

    def split(self, url: str, output_path: str = None,
              format: str = 'mp4') -> List[str]:
        """
        Download and split video by chapters.

        Args:
            url: YouTube video URL
            output_path: Output directory
            format: Output format ('mp4', 'mp3', etc.)

        Returns:
            List of paths to split files
        """
        return self._toolkit.split_by_chapters(url, output_path, format)


class ThumbnailAPI:
    """
    Thumbnail API - Download video thumbnails.

    Usage:
        path = toolkit.thumbnail.download("url")
        path = toolkit.thumbnail.download("url", quality='maxres')
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def download(self, url: str, output_path: str = None,
                 quality: str = 'best') -> str:
        """
        Download video thumbnail.

        Args:
            url: YouTube video URL
            output_path: Output directory
            quality: 'best', 'maxres', 'standard', 'high', 'medium', 'default'

        Returns:
            Path to thumbnail file
        """
        return self._toolkit.download_thumbnail(url, output_path, quality)

    def url(self, url: str, quality: str = 'maxres') -> str:
        """
        Get thumbnail URL without downloading.

        Args:
            url: YouTube video URL
            quality: Thumbnail quality

        Returns:
            Thumbnail URL
        """
        return self._toolkit.get_thumbnail_url(url)


class AudioEnhancedAPI:
    """
    Enhanced Audio API - Download with metadata and artwork.

    Usage:
        path = toolkit.audio_enhanced.download("url")  # With metadata + thumbnail
        path = toolkit.audio_enhanced.download("url", embed_thumbnail=False)
    """

    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit

    def download(self, url: str, output_path: str = None,
                 format: str = 'mp3',
                 embed_thumbnail: bool = True,
                 add_metadata: bool = True) -> str:
        """
        Download audio with embedded metadata and thumbnail.

        Args:
            url: YouTube video URL
            output_path: Output directory
            format: 'mp3', 'm4a', 'opus', 'flac'
            embed_thumbnail: Embed cover art
            add_metadata: Add ID3/metadata tags

        Returns:
            Path to audio file
        """
        return self._toolkit.download_audio_with_metadata(
            url, output_path, format, embed_thumbnail, add_metadata
        )

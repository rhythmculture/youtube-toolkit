"""
Main YouTube Toolkit interface.

This module provides a unified interface that combines all handlers
and implements fallback logic for robust YouTube operations.
"""

from typing import Optional, List, Dict, Any, Union
from .handlers.pytubefix_handler import PyTubeFixHandler
from .handlers.yt_dlp_handler import YTDLPHandler
from .handlers.youtube_api_handler import YouTubeAPIHandler
from .utils.anti_detection import AntiDetectionManager
from .core.video_info import VideoInfo
from .core.download import DownloadResult
from .core.search import SearchResult, SearchFilters, SearchResultItem
from .core.comments import CommentResult, CommentFilters, Comment, CommentAuthor, CommentMetrics, CommentOrder
from .core.captions import CaptionResult, CaptionFilters, CaptionTrack
import os
import time
import warnings


class YouTubeToolkit:
    """
    Main YouTube Toolkit class that combines multiple backends.

    This class orchestrates different handlers to provide robust
    YouTube functionality with automatic fallback.

    Action-Based API (v0.4+):
        toolkit = YouTubeToolkit()

        # GET - Retrieve information
        toolkit.get(url)                          # Smart auto-detect
        toolkit.get.video(url)                    # Video info
        toolkit.get.channel("@Fireship")          # Channel info
        toolkit.get.channel.videos("@Fireship")   # Channel videos
        toolkit.get.chapters(url)                 # Video chapters
        toolkit.get.transcript(url)               # Video transcript

        # DOWNLOAD - Save to disk
        toolkit.download(url)                     # Audio (default)
        toolkit.download.audio(url, format='mp3') # Explicit audio
        toolkit.download.video(url, quality='720p')

        # SEARCH - Find content
        toolkit.search("query")                   # Videos (default)
        toolkit.search.videos("query")
        toolkit.search.with_filters("query", duration='medium')

    Legacy methods are still available for backward compatibility.
    """

    def __init__(self, verbose: bool = False):
        """
        Initialize the YouTube Toolkit.

        Args:
            verbose: Whether to show detailed progress information
        """
        self.verbose = verbose

        # Create ONE anti-detection manager
        self.anti_detection = AntiDetectionManager()

        # Pass anti-detection to handlers that need it (not YouTube API)
        self.pytubefix = PyTubeFixHandler(self.anti_detection)
        self.ytdlp = YTDLPHandler(self.anti_detection)
        # Alias for backward compatibility
        self.yt_dlp = self.ytdlp
        # YouTube API doesn't need anti-detection (it's official)
        self.youtube_api = YouTubeAPIHandler()

        # Initialize Action-Based Sub-APIs (v0.4+)
        from .sub_apis import GetAPI, DownloadAPI, SearchAPI
        self.get = GetAPI(self)
        self.download = DownloadAPI(self)
        self.search = SearchAPI(self)

        # Initialize Advanced Sub-APIs (v0.5+)
        from .sub_apis import (
            SponsorBlockAPI, LiveStreamAPI, ArchiveAPI, EngagementAPI,
            CookiesAPI, SubtitlesAPI, ChapterAPI, ThumbnailAPI, AudioEnhancedAPI
        )
        self.sponsorblock = SponsorBlockAPI(self)
        self.live = LiveStreamAPI(self)
        self.archive = ArchiveAPI(self)
        self.engagement = EngagementAPI(self)
        self.cookies = CookiesAPI(self)
        self.subtitles = SubtitlesAPI(self)
        self.chapters = ChapterAPI(self)
        self.thumbnail = ThumbnailAPI(self)
        self.audio_enhanced = AudioEnhancedAPI(self)
    
    def get_video_info(self, url: str) -> Dict[str, Any]:
        """
        Get video information with automatic fallback.
        
        Tries pytubefix first, then falls back to yt-dlp.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary with video details
            
        Raises:
            RuntimeError: If all methods fail
        """
        # Try pytubefix first (usually most reliable)
        try:
            return self.pytubefix.get_video_info(url)
        except Exception as e:
            print(f"PyTubeFix failed: {e}")
        
        # Fallback to yt-dlp
        try:
            return self.yt_dlp.get_video_info(url)
        except Exception as e:
            print(f"YT-DLP failed: {e}")
        
        # If both fail, raise error
        raise RuntimeError("All video info extraction methods failed")
    
    def download_audio(self, url: str, format: str = 'wav', 
                       progress_callback: bool = True, prefer_yt_dlp: bool = False,
                       output_path: str = None, bitrate: str = '128k') -> str:
        """
        Download audio with automatic fallback.
        
        Args:
            url: YouTube video URL
            format: Audio format ('wav', 'mp3', 'm4a')
            progress_callback: Whether to show download progress
            prefer_yt_dlp: Whether to prefer yt-dlp over pytubefix
            output_path: Custom output path for the audio file. If None, uses default location.
                         For pytubefix: full file path including filename
                         For yt-dlp: directory path (filename auto-generated)
            bitrate: Audio bitrate ('best', '320k', '256k', '192k', '128k', '96k', '64k')
            
        Returns:
            Path to downloaded audio file
        """
        video_id = self.extract_video_id(url)
        
        # Standardize default output path for consistent behavior
        if output_path is None:
            # Get video title for consistent naming
            try:
                # Try to get title from pytubefix first
                yt = self.pytubefix._yt(url)
                title = self.pytubefix.sanitize_path(yt.title.replace(' ', '-'))
            except:
                # Fallback to video ID if title extraction fails
                title = video_id
            
            # Create consistent default path in current working directory
            default_path = os.path.join(os.getcwd(), f'{title}.{format}')
            
            # For pytubefix: use full path, for yt-dlp: use directory only
            pytubefix_path = default_path
            ytdlp_path = os.path.dirname(default_path)
        else:
            pytubefix_path = output_path
            ytdlp_path = output_path
        
        if prefer_yt_dlp:
            # Try yt-dlp first
            try:
                return self.yt_dlp.download_audio(video_id, output_path=ytdlp_path, format=format, progress_callback=progress_callback, bitrate=bitrate)
            except Exception as e:
                print(f"YT-DLP audio download failed: {e}")
                # Fallback to pytubefix
                return self.pytubefix.download_audio(url, output_path=pytubefix_path, format=format, progress_callback=progress_callback, bitrate=bitrate)
        else:
            # Try pytubefix first
            try:
                return self.pytubefix.download_audio(url, output_path=pytubefix_path, format=format, progress_callback=progress_callback, bitrate=bitrate)
            except Exception as e:
                print(f"PyTubeFix audio download failed: {e}")
                # Fallback to yt-dlp
                return self.yt_dlp.download_audio(video_id, output_path=ytdlp_path, format=format, progress_callback=progress_callback, bitrate=bitrate)
    
    def download_video(self, url: str, quality: str = 'best',
                       progress_callback: bool = True, prefer_yt_dlp: bool = True,
                       output_path: str = None) -> str:
        """
        Download video with automatic fallback.

        Args:
            url: YouTube video URL
            quality: Video quality ('best', '720p', '1080p', etc.')
            progress_callback: Whether to show download progress
            prefer_yt_dlp: Whether to prefer yt-dlp over pytubefix (default: True for reliability)
            output_path: Custom output path for the video file. If None, uses default location.
                         For pytubefix: full file path including filename
                         For yt-dlp: directory path (filename auto-generated)

        Returns:
            Path to downloaded video file

        Note:
            yt-dlp is now preferred by default due to better reliability and fewer
            broken pipe errors compared to PyTubeFix's MoviePy+ffmpeg combination.
        """
        video_id = self.extract_video_id(url)
        
        # Standardize default output path for consistent behavior
        if output_path is None:
            # Get video title for consistent naming
            try:
                # Try to get title from pytubefix first
                yt = self.pytubefix._yt(url)
                title = self.pytubefix.sanitize_path(yt.title.replace(' ', '-'))
            except:
                # Fallback to video ID if title extraction fails
                title = video_id
            
            # Create consistent default path in current working directory
            default_path = os.path.join(os.getcwd(), f'{title}.mp4')
            
            # For pytubefix: use full path, for yt-dlp: use directory only
            pytubefix_path = default_path
            ytdlp_path = os.path.dirname(default_path)
        else:
            pytubefix_path = output_path
            ytdlp_path = output_path
        
        # Use verbose setting to control progress display
        effective_progress = progress_callback and self.verbose
        
        if prefer_yt_dlp:
            # Try yt-dlp first
            try:
                if self.verbose:
                    print("🎯 Trying YT-DLP first...")
                return self.yt_dlp.download_video(video_id, output_path=ytdlp_path, quality=quality, progress_callback=effective_progress)
            except Exception as e:
                if self.verbose:
                    print(f"YT-DLP video download failed: {e}")
                    print("🔄 Falling back to PyTubeFix...")
                # Fallback to pytubefix
                return self.pytubefix.download_video(url, output_path=pytubefix_path, quality=quality, progress_callback=effective_progress)
        else:
            # Try pytubefix first
            try:
                if self.verbose:
                    print("🎯 Trying PyTubeFix first (best quality)...")
                return self.pytubefix.download_video(url, output_path=pytubefix_path, quality=quality, progress_callback=effective_progress)
            except Exception as e:
                if self.verbose:
                    print(f"PyTubeFix video download failed: {e}")
                    print("🔄 Falling back to YT-DLP...")
                # Fallback to yt-dlp
                return self.yt_dlp.download_video(video_id, output_path=ytdlp_path, quality=quality, progress_callback=effective_progress)
    
    def get_available_formats(self, url: str) -> Dict[str, Any]:
        """
        Get available download formats.
        
        Tries pytubefix first, then falls back to yt-dlp.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary of available formats
        """
        # Try pytubefix first
        try:
            return self.pytubefix.get_available_formats(url)
        except Exception as e:
            print(f"PyTubeFix formats failed: {e}")
        
        # Fallback to yt-dlp
        try:
            return self.yt_dlp.get_available_formats(url)
        except Exception as e:
            print(f"YT-DLP formats failed: {e}")
        
        # If both fail, return empty dict
        return {}
    
    def extract_video_id(self, url: str) -> str:
        """
        Extract video ID from URL.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Video ID string
        """
        # Try pytubefix method first
        try:
            return self.pytubefix.extract_video_id(url)
        except:
            pass
        
        # Fallback to yt-dlp method
        try:
            return self.yt_dlp.extract_video_id(url)
        except:
            pass
        
        # If both fail, raise error
        raise ValueError(f"Could not extract video ID from URL: {url}")
    
    def get_video_description(self, url: str) -> str:
        """
        Get video description using yt-dlp.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Video description text
        """
        return self.yt_dlp.get_video_description(url)
    
    def test_handlers(self, url: str) -> Dict[str, bool]:
        """
        Test both handlers to see which ones are working.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary with handler status
        """
        results = {}
        
        # Test pytubefix
        try:
            results['pytubefix'] = self.pytubefix.test_connection(url)
        except:
            results['pytubefix'] = False
        
        # Test yt-dlp
        try:
            results['yt_dlp'] = self.yt_dlp.test_connection(url)
        except:
            results['yt_dlp'] = False
        
        # Test YouTube API
        try:
            results['youtube_api'] = self.youtube_api.test_connection(url)
        except:
            results['youtube_api'] = False
        
        return results
    
    def get_rich_metadata(self, url: str) -> Dict[str, Any]:
        """
        Get rich metadata using YouTube API.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary with rich metadata
        """
        return self.youtube_api.fetch_metadata(url)
    
    def get_comments(self, url: str, max_results: int = 100,
                     sort_by: str = 'relevance') -> List[Dict[str, Any]]:
        """
        Get video comments using YouTube API (legacy method for backward compatibility).
        
        Args:
            url: YouTube video URL
            max_results: Maximum number of comments to retrieve
            sort_by: Sort order ('relevance', 'time')
            
        Returns:
            List of comment dictionaries
        """
        return self.youtube_api.get_comments(url, max_results=max_results, sort_by=sort_by)
    
    def advanced_get_comments(self, url: str, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Advanced comment retrieval with comprehensive filtering, pagination, and analytics.
        
        Args:
            url: YouTube video URL
            filters: CommentFilters object or dict with advanced filtering options
            
        Returns:
            Dictionary with comprehensive comment results including analytics
        """
        return self.youtube_api.advanced_fetch_comments(url, filters)
    
    def get_comments_paginated(self, url: str, page_token: Optional[str] = None,
                              max_results: int = 100, order: str = 'relevance') -> Dict[str, Any]:
        """
        Get comments with pagination support.
        
        Args:
            url: YouTube video URL
            page_token: Token for pagination (from previous result)
            max_results: Maximum number of comments per page
            order: Comment order ('relevance', 'time', 'rating')
            
        Returns:
            Dictionary with paginated comment results
        """
        from .core.comments import CommentFilters
        
        filters = CommentFilters(
            order=CommentFilters.Order(order),
            page_token=page_token,
            max_results=max_results
        )
        
        return self.advanced_get_comments(url, filters)
    
    def search_comments(self, url: str, search_term: str, max_results: int = 100) -> Dict[str, Any]:
        """
        Search within video comments.
        
        Args:
            url: YouTube video URL
            search_term: Term to search for in comments
            max_results: Maximum number of comments to retrieve
            
        Returns:
            Dictionary with filtered comment results
        """
        from .core.comments import CommentFilters
        
        filters = CommentFilters(
            search_terms=search_term,
            max_results=max_results
        )
        
        return self.advanced_get_comments(url, filters)
    
    def get_high_engagement_comments(self, url: str, min_likes: int = 10,
                                   max_results: int = 50) -> Dict[str, Any]:
        """
        Get comments with high engagement (likes).
        
        Args:
            url: YouTube video URL
            min_likes: Minimum number of likes required
            max_results: Maximum number of comments to retrieve
            
        Returns:
            Dictionary with high engagement comment results
        """
        from .core.comments import CommentFilters
        
        filters = CommentFilters(
            min_likes=min_likes,
            max_results=max_results,
            order=CommentFilters.Order.RATING
        )
        
        return self.advanced_get_comments(url, filters)
    
    def get_comments_by_author(self, url: str, author_channel_id: str,
                              max_results: int = 100) -> Dict[str, Any]:
        """
        Get comments from a specific author.
        
        Args:
            url: YouTube video URL
            author_channel_id: Channel ID of the author
            max_results: Maximum number of comments to retrieve
            
        Returns:
            Dictionary with author-specific comment results
        """
        from .core.comments import CommentFilters
        
        filters = CommentFilters(
            author_channel_id=author_channel_id,
            max_results=max_results
        )
        
        return self.advanced_get_comments(url, filters)
    
    def get_recent_comments(self, url: str, days_back: int = 7,
                           max_results: int = 100) -> Dict[str, Any]:
        """
        Get recent comments from the last N days.
        
        Args:
            url: YouTube video URL
            days_back: Number of days to look back
            max_results: Maximum number of comments to retrieve
            
        Returns:
            Dictionary with recent comment results
        """
        from .core.comments import CommentFilters
        from datetime import datetime, timedelta
        
        filters = CommentFilters(
            published_after=datetime.now() - timedelta(days=days_back),
            max_results=max_results,
            order=CommentFilters.Order.TIME
        )
        
        return self.advanced_get_comments(url, filters)
    
    def export_comments(self, url: str, format: str = 'json', 
                       output_path: Optional[str] = None, filters: Optional[Dict] = None) -> str:
        """
        Export comments to file (JSON or CSV).
        
        Args:
            url: YouTube video URL
            format: Export format ('json' or 'csv')
            output_path: Output file path (optional)
            filters: Optional comment filters
            
        Returns:
            Path to exported file
        """
        import json
        import csv
        import os
        from datetime import datetime
        
        # Get comments
        results = self.advanced_get_comments(url, filters)
        comments = results.get('comments', [])
        
        if not comments:
            raise ValueError("No comments found to export")
        
        # Generate output path if not provided
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"comments_export_{timestamp}.{format}"
            output_path = os.path.join(os.getcwd(), filename)
        
        if format.lower() == 'json':
            # Export as JSON
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False, default=str)
        
        elif format.lower() == 'csv':
            # Export as CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow([
                    'Comment ID', 'Text', 'Author', 'Published At', 'Likes', 
                    'Replies', 'Channel ID', 'Is Verified', 'Parent ID'
                ])
                
                # Write comment data
                for comment in comments:
                    writer.writerow([
                        comment.get('comment_id', ''),
                        comment.get('text', ''),
                        comment.get('author', {}).get('display_name', ''),
                        comment.get('published_at', ''),
                        comment.get('metrics', {}).get('like_count', 0),
                        comment.get('metrics', {}).get('reply_count', 0),
                        comment.get('author', {}).get('channel_id', ''),
                        comment.get('author', {}).get('is_verified', False),
                        comment.get('parent_id', '')
                    ])
        
        else:
            raise ValueError("Format must be 'json' or 'csv'")
        
        return output_path
    
    def display_comments(self, url: str, top_n: int = 3,
                        sort_by: str = 'relevance') -> None:
        """
        Display top comments for a video.
        
        Args:
            url: YouTube video URL
            top_n: Number of top comments to display
            sort_by: Sort order ('relevance', 'time')
        """
        comments = self.get_comments(url, max_results=top_n, sort_by=sort_by)
        
        if not comments:
            print("No comments found for this video.")
            return
        
        print(f"\n📝 Top {len(comments)} Comments:")
        for i, comment in enumerate(comments, 1):
            author = comment.get('author', 'Unknown')
            text = comment.get('text', 'No text')
            likes = comment.get('like_count', 0)
            print(f"\n{i}. {author} (👍 {likes})")
            print(f"   {text}")
    
    def search_videos(self, query: str, filters: Optional[Dict] = None, max_results: int = 20) -> List[Dict[str, Any]]:
        """
        Search for YouTube videos (legacy method for backward compatibility).
        
        Args:
            query: Search query string
            filters: Optional filters for search results
            max_results: Maximum number of results to return
            
        Returns:
            List of video dictionaries with search results
        """
        results = []
        
        # Try pytubefix first
        try:
            pytube_results = self.pytubefix.search_videos(query, filters, max_results)
            if pytube_results and len(pytube_results) > 0:
                results.extend(pytube_results)
                print(f"✅ PyTubeFix search returned {len(pytube_results)} results")
            else:
                print("⚠️  PyTubeFix search returned no results")
        except Exception as e:
            print(f"PyTubeFix search failed: {e}")
        
        # If PyTubeFix failed or returned no results, try simple search
        if not results:
            try:
                print("🔍 Trying PyTubeFix simple search fallback...")
                simple_results = self.pytubefix.simple_search(query, max_results)
                if simple_results and len(simple_results) > 0:
                    results.extend(simple_results)
                    print(f"✅ PyTubeFix simple search returned {len(simple_results)} results")
                else:
                    print("⚠️  PyTubeFix simple search returned no results")
            except Exception as e:
                print(f"PyTubeFix simple search failed: {e}")
        
        # If we don't have enough results, try YouTube API
        if len(results) < max_results:
            try:
                remaining_count = max_results - len(results)
                print(f"🔍 Trying YouTube API for {remaining_count} more results...")
                api_results = self.youtube_api.search_videos(query, remaining_count)
                if api_results and len(api_results) > 0:
                    results.extend(api_results)
                    print(f"✅ YouTube API search returned {len(api_results)} additional results")
                else:
                    print("⚠️  YouTube API search returned no results")
            except Exception as e:
                print(f"YouTube API search failed: {e}")
        
        # If still no results, try yt-dlp as last resort
        if not results:
            try:
                print("Trying yt-dlp search as fallback...")
                # Note: yt-dlp doesn't have built-in search, but we can try to get video info
                # This is a placeholder for future implementation
                print("yt-dlp search not implemented yet")
            except Exception as e:
                print(f"yt-dlp search failed: {e}")
        
        # Limit results to requested max
        if len(results) > max_results:
            results = results[:max_results]
        
        if not results:
            print("⚠️  All search methods failed. No results found.")
            print("💡 Try:")
            print("   1. Check your internet connection")
            print("   2. Verify the search query is valid")
            print("   3. Check if YouTube API key is set (for enhanced search)")
            print("   4. Try a different search term")
            return []
        
        print(f"🎯 Total search results: {len(results)}")
        return results
    
    def advanced_search(self, query: str, filters: Optional[Dict] = None, max_results: int = 20) -> Dict[str, Any]:
        """
        Advanced search with comprehensive filtering and rich results.
        
        Args:
            query: Search query string
            filters: SearchFilters object or dict with advanced filtering options
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with comprehensive search results including thumbnails, live content, etc.
        """
        from .core.search import SearchFilters
        
        # Convert dict to SearchFilters if needed
        if isinstance(filters, dict):
            filters = SearchFilters(**filters)
        elif filters is None:
            filters = SearchFilters()
        
        # Try YouTube API first for advanced search (most comprehensive)
        try:
            print(f"🔍 Advanced search: '{query}' with {filters.type} type, order: {filters.order}")
            api_results = self.youtube_api.advanced_search(query, filters, max_results)
            
            if api_results and not api_results.get('error'):
                print(f"✅ YouTube API advanced search returned {len(api_results.get('items', []))} results")
                return api_results
            else:
                print(f"⚠️  YouTube API advanced search failed: {api_results.get('error', 'Unknown error')}")
        except Exception as e:
            print(f"YouTube API advanced search failed: {e}")
        
        # Fallback to basic search methods
        print("🔄 Falling back to basic search methods...")
        basic_results = self.search_videos(query, filters.__dict__ if filters else None, max_results)
        
        # Convert basic results to advanced format
        from .core.search import SearchResult, SearchResultItem, Thumbnails, Thumbnail
        from datetime import datetime
        
        items = []
        for result in basic_results:
            try:
                # Parse published date
                published_at = None
                if result.get('publish_date'):
                    try:
                        published_at = datetime.fromisoformat(result['publish_date'].replace('Z', '+00:00'))
                    except:
                        pass
                
                # Create basic thumbnail (we don't have thumbnail data from basic search)
                thumbnails = None
                
                item = SearchResultItem(
                    kind="youtube#video",
                    etag="",
                    video_id=result.get('video_id'),
                    title=result.get('title', ''),
                    description=result.get('description', ''),
                    channel_title=result.get('author', ''),
                    published_at=published_at,
                    thumbnails=thumbnails,
                    live_broadcast_content="none"  # We don't have this info from basic search
                )
                items.append(item)
            except Exception as item_error:
                print(f"Warning: Failed to convert basic result: {item_error}")
                continue
        
        # Create search result
        search_result = SearchResult(
            items=items,
            total_results=len(items),
            query=query,
            filters_applied=filters,
            backend_used='fallback',
            next_page_token=None,
            prev_page_token=None
        )
        
        return search_result.to_dict()
    
    def search_live_content(self, query: str, event_type: str = "live", max_results: int = 20) -> Dict[str, Any]:
        """
        Search specifically for live content (live streams, upcoming broadcasts).
        
        Args:
            query: Search query string
            event_type: Type of live content ('live', 'upcoming', 'completed')
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with live content search results
        """
        from .core.search import SearchFilters
        
        filters = SearchFilters(
            type="video",
            event_type=event_type,
            order="viewCount"  # Sort by current viewers for live content
        )
        
        return self.advanced_search(query, filters, max_results)
    
    def search_by_category(self, query: str, category_name: str, max_results: int = 20) -> Dict[str, Any]:
        """
        Search for videos in a specific YouTube category.
        
        Args:
            query: Search query string
            category_name: YouTube category name (e.g., 'Gaming', 'Music', 'Education')
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with category-filtered search results
        """
        from .core.search import SearchFilters, YOUTUBE_CATEGORIES
        
        category_id = YOUTUBE_CATEGORIES.get(category_name)
        if not category_id:
            available_categories = list(YOUTUBE_CATEGORIES.keys())
            raise ValueError(f"Unknown category '{category_name}'. Available categories: {available_categories}")
        
        filters = SearchFilters(
            type="video",
            video_category_id=category_id
        )
        
        return self.advanced_search(query, filters, max_results)
    
    def search_sponsored_content(self, query: str, max_results: int = 20) -> Dict[str, Any]:
        """
        Search for videos with paid product placements (sponsored content).
        
        Args:
            query: Search query string
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with sponsored content search results
        """
        from .core.search import SearchFilters
        
        filters = SearchFilters(
            type="video",
            video_paid_product_placement="true"
        )
        
        return self.advanced_search(query, filters, max_results)
    
    def search_with_boolean_query(self, boolean_query: str, filters: Optional[Dict] = None, max_results: int = 20) -> Dict[str, Any]:
        """
        Search using Boolean operators (NOT -, OR |).
        
        Args:
            boolean_query: Query string with Boolean operators (e.g., "python -tutorial", "gaming|streaming")
            filters: Optional additional filters
            max_results: Maximum number of results to return
            
        Returns:
            Dictionary with search results
        """
        from .core.search import SearchFilters, BooleanSearchQuery
        
        # Parse Boolean query
        boolean_search = BooleanSearchQuery.from_string(boolean_query)
        processed_query = boolean_search.build_query()
        
        # Apply additional filters
        if isinstance(filters, dict):
            search_filters = SearchFilters(**filters)
        elif filters is None:
            search_filters = SearchFilters()
        else:
            search_filters = filters
        
        return self.advanced_search(processed_query, search_filters, max_results)
    
    def search_paginated(self, query: str, filters: Optional[Dict] = None, 
                        page_token: Optional[str] = None, max_results: int = 20) -> Dict[str, Any]:
        """
        Search with pagination support.
        
        Args:
            query: Search query string
            filters: Optional search filters
            page_token: Token for pagination (from previous search result)
            max_results: Maximum number of results per page
            
        Returns:
            Dictionary with paginated search results
        """
        from .core.search import SearchFilters
        
        if isinstance(filters, dict):
            search_filters = SearchFilters(**filters)
        elif filters is None:
            search_filters = SearchFilters()
        else:
            search_filters = filters
        
        # Add pagination
        search_filters.page_token = page_token
        search_filters.max_results = max_results
        
        return self.advanced_search(query, search_filters, max_results)
    
    def get_search_categories(self) -> Dict[str, str]:
        """
        Get available YouTube categories for filtering.
        
        Returns:
            Dictionary mapping category names to IDs
        """
        from .core.search import YOUTUBE_CATEGORIES
        return YOUTUBE_CATEGORIES.copy()
    
    def get_captions(self, url: str) -> Dict[str, Any]:
        """
        Get available captions/subtitles for a YouTube video.
        
        Args:
            url: YouTube video URL
            
        Returns:
            Dictionary with caption information
        """
        try:
            return self.pytubefix.get_captions(url)
        except Exception as e:
            print(f"PyTubeFix captions failed: {e}")
            return {"error": str(e)}
    
    def download_captions(self, url: str, language_code: str = 'en', output_path: str = None) -> str:
        """
        Download captions with automatic fallback across handlers (legacy method for backward compatibility).
        
        Args:
            url: YouTube video URL
            language_code: Language code (e.g., 'en', 'es', 'fr')
            output_path: Output file path (optional)
            
        Returns:
            Path to downloaded caption file
        """
        # Try PyTubeFix first (most reliable)
        try:
            return self.pytubefix.download_captions(url, language_code, output_path)
        except Exception as e:
            print(f"PyTubeFix captions failed: {e}")
        
        # Try YT-DLP second
        try:
            return self.yt_dlp.download_captions(url, language_code, output_path)
        except Exception as e:
            print(f"YT-DLP captions failed: {e}")
        
        # Try YouTube API last
        try:
            return self.youtube_api.download_captions(url, language_code, output_path)
        except Exception as e:
            print(f"YouTube API captions failed: {e}")
        
        raise RuntimeError("All caption download methods failed")
    
    def list_captions(self, url: str, filters: Optional[Dict] = None) -> Dict[str, Any]:
        """
        List available caption tracks for a video with advanced filtering.
        
        Args:
            url: YouTube video URL
            filters: CaptionFilters object or dict with filtering options
            
        Returns:
            Dictionary with caption track information and analytics
        """
        return self.youtube_api.advanced_list_captions(url, filters)
    
    def advanced_download_captions(self, url: str, language_code: str = 'en',
                                 format: str = 'srt', output_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Advanced caption download with format conversion and analysis.
        
        Args:
            url: YouTube video URL
            language_code: Language code (e.g., 'en', 'es', 'fr')
            format: Output format ('srt', 'vtt', 'txt', 'ttml')
            output_path: Output file path (optional)
            
        Returns:
            Dictionary with download results and analysis
        """
        try:
            # Try YouTube API first (requires OAuth2)
            return self.youtube_api.advanced_download_captions(url, language_code=language_code, format=format, output_path=output_path)
        except Exception as api_error:
            # Fall back to yt-dlp handler
            try:
                print(f"YouTube API failed ({api_error}), falling back to yt-dlp...")
                caption_path = self.yt_dlp.download_captions(url, language_code, output_path)
                
                # Read the downloaded caption content
                with open(caption_path, 'r', encoding='utf-8') as f:
                    raw_content = f.read()
                
                # Convert format if needed
                from youtube_toolkit.core.captions import CaptionFormatConverter
                converted_content = raw_content
                if format.lower() == 'vtt':
                    converted_content = CaptionFormatConverter.srt_to_vtt(raw_content)
                elif format.lower() == 'txt':
                    converted_content = CaptionFormatConverter.srt_to_txt(raw_content)
                
                # Save converted content if different format
                if converted_content != raw_content:
                    output_path = caption_path.replace('.srt', f'.{format}')
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(converted_content)
                    caption_path = output_path
                
                # Basic analysis
                from youtube_toolkit.core.captions import CaptionFormatConverter, CaptionAnalyzer
                cues = CaptionFormatConverter.parse_srt(raw_content)
                analysis = {
                    'total_duration': sum(cue.duration for cue in cues),
                    'word_count': sum(len(cue.text.split()) for cue in cues),
                    'cue_count': len(cues),
                    'average_cue_duration': sum(cue.duration for cue in cues) / len(cues) if cues else 0,
                    'words_per_minute': CaptionAnalyzer.analyze_reading_speed(cues)['average_wpm'],
                    'language_analysis': CaptionAnalyzer.analyze_language(converted_content),
                    'gaps': CaptionAnalyzer.find_gaps(cues)
                }
                
                return {
                    'success': True,
                    'output_path': caption_path,
                    'caption_id': 'yt-dlp-fallback',
                    'language_code': language_code,
                    'format': format,
                    'analysis': analysis,
                    'quota_cost': 0
                }
            except Exception as ytdlp_error:
                return {
                    'success': False,
                    'error': f"YouTube API failed: {api_error}. yt-dlp fallback failed: {ytdlp_error}",
                    'quota_cost': 0
                }
    
    def get_captions_in_format(self, url: str, language_code: str = 'en',
                              format: str = 'vtt') -> str:
        """
        Get captions in specific format (VTT, TXT, etc.).
        
        Args:
            url: YouTube video URL
            language_code: Language code
            format: Output format ('srt', 'vtt', 'txt')
            
        Returns:
            Caption content as string
        """
        result = self.advanced_download_captions(url, language_code, format)
        
        if result.get('success'):
            with open(result['output_path'], 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise RuntimeError(f"Failed to get captions: {result.get('error')}")
    
    def search_captions(self, url: str, search_term: str, language_code: str = 'en') -> List[Dict[str, Any]]:
        """
        Search within caption content.
        
        Args:
            url: YouTube video URL
            search_term: Term to search for in captions
            language_code: Language code
            
        Returns:
            List of matching caption cues with timestamps
        """
        from .core.captions import CaptionFormatConverter
        
        # Download captions
        result = self.advanced_download_captions(url, language_code, 'srt')
        
        if not result.get('success'):
            raise RuntimeError(f"Failed to download captions: {result.get('error')}")
        
        # Parse captions
        if 'content' in result:
            raw_content = result['content'].raw_content
        else:
            # Fallback case - read from file
            with open(result['output_path'], 'r', encoding='utf-8') as f:
                raw_content = f.read()
        
        from youtube_toolkit.core.captions import CaptionFormatConverter
        cues = CaptionFormatConverter.parse_srt(raw_content)
        
        # Search for term
        matching_cues = []
        search_lower = search_term.lower()
        
        for cue in cues:
            if search_lower in cue.text.lower():
                matching_cues.append({
                    'start_time': cue.start_time,
                    'end_time': cue.end_time,
                    'text': cue.text,
                    'formatted_start': cue.formatted_start,
                    'formatted_end': cue.formatted_end
                })
        
        return matching_cues
    
    def get_caption_analytics(self, url: str, language_code: str = 'en') -> Dict[str, Any]:
        """
        Get comprehensive caption analytics.
        
        Args:
            url: YouTube video URL
            language_code: Language code
            
        Returns:
            Dictionary with caption analytics
        """
        result = self.advanced_download_captions(url, language_code, 'srt')
        
        if not result.get('success'):
            raise RuntimeError(f"Failed to download captions: {result.get('error')}")
        
        return result['analysis']
    
    def export_captions(self, url: str, format: str = 'json', 
                       output_path: Optional[str] = None, language_code: str = 'en') -> str:
        """
        Export captions with metadata and analysis.
        
        Args:
            url: YouTube video URL
            format: Export format ('json', 'csv', 'srt', 'vtt', 'txt')
            output_path: Output file path (optional)
            language_code: Language code
            
        Returns:
            Path to exported file
        """
        import json
        import csv
        import os
        from datetime import datetime
        
        # Get caption data
        result = self.advanced_download_captions(url, language_code, 'srt')
        
        if not result.get('success'):
            raise RuntimeError(f"Failed to download captions: {result.get('error')}")
        
        # Generate output path if not provided
        if not output_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"captions_export_{timestamp}.{format}"
            output_path = os.path.join(os.getcwd(), filename)
        
        if format.lower() == 'json':
            # Export as JSON with metadata
            export_data = {
                'video_url': url,
                'language_code': language_code,
                'caption_id': result['caption_id'],
                'analysis': result['analysis'],
                'cues': [
                    {
                        'start_time': cue.start_time,
                        'end_time': cue.end_time,
                        'text': cue.text,
                        'formatted_start': cue.formatted_start,
                        'formatted_end': cue.formatted_end
                    } for cue in result['content'].cues
                ]
            }
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        elif format.lower() == 'csv':
            # Export as CSV
            with open(output_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                
                # Write header
                writer.writerow(['Start Time', 'End Time', 'Duration', 'Text', 'Formatted Start', 'Formatted End'])
                
                # Write cue data
                for cue in result['content'].cues:
                    writer.writerow([
                        cue.start_time,
                        cue.end_time,
                        cue.duration,
                        cue.text,
                        cue.formatted_start,
                        cue.formatted_end
                    ])
        
        elif format.lower() in ['srt', 'vtt', 'txt']:
            # Export in caption format
            caption_result = self.advanced_download_captions(url, language_code, format, output_path)
            if not caption_result.get('success'):
                raise RuntimeError(f"Failed to export captions: {caption_result.get('error')}")
            output_path = caption_result['output_path']
        
        else:
            raise ValueError("Format must be 'json', 'csv', 'srt', 'vtt', or 'txt'")
        
        return output_path
    
    def get_best_caption_track(self, url: str, preferred_language: str = 'en') -> Optional[Dict[str, Any]]:
        """
        Get the best available caption track for a video.
        
        Args:
            url: YouTube video URL
            preferred_language: Preferred language code
            
        Returns:
            Dictionary with best caption track information
        """
        caption_list = self.list_captions(url)
        tracks = caption_list.get('tracks', [])
        
        if not tracks:
            return None
        
        # Find best track using CaptionResult logic
        from .core.captions import CaptionResult
        result = CaptionResult(tracks=tracks)
        best_track = result.get_best_track(preferred_language)
        
        if best_track:
            return {
                'caption_id': best_track.caption_id,
                'language': best_track.language,
                'language_code': best_track.language_code,
                'name': best_track.name,
                'track_type': best_track.track_type.value,
                'status': best_track.status.value,
                'is_auto_generated': best_track.is_auto_generated,
                'is_cc': best_track.is_cc,
                'display_name': best_track.display_name
            }
        
        return None
    
    def get_anti_detection_status(self) -> Dict[str, Any]:
        """Get comprehensive anti-detection status."""
        return {
            'global_status': self.anti_detection.get_status(),
            'handlers': {
                'pytubefix': self.pytubefix.get_anti_detection_status(),
                'yt_dlp': self.yt_dlp.get_anti_detection_status(),
                'youtube_api': {
                    'note': 'Official API - no anti-detection needed',
                    'status': 'active'
                }
            }
        }
    
    def test_anti_detection(self, url: str) -> Dict[str, Any]:
        """Test anti-detection system with a simple request."""
        import time
        
        try:
            print("🧪 Testing anti-detection system...")
            
            # Test each handler with anti-detection
            results = {}
            
            # Test PyTubeFix
            print("  Testing PyTubeFix...")
            start_time = time.time()
            info = self.pytubefix.get_video_info(url)
            pytubefix_time = time.time() - start_time
            results['pytubefix'] = {
                'success': info is not None,
                'time_taken': pytubefix_time,
                'anti_detection_status': self.pytubefix.get_anti_detection_status()
            }
            
            # Test YT-DLP
            print("  Testing YT-DLP...")
            start_time = time.time()
            info = self.yt_dlp.get_video_info(url)
            ytdlp_time = time.time() - start_time
            results['yt_dlp'] = {
                'success': info is not None,
                'time_taken': ytdlp_time,
                'anti_detection_status': self.yt_dlp.get_anti_detection_status()
            }
            
            # Test YouTube API
            print("  Testing YouTube API...")
            start_time = time.time()
            metadata = self.youtube_api.fetch_metadata(url)
            api_time = time.time() - start_time
            results['youtube_api'] = {
                'success': 'error' not in metadata,
                'time_taken': api_time,
                'note': 'Official API - no anti-detection needed'
            }
            
            # Overall status
            results['overall'] = {
                'all_successful': all(r['success'] for r in results.values() if isinstance(r, dict) and 'success' in r),
                'total_time': sum(r['time_taken'] for r in results.values() if isinstance(r, dict) and 'time_taken' in r),
                'global_anti_detection': self.anti_detection.get_status()
            }
            
            print("✅ Anti-detection test completed!")
            return results
            
        except Exception as e:
            print(f"❌ Anti-detection test failed: {e}")
            return {'error': str(e)}

    def test_search(self, query: str = "test") -> Dict[str, Any]:
        """
        Test search functionality across all handlers.
        
        Args:
            query: Test search query
            
        Returns:
            Dictionary with search test results
        """
        print(f"🔍 Testing search functionality with query: '{query}'")
        
        results = {}
        
        # Test PyTubeFix search
        try:
            pytube_results = self.pytubefix.search_videos(query, max_results=3)
            results['pytubefix'] = {
                'success': True,
                'count': len(pytube_results),
                'sample': pytube_results[0] if pytube_results else None
            }
            print(f"✅ PyTubeFix: {len(pytube_results)} results")
        except Exception as e:
            results['pytubefix'] = {
                'success': False,
                'error': str(e)
            }
            print(f"❌ PyTubeFix: {e}")
        
        # Test YouTube API search
        try:
            api_results = self.youtube_api.search_videos(query, max_results=3)
            results['youtube_api'] = {
                'success': True,
                'count': len(api_results),
                'sample': api_results[0] if api_results else None
            }
            print(f"✅ YouTube API: {len(api_results)} results")
        except Exception as e:
            results['youtube_api'] = {
                'success': False,
                'error': str(e)
            }
            print(f"❌ YouTube API: {e}")
        
        # Overall status
        working_handlers = sum(1 for r in results.values() if r.get('success', False))
        results['overall'] = {
            'working_handlers': working_handlers,
            'total_handlers': len(results),
            'all_working': working_handlers == len(results)
        }
        
        print(f"🎯 Search test completed: {working_handlers}/{len(results)} handlers working")
        return results
    
    def get_playlist_urls(self, playlist_url: str) -> List[str]:
        """
        Get video URLs from playlist with automatic fallback.
        
        Args:
            playlist_url: YouTube playlist URL
            
        Returns:
            List of video URLs
        """
        import time
        
        # Try YouTube API first (most reliable)
        try:
            urls = self.youtube_api.get_playlist_urls(playlist_url)
            if urls:
                return urls
        except Exception as e:
            print(f"YouTube API playlist failed: {e}")
        
        # Try PyTubeFix second
        try:
            urls = self.pytubefix.get_playlist_urls(playlist_url)
            if urls:
                return urls
        except Exception as e:
            print(f"PyTubeFix playlist failed: {e}")
        
        # Try YT-DLP last
        try:
            urls = self.yt_dlp.get_playlist_urls(playlist_url)
            if urls:
                return urls
        except Exception as e:
            print(f"YT-DLP playlist failed: {e}")
        
        print("❌ All playlist methods failed")
        return []
    
    def download_playlist_media(self, playlist_url: str, media_type: str = 'audio', 
                               format: str = 'wav', quality: str = 'best',
                               include_captions: bool = False, audio_bitrate: str = '128k') -> Dict[str, Any]:
        """
        Download media from all videos in playlist.
        
        Args:
            playlist_url: YouTube playlist URL
            media_type: 'audio' or 'video'
            format: Audio format ('wav', 'mp3', 'm4a') or video quality ('best', '720p', '1080p')
            quality: Video quality (only used if media_type='video')
            include_captions: Whether to download captions for each video
            audio_bitrate: Audio bitrate ('best', '320k', '256k', '192k', '128k', '96k', '64k') - only used if media_type='audio'
            
        Returns:
            Dictionary with results summary
        """
        import json
        import os
        import time
        from datetime import datetime
        
        # Get playlist info and URLs
        try:
            playlist_info = self.youtube_api.get_playlist_info(playlist_url)
        except:
            playlist_info = {
                'title': 'YouTube Playlist',
                'description': 'Playlist downloaded with YouTube Toolkit'
            }
        
        urls = self.get_playlist_urls(playlist_url)
        if not urls:
            return {'success': False, 'error': 'No videos found in playlist'}
        
        # Create folder structure
        base_dir = os.path.join(os.getcwd(), 'playlist_downloads')
        playlist_dir = os.path.join(base_dir, self._sanitize_filename(playlist_info['title']))
        
        folders = {
            'base': playlist_dir,
            'audio': os.path.join(playlist_dir, 'audio'),
            'video': os.path.join(playlist_dir, 'video'),
            'captions': os.path.join(playlist_dir, 'captions')
        }
        
        # Create directories
        for folder in folders.values():
            os.makedirs(folder, exist_ok=True)
        
        # Initialize metadata
        metadata = {
            'playlist_info': {
                'title': playlist_info['title'],
                'description': playlist_info.get('description', ''),
                'video_count': len(urls),
                'playlist_url': playlist_url,
                'download_date': datetime.now().isoformat(),
                'download_settings': {
                    'media_type': media_type,
                    'format': format,
                    'quality': quality,
                    'include_captions': include_captions
                }
            },
            'videos': [],
            'download_summary': {
                'total_videos': len(urls),
                'successful_downloads': 0,
                'failed_downloads': 0,
                'total_size_mb': 0,
                'download_time_seconds': 0
            }
        }
        
        start_time = time.time()
        
        # Download each video
        for i, url in enumerate(urls, 1):
            try:
                print(f"📥 [{i}/{len(urls)}] Processing...")
                
                # Get video info
                video_info = self.get_video_info(url)
                video_title = self._sanitize_filename(video_info['title'])
                
                # Download main media
                if media_type == 'audio':
                    media_path = self.download_audio(
                        url, 
                        format=format, 
                        output_path=os.path.join(folders['audio'], f"{video_title}.{format}"),
                        bitrate=audio_bitrate
                    )
                else:  # video
                    media_path = self.download_video(
                        url, 
                        quality=quality,
                        output_path=os.path.join(folders['video'], f"{video_title}.mp4")
                    )
                
                # Download captions if requested
                caption_path = None
                if include_captions:
                    try:
                        caption_path = self.download_captions(
                            url, 
                            language_code='en',
                            output_path=os.path.join(folders['captions'], f"{video_title}_en.txt")
                        )
                    except Exception as e:
                        print(f"⚠️  Captions failed: {e}")
                        # Continue without captions rather than failing the whole download
                
                # Update metadata
                video_metadata = {
                    'index': i,
                    'video_id': video_info.get('video_id', ''),
                    'title': video_info['title'],
                    'channel': video_info.get('channel', 'Unknown'),
                    'duration': video_info.get('duration', 0),
                    'views': video_info.get('view_count', 0),
                    'upload_date': video_info.get('upload_date', ''),
                    'download_status': 'success',
                    'files': {
                        'audio': os.path.relpath(media_path, playlist_dir) if media_type == 'audio' else None,
                        'video': os.path.relpath(media_path, playlist_dir) if media_type == 'video' else None,
                        'caption': os.path.relpath(caption_path, playlist_dir) if caption_path else None
                    },
                    'error': None
                }
                
                metadata['videos'].append(video_metadata)
                metadata['download_summary']['successful_downloads'] += 1
                
                print(f"✅ Downloaded: {video_title}")
                
            except Exception as e:
                error_msg = f"Video {i} failed: {e}"
                print(f"❌ {error_msg}")
                
                # Add failed video to metadata
                video_metadata = {
                    'index': i,
                    'video_id': self.extract_video_id(url),
                    'title': f"Video {i}",
                    'channel': 'Unknown',
                    'duration': 0,
                    'views': 0,
                    'upload_date': '',
                    'download_status': 'failed',
                    'files': {'audio': None, 'video': None, 'caption': None},
                    'error': str(e)
                }
                
                metadata['videos'].append(video_metadata)
                metadata['download_summary']['failed_downloads'] += 1
        
        # Calculate final statistics
        end_time = time.time()
        metadata['download_summary']['download_time_seconds'] = end_time - start_time
        
        # Calculate total size
        total_size = 0
        for video in metadata['videos']:
            if video['download_status'] == 'success':
                for file_path in video['files'].values():
                    if file_path and os.path.exists(os.path.join(playlist_dir, file_path)):
                        total_size += os.path.getsize(os.path.join(playlist_dir, file_path))
        
        metadata['download_summary']['total_size_mb'] = round(total_size / (1024 * 1024), 2)
        
        # Save metadata
        metadata_path = os.path.join(playlist_dir, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print(f"\n🎯 Playlist download complete!")
        print(f"   📁 Saved to: {playlist_dir}")
        print(f"   📊 Metadata: {metadata_path}")
        print(f"   ✅ Successful: {metadata['download_summary']['successful_downloads']}/{len(urls)}")
        print(f"   ❌ Failed: {metadata['download_summary']['failed_downloads']}")
        print(f"   💾 Total size: {metadata['download_summary']['total_size_mb']} MB")
        print(f"   ⏱️  Time: {metadata['download_summary']['download_time_seconds']:.1f} seconds")
        
        return {
            'success': True,
            'playlist_dir': playlist_dir,
            'metadata_path': metadata_path,
            'metadata': metadata
        }
    
    def _sanitize_filename(self, filename: str) -> str:
        """Convert filename to safe format for file system."""
        import re
        # Remove/replace invalid characters
        safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
        # Limit length
        return safe_name[:100].strip()

    # =========================================================================
    # CHANNEL SUPPORT (v0.3+)
    # These methods provide channel-related functionality.
    # =========================================================================

    def get_channel_videos(self, channel: str,
                           content_type: str = 'videos',
                           limit: Optional[int] = None,
                           sort_by: str = 'newest',
                           use_scrapetube: bool = False) -> List[Dict[str, Any]]:
        """
        Get videos from a YouTube channel.

        Uses pytubefix by default. Set use_scrapetube=True for unlimited videos
        (requires scrapetube to be installed: pip install youtube-toolkit[scrapers]).

        Args:
            channel: Channel URL (@handle, /channel/ID, or full URL)
            content_type: 'videos', 'shorts', 'live', or 'playlists'
            limit: Maximum number of items (None = all available)
            sort_by: Sort order - 'newest', 'oldest', or 'popular'
            use_scrapetube: Use scrapetube for unlimited results (optional dependency)

        Returns:
            List of video/playlist info dicts

        Example:
            >>> videos = toolkit.get_channel_videos("@Fireship", limit=50)
            >>> shorts = toolkit.get_channel_videos("@Fireship", content_type='shorts')
            >>> # For unlimited videos (requires scrapetube)
            >>> all_videos = toolkit.get_channel_videos("@Fireship", use_scrapetube=True)
        """
        if use_scrapetube:
            # Try scrapetube for unlimited results
            try:
                from .handlers.scrapetube_handler import ScrapeTubeHandler
                scrapetube = ScrapeTubeHandler()

                if content_type == 'videos':
                    return scrapetube.get_channel_videos(channel, limit=limit, sort_by=sort_by)
                elif content_type == 'shorts':
                    return scrapetube.get_channel_shorts(channel, limit=limit)
                elif content_type == 'live':
                    return scrapetube.get_channel_streams(channel, limit=limit)
                else:
                    # Fallback to pytubefix for playlists
                    return self.pytubefix.get_channel_videos(channel, content_type, limit, sort_by)

            except ImportError:
                if self.verbose:
                    print("⚠️ scrapetube not installed. Falling back to pytubefix.")
                    print("   Install with: pip install youtube-toolkit[scrapers]")

        # Use pytubefix (default)
        return self.pytubefix.get_channel_videos(channel, content_type, limit, sort_by)

    def get_channel_info(self, channel_url: str) -> Dict[str, Any]:
        """
        Get channel metadata without API quota.

        Args:
            channel_url: YouTube channel URL (@handle, /channel/ID, or full URL)

        Returns:
            Dict with channel_name, channel_id, description, thumbnail, views, etc.

        Example:
            >>> info = toolkit.get_channel_info("@Fireship")
            >>> print(f"Channel: {info['channel_name']}")
            >>> print(f"Videos: {info['video_count']}")
        """
        return self.pytubefix.get_channel_info(channel_url)

    def get_all_channel_videos(self, channel: str,
                               content_type: str = 'videos') -> List[Dict[str, Any]]:
        """
        Get ALL videos from a channel (unlimited) using scrapetube.

        This method requires scrapetube to be installed and can retrieve
        ALL videos from a channel without the 500 video limit of the API.

        Args:
            channel: Channel URL or identifier
            content_type: 'videos', 'shorts', or 'streams'

        Returns:
            List of all video info dicts

        Raises:
            ImportError: If scrapetube is not installed

        Example:
            >>> # Get ALL videos from a channel (may take time for large channels)
            >>> all_videos = toolkit.get_all_channel_videos("@Fireship")
            >>> print(f"Total videos: {len(all_videos)}")
        """
        try:
            from .handlers.scrapetube_handler import ScrapeTubeHandler
            scrapetube = ScrapeTubeHandler()

            if content_type == 'videos':
                return scrapetube.get_channel_videos(channel, limit=None)
            elif content_type == 'shorts':
                return scrapetube.get_channel_shorts(channel, limit=None)
            elif content_type == 'streams':
                return scrapetube.get_channel_streams(channel, limit=None)
            else:
                raise ValueError(f"Invalid content_type: {content_type}")

        except ImportError:
            raise ImportError(
                "scrapetube is required for unlimited channel videos. "
                "Install with: pip install youtube-toolkit[scrapers]"
            )

    # =========================================================================
    # VIDEO CHAPTERS & ENGAGEMENT (v0.3+)
    # =========================================================================

    def get_video_chapters(self, url: str) -> List[Dict[str, Any]]:
        """
        Get video chapters/timestamps.

        Args:
            url: YouTube video URL

        Returns:
            List of chapter dicts with title, start_seconds, duration, formatted_start

        Example:
            >>> chapters = toolkit.get_video_chapters("https://youtube.com/watch?v=...")
            >>> for ch in chapters:
            ...     print(f"{ch['formatted_start']} - {ch['title']}")
        """
        return self.pytubefix.get_video_chapters(url)

    def get_key_moments(self, url: str) -> List[Dict[str, Any]]:
        """
        Get AI-generated key moments/timestamps.

        Args:
            url: YouTube video URL

        Returns:
            List of key moment dicts with title, start_seconds, duration
        """
        return self.pytubefix.get_key_moments(url)

    def get_replayed_heatmap(self, url: str) -> List[Dict[str, Any]]:
        """
        Get viewer engagement heatmap data (most replayed segments).

        Args:
            url: YouTube video URL

        Returns:
            List of heatmap segments with start_seconds, duration, intensity
        """
        return self.pytubefix.get_replayed_heatmap(url)

    # =========================================================================
    # ADVANCED SEARCH (PYTUBEFIX) (v0.3+)
    # =========================================================================

    def search_with_filters(self, query: str,
                            duration: Optional[str] = None,
                            upload_date: Optional[str] = None,
                            sort_by: Optional[str] = None,
                            features: Optional[List[str]] = None,
                            result_type: str = 'video',
                            max_results: int = 20) -> Dict[str, Any]:
        """
        Search YouTube with native filters (no API quota).

        This uses pytubefix's advanced search with YouTube's native filters.

        Args:
            query: Search query
            duration: 'short' (<4min), 'medium' (4-20min), 'long' (>20min)
            upload_date: 'hour', 'today', 'week', 'month', 'year'
            sort_by: 'relevance', 'date', 'views', 'rating'
            features: List of ['hd', '4k', 'live', 'cc', 'creative_commons', 'hdr', '360', 'vr180']
            result_type: 'video', 'channel', 'playlist'
            max_results: Max results to return

        Returns:
            Dict with videos, shorts, channels, playlists, completion_suggestions

        Example:
            >>> # Find medium-length Python tutorials from this month
            >>> results = toolkit.search_with_filters(
            ...     "python tutorial",
            ...     duration='medium',
            ...     upload_date='month',
            ...     sort_by='views'
            ... )
            >>> for video in results['videos']:
            ...     print(video['title'])
        """
        return self.pytubefix.advanced_search(
            query=query,
            duration=duration,
            upload_date=upload_date,
            sort_by=sort_by,
            features=features,
            result_type=result_type,
            max_results=max_results
        )

    # =========================================================================
    # PLAYLIST INFO (v0.3+)
    # =========================================================================

    def get_playlist_info(self, playlist_url: str) -> Dict[str, Any]:
        """
        Get comprehensive playlist information.

        Args:
            playlist_url: YouTube playlist URL

        Returns:
            Dict with title, description, owner, views, video_count, etc.

        Example:
            >>> info = toolkit.get_playlist_info("https://youtube.com/playlist?list=...")
            >>> print(f"Playlist: {info['title']} ({info['video_count']} videos)")
        """
        return self.pytubefix.get_playlist_info(playlist_url)

    # =========================================================================
    # SCRAPETUBE SEARCH (v0.3+)
    # =========================================================================

    def search_without_api(self, query: str,
                           limit: int = 20,
                           sort_by: str = 'relevance') -> List[Dict[str, Any]]:
        """
        Search YouTube videos without using API quota.

        Uses scrapetube for search. Falls back to pytubefix if scrapetube
        is not installed.

        Args:
            query: Search query
            limit: Maximum results (default: 20)
            sort_by: 'relevance', 'upload_date', 'view_count', 'rating'

        Returns:
            List of video dicts

        Example:
            >>> results = toolkit.search_without_api("python tutorial", limit=10)
            >>> for video in results:
            ...     print(f"{video['title']} - {video['views']} views")
        """
        try:
            from .handlers.scrapetube_handler import ScrapeTubeHandler
            scrapetube = ScrapeTubeHandler()
            return scrapetube.search(query, limit=limit, sort_by=sort_by)

        except ImportError:
            if self.verbose:
                print("⚠️ scrapetube not installed. Using pytubefix search.")
            return self.pytubefix.search_videos(query, max_results=limit)

    # =========================================================================
    # NEW CLEAN API (v0.2+)
    # These methods provide a cleaner interface with proper return types.
    # The old methods above are kept for backward compatibility.
    # =========================================================================

    def get_video(self, url: str) -> VideoInfo:
        """
        Get video information as a VideoInfo object.

        This is the new clean API. Returns a proper dataclass instead of Dict.

        Args:
            url: YouTube video URL

        Returns:
            VideoInfo object with video details

        Raises:
            RuntimeError: If all extraction methods fail

        Example:
            >>> video = toolkit.get_video('https://youtube.com/watch?v=...')
            >>> print(video.title)
            >>> print(video.duration)
        """
        # Get raw dict from existing method
        data = self.get_video_info(url)

        # Convert to VideoInfo dataclass
        return VideoInfo(
            title=data.get('title', ''),
            duration=data.get('duration', 0),
            views=data.get('view_count', 0),
            author=data.get('channel', data.get('author', '')),
            video_id=data.get('video_id', ''),
            url=data.get('video_url', url),
            description=data.get('description'),
            thumbnail=data.get('thumbnail_url'),
            published_date=data.get('upload_date'),
            like_count=data.get('like_count'),
        )

    def download(
        self,
        url: str,
        type: str = 'audio',
        format: str = 'wav',
        quality: str = 'best',
        output_path: Optional[str] = None,
        bitrate: str = '128k',
        progress: bool = True,
    ) -> DownloadResult:
        """
        Download media from YouTube as a DownloadResult object.

        This is the new clean API. Combines audio/video download into one method.

        Args:
            url: YouTube video URL
            type: 'audio' or 'video'
            format: For audio: 'wav', 'mp3', 'm4a'. For video: ignored (always mp4)
            quality: For video: 'best', '720p', '1080p', etc. For audio: ignored
            output_path: Custom output path (optional)
            bitrate: Audio bitrate: 'best', '320k', '256k', '192k', '128k'
            progress: Show download progress

        Returns:
            DownloadResult object with file path and metadata

        Example:
            >>> result = toolkit.download('https://youtube.com/watch?v=...', type='audio')
            >>> print(result.file_path)
            >>> print(result.success)

            >>> result = toolkit.download('https://youtube.com/watch?v=...', type='video', quality='720p')
            >>> if result.success:
            ...     print(f"Downloaded to {result.file_path}")
        """
        start_time = time.time()
        backend_used = None

        try:
            if type == 'audio':
                file_path = self.download_audio(
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
                file_path = self.download_video(
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

    def search(
        self,
        query: str,
        max_results: int = 20,
        filters: Optional[SearchFilters] = None,
    ) -> SearchResult:
        """
        Search YouTube videos and return a SearchResult object.

        This is the new clean API. Returns proper dataclass instead of List[Dict].

        Args:
            query: Search query string
            max_results: Maximum number of results (default: 20)
            filters: Optional SearchFilters for advanced filtering

        Returns:
            SearchResult object containing search results

        Example:
            >>> results = toolkit.search('python tutorial', max_results=10)
            >>> for item in results.items:
            ...     print(item.title)

            >>> # With filters
            >>> from youtube_toolkit import SearchFilters
            >>> filters = SearchFilters(video_duration='short', order='viewCount')
            >>> results = toolkit.search('music', filters=filters)
        """
        if filters is None:
            filters = SearchFilters()

        filters.max_results = max_results

        # Use existing advanced_search which returns dict
        raw_result = self.advanced_search(query, filters, max_results)

        # If already a SearchResult dict format, convert items
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
            total_results=raw_result.get('total_results', len(items)),
            query=query,
            filters_applied=filters,
            backend_used=raw_result.get('backend_used', 'mixed'),
            next_page_token=raw_result.get('next_page_token'),
            prev_page_token=raw_result.get('prev_page_token'),
        )

    def comments(
        self,
        url: str,
        max_results: int = 100,
        filters: Optional[CommentFilters] = None,
    ) -> CommentResult:
        """
        Get video comments as a CommentResult object.

        This is the new clean API. Returns proper dataclass instead of Dict/List.

        Args:
            url: YouTube video URL
            max_results: Maximum number of comments (default: 100)
            filters: Optional CommentFilters for advanced filtering

        Returns:
            CommentResult object containing comments and analytics

        Example:
            >>> result = toolkit.comments('https://youtube.com/watch?v=...')
            >>> print(f"Total comments: {result.total_results}")
            >>> for comment in result.comments:
            ...     print(f"{comment.author.display_name}: {comment.text}")

            >>> # With filters
            >>> from youtube_toolkit import CommentFilters, CommentOrder
            >>> filters = CommentFilters(order=CommentOrder.TIME, min_likes=10)
            >>> result = toolkit.comments(url, filters=filters)
        """
        if filters is None:
            filters = CommentFilters(max_results=max_results)
        else:
            filters.max_results = max_results

        # Use existing advanced_get_comments
        raw_result = self.advanced_get_comments(url, filters)

        # Convert raw comments to Comment objects
        comments = []
        raw_comments = raw_result.get('comments', [])

        for raw in raw_comments:
            if isinstance(raw, Comment):
                comments.append(raw)
            elif isinstance(raw, dict):
                author_data = raw.get('author', {})
                metrics_data = raw.get('metrics', {})

                author = CommentAuthor(
                    display_name=author_data.get('display_name', 'Unknown'),
                    channel_id=author_data.get('channel_id'),
                    profile_image_url=author_data.get('profile_image_url'),
                    is_verified=author_data.get('is_verified', False),
                    is_channel_owner=author_data.get('is_channel_owner', False),
                )

                metrics = CommentMetrics(
                    like_count=metrics_data.get('like_count', 0),
                    reply_count=metrics_data.get('reply_count', 0),
                )

                from datetime import datetime
                published_at = raw.get('published_at')
                if isinstance(published_at, str):
                    try:
                        published_at = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
                    except:
                        published_at = datetime.now()
                elif not isinstance(published_at, datetime):
                    published_at = datetime.now()

                comments.append(Comment(
                    comment_id=raw.get('comment_id', ''),
                    text=raw.get('text', ''),
                    author=author,
                    published_at=published_at,
                    metrics=metrics,
                    parent_id=raw.get('parent_id'),
                ))

        return CommentResult(
            comments=comments,
            total_results=raw_result.get('total_results', len(comments)),
            next_page_token=raw_result.get('next_page_token'),
            filters_applied=filters,
            quota_cost=raw_result.get('quota_cost', 1),
        )

    def captions(
        self,
        url: str,
        language: str = 'en',
        filters: Optional[CaptionFilters] = None,
    ) -> CaptionResult:
        """
        Get available captions as a CaptionResult object.

        This is the new clean API. Returns proper dataclass instead of Dict.

        Args:
            url: YouTube video URL
            language: Preferred language code (default: 'en')
            filters: Optional CaptionFilters for advanced filtering

        Returns:
            CaptionResult object containing available caption tracks

        Example:
            >>> result = toolkit.captions('https://youtube.com/watch?v=...')
            >>> for track in result.tracks:
            ...     print(f"{track.language}: {track.name}")

            >>> # Get best track for English
            >>> best = result.get_best_track('en')
            >>> if best:
            ...     print(f"Best track: {best.name}")
        """
        # Use existing list_captions
        raw_result = self.list_captions(url, filters)

        # Convert to CaptionResult
        tracks = []
        raw_tracks = raw_result.get('tracks', [])

        for raw in raw_tracks:
            if isinstance(raw, CaptionTrack):
                tracks.append(raw)
            # If it's a dict, the list_captions should have already converted it

        return CaptionResult(
            tracks=tracks,
            quota_cost=raw_result.get('quota_cost', 0),
        )

    def playlist(self, url: str) -> List[str]:
        """
        Get all video URLs from a playlist.

        This is the new clean API. Alias for get_playlist_urls.

        Args:
            url: YouTube playlist URL

        Returns:
            List of video URLs

        Example:
            >>> urls = toolkit.playlist('https://youtube.com/playlist?list=...')
            >>> print(f"Found {len(urls)} videos")
            >>> for video_url in urls:
            ...     video = toolkit.get_video(video_url)
            ...     print(video.title)
        """
        return self.get_playlist_urls(url)

    # ==================== v0.5 FEATURES ====================

    # --- SponsorBlock Methods ---

    def get_sponsorblock_segments(self, url: str) -> List[Dict[str, Any]]:
        """
        Get SponsorBlock segments for a video.

        SponsorBlock is a crowdsourced database of sponsored segments, intros,
        outros, and other skippable content.

        Args:
            url: YouTube video URL

        Returns:
            List of segment dictionaries with category, start/end times, etc.
        """
        return self.yt_dlp.get_sponsorblock_segments(url)

    def download_with_sponsorblock(self, url: str, output_path: str = None,
                                   action: str = 'remove',
                                   categories: List[str] = None) -> str:
        """
        Download video with SponsorBlock segments handled.

        Args:
            url: YouTube video URL
            output_path: Output directory
            action: 'remove' (cut out segments), 'mark' (add as chapters)
            categories: Categories to handle. Default: ['sponsor', 'selfpromo', 'intro', 'outro']

        Returns:
            Path to downloaded file
        """
        return self.yt_dlp.download_with_sponsorblock(url, output_path, action, categories)

    # --- Live Stream Methods ---

    def get_live_status(self, url: str) -> Dict[str, Any]:
        """
        Get live stream status information.

        Args:
            url: YouTube video URL

        Returns:
            Dictionary with is_live, was_live, live_status, release_timestamp, etc.
        """
        return self.yt_dlp.get_live_status(url)

    def download_live_stream(self, url: str, output_path: str = None,
                             from_start: bool = False,
                             duration: int = None) -> str:
        """
        Download a live stream or live stream archive.

        Args:
            url: YouTube live stream URL
            output_path: Output directory
            from_start: If True, download from the beginning of the stream
            duration: Maximum duration to download in seconds (None for full stream)

        Returns:
            Path to downloaded file
        """
        return self.yt_dlp.download_live_stream(url, output_path, from_start, duration)

    def is_live(self, url: str) -> bool:
        """
        Check if a video is currently live streaming.

        Args:
            url: YouTube video URL

        Returns:
            True if currently live, False otherwise
        """
        status = self.get_live_status(url)
        return status.get('is_live', False)

    # --- Archive Methods ---

    def download_with_archive(self, url: str, output_path: str = None,
                              archive_file: str = None,
                              format: str = 'best') -> Optional[str]:
        """
        Download video with archive tracking to prevent re-downloads.

        Args:
            url: YouTube video URL
            output_path: Output directory
            archive_file: Path to archive file (default: 'downloaded.txt' in output_path)
            format: Format specification

        Returns:
            Path to downloaded file, or None if already in archive
        """
        return self.yt_dlp.download_with_archive(url, output_path, archive_file, format)

    def is_in_archive(self, url: str, archive_file: str) -> bool:
        """
        Check if a video is already in the download archive.

        Args:
            url: YouTube video URL
            archive_file: Path to archive file

        Returns:
            True if video is in archive, False otherwise
        """
        return self.yt_dlp.is_in_archive(url, archive_file)

    # --- Engagement Methods ---

    def get_heatmap(self, url: str) -> List[Dict[str, Any]]:
        """
        Get viewer engagement heatmap data (most replayed sections).

        Args:
            url: YouTube video URL

        Returns:
            List of heatmap segments with start_time, end_time, and value (intensity)
        """
        # Try yt-dlp first (more reliable for heatmap)
        try:
            result = self.yt_dlp.get_heatmap(url)
            if result:
                return result
        except Exception:
            pass

        # Fallback to pytubefix
        try:
            return self.pytubefix.get_replayed_heatmap(url)
        except Exception:
            return []

    def get_comments_raw(self, url: str, max_comments: int = 100,
                         sort: str = 'top') -> List[Dict[str, Any]]:
        """
        Extract comments from a YouTube video using yt-dlp.

        Args:
            url: YouTube video URL
            max_comments: Maximum number of comments to retrieve
            sort: Sort order ('top' or 'new')

        Returns:
            List of comment dictionaries with author, text, likes, replies, etc.
        """
        return self.yt_dlp.get_comments(url, max_comments, sort)

    # --- Cookies Methods ---

    def get_video_info_with_cookies(self, url: str, browser: str = 'chrome') -> Dict[str, Any]:
        """
        Get video info using cookies extracted from browser.
        Useful for age-restricted or member-only content.

        Args:
            url: YouTube video URL
            browser: Browser to extract cookies from ('chrome', 'firefox', 'safari', 'edge', etc.)

        Returns:
            Dictionary with video details
        """
        return self.yt_dlp.get_video_info_with_cookies_from_browser(url, browser)

    def get_supported_browsers(self) -> List[str]:
        """
        Get list of supported browsers for cookie extraction.

        Returns:
            List of supported browser names
        """
        return ['chrome', 'firefox', 'safari', 'edge', 'opera', 'brave', 'chromium', 'vivaldi']

    # --- Subtitles Methods ---

    def download_subtitles(self, url: str, lang: str = 'en',
                           output_path: str = None) -> str:
        """
        Download subtitles for a video.

        Args:
            url: YouTube video URL
            lang: Language code
            output_path: Output path

        Returns:
            Path to subtitle file
        """
        return self.yt_dlp.download_captions(url, lang, output_path)

    def convert_subtitles(self, input_path: str, output_format: str = 'srt') -> str:
        """
        Convert subtitle file to different format.

        Args:
            input_path: Path to input subtitle file
            output_format: Output format ('srt', 'vtt', 'ass', 'json3', 'ttml')

        Returns:
            Path to converted subtitle file
        """
        return self.yt_dlp.convert_subtitles(input_path, output_format)

    def get_supported_subtitle_formats(self) -> List[str]:
        """
        Get supported subtitle formats for conversion.

        Returns:
            List of supported format names
        """
        return ['srt', 'vtt', 'ass', 'json3', 'ttml']

    # --- Chapters Methods ---

    def get_chapters(self, url: str) -> List[Dict[str, Any]]:
        """
        Get video chapters with automatic fallback.

        Args:
            url: YouTube video URL

        Returns:
            List of chapters with title, start_time, end_time, duration, formatted times
        """
        # Try pytubefix first
        try:
            result = self.pytubefix.get_video_chapters(url)
            if result:
                return result
        except Exception:
            pass

        # Fallback to yt-dlp
        return self.yt_dlp.get_chapters(url)

    def split_by_chapters(self, url: str, output_path: str = None,
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
        return self.yt_dlp.split_by_chapters(url, output_path, format)

    # --- Thumbnail Methods ---

    def download_thumbnail(self, url: str, output_path: str = None,
                           quality: str = 'best') -> str:
        """
        Download video thumbnail.

        Args:
            url: YouTube video URL
            output_path: Output directory or file path
            quality: Thumbnail quality ('best', 'maxres', 'standard', 'high', 'medium', 'default')

        Returns:
            Path to downloaded thumbnail file
        """
        return self.yt_dlp.download_thumbnail(url, output_path, quality)

    def get_thumbnail_url(self, url: str) -> str:
        """
        Get thumbnail URL without downloading.

        Args:
            url: YouTube video URL

        Returns:
            Thumbnail URL
        """
        info = self.yt_dlp.get_video_info(url)
        return info.get('thumbnail_url', '')

    # --- Enhanced Audio Methods ---

    def download_audio_with_metadata(self, url: str, output_path: str = None,
                                     format: str = 'mp3',
                                     embed_thumbnail: bool = True,
                                     add_metadata: bool = True) -> str:
        """
        Download audio with embedded metadata and thumbnail.

        Args:
            url: YouTube video URL
            output_path: Output directory
            format: Audio format ('mp3', 'm4a', 'opus', 'flac')
            embed_thumbnail: Whether to embed thumbnail in audio file
            add_metadata: Whether to add metadata tags

        Returns:
            Path to downloaded audio file
        """
        return self.yt_dlp.download_audio_with_metadata(
            url, output_path, format, embed_thumbnail, add_metadata
        )

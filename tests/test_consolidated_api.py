"""
Tests for the consolidated v1.0 API structure.

This tests the 5 core Sub-APIs:
- GetAPI
- DownloadAPI
- SearchAPI
- AnalyzeAPI
- StreamAPI
"""

import pytest
from unittest.mock import patch, MagicMock


class TestCoreSubAPIs:
    """Tests for the 5 core Sub-API structure."""

    def test_get_api_exists(self):
        """Test that get API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get')
        assert callable(toolkit.get)

    def test_download_api_exists(self):
        """Test that download API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'download')
        assert callable(toolkit.download)

    def test_search_api_exists(self):
        """Test that search API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'search')
        assert callable(toolkit.search)

    def test_analyze_api_exists(self):
        """Test that analyze API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'analyze')
        assert callable(toolkit.analyze)

    def test_stream_api_exists(self):
        """Test that stream API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'stream')
        assert callable(toolkit.stream)


class TestGetAPI:
    """Tests for GetAPI methods."""

    def test_get_video_method(self):
        """Test that get.video exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'video')

    def test_get_channel_exists(self):
        """Test that get.channel exists and is callable."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'channel')
        assert callable(toolkit.get.channel)

    def test_get_channel_videos_exists(self):
        """Test that get.channel.videos exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get.channel, 'videos')

    def test_get_channel_playlists_exists(self):
        """Test that get.channel.playlists exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get.channel, 'playlists')

    def test_get_playlist_exists(self):
        """Test that get.playlist exists and is callable."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'playlist')
        assert callable(toolkit.get.playlist)

    def test_get_comments_exists(self):
        """Test that get.comments exists and is callable."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'comments')
        assert callable(toolkit.get.comments)

    def test_get_chapters_method(self):
        """Test that get.chapters exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'chapters')

    def test_get_heatmap_method(self):
        """Test that get.heatmap exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'heatmap')

    def test_get_keywords_method(self):
        """Test that get.keywords exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'keywords')

    def test_get_formats_method(self):
        """Test that get.formats exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'formats')

    def test_get_restriction_method(self):
        """Test that get.restriction exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'restriction')

    def test_get_transcript_method(self):
        """Test that get.transcript exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'transcript')

    def test_get_captions_method(self):
        """Test that get.captions exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'captions')

    def test_get_embed_url_method(self):
        """Test that get.embed_url exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.get, 'embed_url')


class TestDownloadAPI:
    """Tests for DownloadAPI methods."""

    def test_download_audio_method(self):
        """Test that download.audio exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'audio')

    def test_download_video_method(self):
        """Test that download.video exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'video')

    def test_download_captions_method(self):
        """Test that download.captions exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'captions')

    def test_download_thumbnail_method(self):
        """Test that download.thumbnail exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'thumbnail')

    def test_download_playlist_method(self):
        """Test that download.playlist exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'playlist')

    def test_download_shorts_method(self):
        """Test that download.shorts exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'shorts')

    def test_download_live_method(self):
        """Test that download.live exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'live')

    def test_download_with_sponsorblock_method(self):
        """Test that download.with_sponsorblock exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'with_sponsorblock')

    def test_download_with_metadata_method(self):
        """Test that download.with_metadata exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'with_metadata')

    def test_download_with_filter_method(self):
        """Test that download.with_filter exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'with_filter')

    def test_download_with_archive_method(self):
        """Test that download.with_archive exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'with_archive')

    def test_download_with_cookies_method(self):
        """Test that download.with_cookies exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.download, 'with_cookies')


class TestSearchAPI:
    """Tests for SearchAPI methods."""

    def test_search_videos_method(self):
        """Test that search.videos exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'videos')

    def test_search_channels_method(self):
        """Test that search.channels exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'channels')

    def test_search_playlists_method(self):
        """Test that search.playlists exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'playlists')

    def test_search_with_filters_method(self):
        """Test that search.with_filters exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'with_filters')

    def test_search_suggestions_method(self):
        """Test that search.suggestions exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'suggestions')

    def test_search_trending_exists(self):
        """Test that search.trending exists and is callable."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'trending')
        assert callable(toolkit.search.trending)

    def test_search_trending_by_category_method(self):
        """Test that search.trending.by_category exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search.trending, 'by_category')

    def test_search_categories_method(self):
        """Test that search.categories exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'categories')

    def test_search_regions_method(self):
        """Test that search.regions exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'regions')

    def test_search_languages_method(self):
        """Test that search.languages exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.search, 'languages')


class TestAnalyzeAPI:
    """Tests for AnalyzeAPI methods."""

    def test_analyze_metadata_method(self):
        """Test that analyze.metadata exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.analyze, 'metadata')

    def test_analyze_engagement_method(self):
        """Test that analyze.engagement exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.analyze, 'engagement')

    def test_analyze_comments_method(self):
        """Test that analyze.comments exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.analyze, 'comments')

    def test_analyze_captions_method(self):
        """Test that analyze.captions exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.analyze, 'captions')

    def test_analyze_sponsorblock_method(self):
        """Test that analyze.sponsorblock exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.analyze, 'sponsorblock')

    def test_analyze_channel_method(self):
        """Test that analyze.channel exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.analyze, 'channel')

    def test_analyze_filesize_method(self):
        """Test that analyze.filesize exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.analyze, 'filesize')


class TestStreamAPI:
    """Tests for StreamAPI methods."""

    def test_stream_audio_method(self):
        """Test that stream.audio exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.stream, 'audio')

    def test_stream_video_method(self):
        """Test that stream.video exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.stream, 'video')

    def test_stream_live_exists(self):
        """Test that stream.live exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.stream, 'live')

    def test_stream_live_status_method(self):
        """Test that stream.live.status exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.stream.live, 'status')

    def test_stream_live_is_live_method(self):
        """Test that stream.live.is_live exists."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit.stream.live, 'is_live')


class TestLegacyAPIsRemoved:
    """Tests to verify legacy APIs have been removed in v1.0 consolidation."""

    def test_no_sponsorblock_api(self):
        """Test that legacy sponsorblock API is removed (use analyze.sponsorblock)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'sponsorblock')

    def test_no_engagement_api(self):
        """Test that legacy engagement API is removed (use analyze.engagement)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'engagement')

    def test_no_live_api(self):
        """Test that legacy live API is removed (use stream.live)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'live')

    def test_no_archive_api(self):
        """Test that legacy archive API is removed (use download.with_archive)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'archive')

    def test_no_cookies_api(self):
        """Test that legacy cookies API is removed (use download.with_cookies)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'cookies')

    def test_no_subtitles_api(self):
        """Test that legacy subtitles API is removed (use download.captions)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'subtitles')

    def test_no_chapters_api(self):
        """Test that legacy chapters API is removed (use get.chapters)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'chapters')

    def test_no_thumbnail_api(self):
        """Test that legacy thumbnail API is removed (use download.thumbnail)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'thumbnail')

    def test_no_filter_api(self):
        """Test that legacy filter API is removed (use download.with_filter)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'filter')

    def test_no_metadata_api(self):
        """Test that legacy metadata API is removed (use analyze.metadata)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'metadata')

    def test_no_shorts_api(self):
        """Test that legacy shorts API is removed (use download.shorts)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'shorts')

    def test_no_categories_api(self):
        """Test that legacy categories API is removed (use search.categories)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'categories')

    def test_no_i18n_api(self):
        """Test that legacy i18n API is removed (use search.languages/regions)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'i18n')

    def test_no_trending_api(self):
        """Test that legacy trending API is removed (use search.trending)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'trending')

    def test_no_channel_info_api(self):
        """Test that legacy channel_info API is removed (use analyze.channel)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'channel_info')

    def test_no_buffer_api(self):
        """Test that old buffer API doesn't exist."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'buffer')

    def test_no_filesize_api(self):
        """Test that old filesize API doesn't exist (use analyze.filesize)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'filesize')

    def test_no_video_info_api(self):
        """Test that old video_info API doesn't exist."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'video_info')

    def test_no_channel_playlists_api(self):
        """Test that old channel_playlists API doesn't exist."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'channel_playlists')

    def test_no_suggestions_api(self):
        """Test that old suggestions API doesn't exist (use search.suggestions)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'suggestions')

    def test_no_subscriptions_api(self):
        """Test that legacy subscriptions API is removed."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'subscriptions')

    def test_no_activities_api(self):
        """Test that legacy activities API is removed."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'activities')

    def test_no_sections_api(self):
        """Test that legacy sections API is removed."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'sections')

    def test_no_audio_enhanced_api(self):
        """Test that legacy audio_enhanced API is removed (use download.with_metadata)."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert not hasattr(toolkit, 'audio_enhanced')


class TestMethodDelegation:
    """Tests for method delegation to handlers."""

    def test_get_heatmap_delegates_to_pytubefix(self):
        """Test that get.heatmap delegates to pytubefix handler."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.pytubefix, 'get_replayed_heatmap') as mock:
            mock.return_value = [{'start': 0, 'end': 10, 'intensity': 0.8}]
            result = toolkit.get.heatmap('https://youtube.com/watch?v=test')
            assert result == [{'start': 0, 'end': 10, 'intensity': 0.8}]
            mock.assert_called_once()

    def test_analyze_sponsorblock_delegates_to_ytdlp(self):
        """Test that analyze.sponsorblock delegates to ytdlp handler."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.ytdlp, 'get_sponsorblock_segments') as mock:
            mock.return_value = [{'category': 'sponsor', 'start': 0, 'end': 30}]
            result = toolkit.analyze.sponsorblock('https://youtube.com/watch?v=test')
            assert result == [{'category': 'sponsor', 'start': 0, 'end': 30}]
            mock.assert_called_once()

    def test_search_suggestions_delegates_to_pytubefix(self):
        """Test that search.suggestions delegates to pytubefix handler."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.pytubefix, 'get_search_suggestions') as mock:
            mock.return_value = ['python tutorial', 'python for beginners']
            result = toolkit.search.suggestions('python')
            assert result == ['python tutorial', 'python for beginners']
            mock.assert_called_once()

    def test_stream_audio_delegates_to_pytubefix(self):
        """Test that stream.audio delegates to pytubefix handler."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.pytubefix, 'stream_to_buffer') as mock:
            mock.return_value = b'audio_data'
            result = toolkit.stream.audio('https://youtube.com/watch?v=test')
            assert result == b'audio_data'
            mock.assert_called_once()

    def test_analyze_filesize_delegates_to_pytubefix(self):
        """Test that analyze.filesize delegates to pytubefix handler."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.pytubefix, 'get_filesize_preview') as mock:
            mock.return_value = {'best_audio': {'filesize_mb': 5.0}}
            result = toolkit.analyze.filesize('https://youtube.com/watch?v=test')
            assert result == {'best_audio': {'filesize_mb': 5.0}}
            mock.assert_called_once()

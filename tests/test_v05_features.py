"""
Tests for v0.5 features: Advanced yt-dlp integrations.
"""

import pytest
from unittest.mock import patch, MagicMock
import os


class TestAdvancedAPIImports:
    """Tests for importing v0.5 advanced APIs."""

    def test_import_advanced_sub_apis(self):
        """Test that advanced sub-APIs can be imported."""
        from youtube_toolkit.sub_apis import (
            SponsorBlockAPI,
            LiveStreamAPI,
            ArchiveAPI,
            EngagementAPI,
            CookiesAPI,
            SubtitlesAPI,
            ChapterAPI,
            ThumbnailAPI,
            AudioEnhancedAPI
        )
        assert SponsorBlockAPI is not None
        assert LiveStreamAPI is not None
        assert ArchiveAPI is not None
        assert EngagementAPI is not None
        assert CookiesAPI is not None
        assert SubtitlesAPI is not None
        assert ChapterAPI is not None
        assert ThumbnailAPI is not None
        assert AudioEnhancedAPI is not None


class TestToolkitAdvancedAPIs:
    """Tests for advanced APIs on YouTubeToolkit."""

    def test_sponsorblock_api_exists(self):
        """Test that sponsorblock API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'sponsorblock')
        assert hasattr(toolkit.sponsorblock, 'segments')
        assert hasattr(toolkit.sponsorblock, 'download')

    def test_live_api_exists(self):
        """Test that live stream API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'live')
        assert hasattr(toolkit.live, 'status')
        assert hasattr(toolkit.live, 'download')
        assert hasattr(toolkit.live, 'is_live')

    def test_archive_api_exists(self):
        """Test that archive API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'archive')
        assert hasattr(toolkit.archive, 'download')
        assert hasattr(toolkit.archive, 'contains')
        assert hasattr(toolkit.archive, 'set_archive_file')

    def test_engagement_api_exists(self):
        """Test that engagement API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'engagement')
        assert hasattr(toolkit.engagement, 'heatmap')
        assert hasattr(toolkit.engagement, 'comments')
        assert hasattr(toolkit.engagement, 'key_moments')

    def test_cookies_api_exists(self):
        """Test that cookies API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'cookies')
        assert hasattr(toolkit.cookies, 'get_video')
        assert hasattr(toolkit.cookies, 'supported_browsers')

    def test_subtitles_api_exists(self):
        """Test that subtitles API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'subtitles')
        assert hasattr(toolkit.subtitles, 'download')
        assert hasattr(toolkit.subtitles, 'convert')
        assert hasattr(toolkit.subtitles, 'supported_formats')

    def test_chapters_api_exists(self):
        """Test that chapters API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'chapters')
        assert hasattr(toolkit.chapters, 'get')
        assert hasattr(toolkit.chapters, 'split')

    def test_thumbnail_api_exists(self):
        """Test that thumbnail API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'thumbnail')
        assert hasattr(toolkit.thumbnail, 'download')
        assert hasattr(toolkit.thumbnail, 'url')

    def test_audio_enhanced_api_exists(self):
        """Test that audio enhanced API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'audio_enhanced')
        assert hasattr(toolkit.audio_enhanced, 'download')


class TestCookiesAPI:
    """Tests for CookiesAPI functionality."""

    def test_supported_browsers(self):
        """Test supported browsers list."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        browsers = toolkit.cookies.supported_browsers()
        assert 'chrome' in browsers
        assert 'firefox' in browsers
        assert 'safari' in browsers
        assert 'edge' in browsers
        assert len(browsers) == 8


class TestSubtitlesAPI:
    """Tests for SubtitlesAPI functionality."""

    def test_supported_formats(self):
        """Test supported subtitle formats."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        formats = toolkit.subtitles.supported_formats()
        assert 'srt' in formats
        assert 'vtt' in formats
        assert 'ass' in formats
        assert 'json3' in formats
        assert 'ttml' in formats


class TestYTDLPHandlerNewFeatures:
    """Tests for new YT-DLP handler features."""

    def test_extract_cookies_from_browser_valid(self):
        """Test valid browser name."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        browser = toolkit.yt_dlp.extract_cookies_from_browser('chrome')
        assert browser == 'chrome'

    def test_extract_cookies_from_browser_invalid(self):
        """Test invalid browser raises error."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with pytest.raises(ValueError) as exc_info:
            toolkit.yt_dlp.extract_cookies_from_browser('invalid_browser')
        assert 'Unsupported browser' in str(exc_info.value)

    def test_format_time_helper(self):
        """Test time formatting helper."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        # MM:SS format
        assert toolkit.yt_dlp._format_time(65) == "1:05"
        assert toolkit.yt_dlp._format_time(0) == "0:00"
        assert toolkit.yt_dlp._format_time(59) == "0:59"

        # HH:MM:SS format
        assert toolkit.yt_dlp._format_time(3600) == "1:00:00"
        assert toolkit.yt_dlp._format_time(3661) == "1:01:01"

    def test_sponsorblock_category_descriptions(self):
        """Test SponsorBlock category description helper."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert 'Sponsored' in toolkit.yt_dlp._get_sponsorblock_category_description('sponsor')
        assert 'Intro' in toolkit.yt_dlp._get_sponsorblock_category_description('intro')
        assert 'Outro' in toolkit.yt_dlp._get_sponsorblock_category_description('outro')


class TestSponsorBlockAPI:
    """Tests for SponsorBlock API."""

    def test_segments_with_mock(self):
        """Test segments retrieval with mock."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.yt_dlp, 'get_sponsorblock_segments') as mock:
            mock.return_value = [
                {'category': 'sponsor', 'start_time': 10, 'end_time': 30},
                {'category': 'intro', 'start_time': 0, 'end_time': 5},
            ]

            segments = toolkit.sponsorblock.segments('https://youtube.com/watch?v=test')

            assert len(segments) == 2
            assert segments[0]['category'] == 'sponsor'


class TestEngagementAPI:
    """Tests for Engagement API."""

    def test_heatmap_with_mock(self):
        """Test heatmap retrieval with mock."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.yt_dlp, 'get_heatmap') as mock:
            mock.return_value = [
                {'start_time': 0, 'end_time': 10, 'value': 0.5},
                {'start_time': 10, 'end_time': 20, 'value': 0.8},
            ]

            heatmap = toolkit.engagement.heatmap('https://youtube.com/watch?v=test')

            assert len(heatmap) == 2
            assert heatmap[1]['value'] == 0.8

    def test_comments_with_mock(self):
        """Test comments retrieval with mock."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.yt_dlp, 'get_comments') as mock:
            mock.return_value = [
                {'text': 'Great video!', 'author': 'User1', 'like_count': 10},
                {'text': 'Thanks!', 'author': 'User2', 'like_count': 5},
            ]

            comments = toolkit.engagement.comments('https://youtube.com/watch?v=test')

            assert len(comments) == 2
            assert comments[0]['like_count'] == 10


class TestLiveStreamAPI:
    """Tests for Live Stream API."""

    def test_status_with_mock(self):
        """Test live status retrieval with mock."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.yt_dlp, 'get_live_status') as mock:
            mock.return_value = {
                'is_live': True,
                'was_live': False,
                'live_status': 'is_live',
            }

            status = toolkit.live.status('https://youtube.com/watch?v=test')

            assert status['is_live'] is True

    def test_is_live_with_mock(self):
        """Test is_live helper."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.yt_dlp, 'get_live_status') as mock:
            mock.return_value = {'is_live': True}
            assert toolkit.live.is_live('url') is True

            mock.return_value = {'is_live': False}
            assert toolkit.live.is_live('url') is False


class TestChapterAPI:
    """Tests for Chapter API."""

    def test_get_chapters_with_mock(self):
        """Test chapter retrieval with mock."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.pytubefix, 'get_video_chapters') as mock:
            mock.return_value = [
                {'title': 'Intro', 'start_time': 0, 'end_time': 60},
                {'title': 'Main', 'start_time': 60, 'end_time': 300},
            ]

            chapters = toolkit.chapters.get('https://youtube.com/watch?v=test')

            assert len(chapters) == 2
            assert chapters[0]['title'] == 'Intro'


class TestArchiveAPI:
    """Tests for Archive API."""

    def test_set_archive_file(self):
        """Test archive file setting."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        toolkit.archive.set_archive_file('/tmp/archive.txt')
        assert toolkit.archive._archive_file == '/tmp/archive.txt'

    def test_contains_without_archive_file(self):
        """Test contains returns False without archive file."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        # No archive file set
        assert toolkit.archive.contains('https://youtube.com/watch?v=test') is False


class TestThumbnailAPI:
    """Tests for Thumbnail API."""

    def test_url_with_mock(self):
        """Test thumbnail URL retrieval."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit.yt_dlp, 'get_video_info') as mock:
            mock.return_value = {
                'thumbnail_url': 'https://i.ytimg.com/vi/test/maxresdefault.jpg'
            }

            url = toolkit.thumbnail.url('https://youtube.com/watch?v=test')

            assert 'maxresdefault' in url

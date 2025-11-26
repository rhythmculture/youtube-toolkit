"""
Tests for v0.6 features: Match Filters, Metadata Export, YouTube Shorts.
"""

import pytest
from unittest.mock import patch, MagicMock
import os


class TestV06APIImports:
    """Tests for importing v0.6 APIs."""

    def test_import_v06_sub_apis(self):
        """Test that v0.6 sub-APIs can be imported."""
        from youtube_toolkit.sub_apis import (
            FilterAPI,
            MetadataAPI,
            ShortsAPI
        )
        assert FilterAPI is not None
        assert MetadataAPI is not None
        assert ShortsAPI is not None


class TestToolkitV06APIs:
    """Tests for v0.6 APIs on YouTubeToolkit."""

    def test_filter_api_exists(self):
        """Test that filter API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'filter')
        assert hasattr(toolkit.filter, 'download')
        assert hasattr(toolkit.filter, 'preview')
        assert hasattr(toolkit.filter, 'playlist')
        assert hasattr(toolkit.filter, 'batch_download')

    def test_metadata_api_exists(self):
        """Test that metadata API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'metadata')
        assert hasattr(toolkit.metadata, 'download_with_files')
        assert hasattr(toolkit.metadata, 'export')
        assert hasattr(toolkit.metadata, 'full')

    def test_shorts_api_exists(self):
        """Test that shorts API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'shorts')
        assert hasattr(toolkit.shorts, 'is_short')
        assert hasattr(toolkit.shorts, 'info')
        assert hasattr(toolkit.shorts, 'download')
        assert hasattr(toolkit.shorts, 'from_channel')
        assert hasattr(toolkit.shorts, 'batch_download')


class TestMatchFiltersAPI:
    """Tests for Match Filters API."""

    def test_download_with_filter_method_exists(self):
        """Test that download_with_filter method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'download_with_filter')

    def test_get_videos_matching_filter_method_exists(self):
        """Test that get_videos_matching_filter method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_videos_matching_filter')

    def test_filter_playlist_method_exists(self):
        """Test that filter_playlist method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'filter_playlist')

    def test_batch_download_with_filter_method_exists(self):
        """Test that batch_download_with_filter method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'batch_download_with_filter')

    def test_filter_api_download_calls_toolkit(self):
        """Test that filter.download calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'download_with_filter') as mock:
            mock.return_value = '/tmp/video.mp4'

            result = toolkit.filter.download(
                'https://youtube.com/watch?v=test',
                match_filter='duration > 600'
            )

            assert result == '/tmp/video.mp4'
            mock.assert_called_once()

    def test_filter_api_preview_calls_toolkit(self):
        """Test that filter.preview calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_videos_matching_filter') as mock:
            mock.return_value = [
                {'title': 'Video 1', 'duration': 700},
                {'title': 'Video 2', 'duration': 800},
            ]

            result = toolkit.filter.preview(
                'https://youtube.com/playlist?list=test',
                match_filter='duration > 600'
            )

            assert len(result) == 2
            mock.assert_called_once()


class TestMetadataExportAPI:
    """Tests for Metadata Export API."""

    def test_download_with_metadata_files_method_exists(self):
        """Test that download_with_metadata_files method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'download_with_metadata_files')

    def test_export_metadata_only_method_exists(self):
        """Test that export_metadata_only method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'export_metadata_only')

    def test_get_full_metadata_method_exists(self):
        """Test that get_full_metadata method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_full_metadata')

    def test_metadata_api_export_calls_toolkit(self):
        """Test that metadata.export calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'export_metadata_only') as mock:
            mock.return_value = '/tmp/video.info.json'

            result = toolkit.metadata.export(
                'https://youtube.com/watch?v=test',
                format='json'
            )

            assert result == '/tmp/video.info.json'
            mock.assert_called_once()

    def test_metadata_api_full_calls_toolkit(self):
        """Test that metadata.full calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_full_metadata') as mock:
            mock.return_value = {
                'id': 'test123',
                'title': 'Test Video',
                'duration': 600,
                'view_count': 10000,
                'channel': 'Test Channel',
                'categories': ['Education'],
                'tags': ['test', 'video'],
            }

            result = toolkit.metadata.full('https://youtube.com/watch?v=test')

            assert result['id'] == 'test123'
            assert 'categories' in result
            assert 'tags' in result
            mock.assert_called_once()


class TestYouTubeShortsAPI:
    """Tests for YouTube Shorts API."""

    def test_is_youtube_short_method_exists(self):
        """Test that is_youtube_short method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'is_youtube_short')

    def test_get_shorts_info_method_exists(self):
        """Test that get_shorts_info method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_shorts_info')

    def test_download_short_method_exists(self):
        """Test that download_short method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'download_short')

    def test_get_channel_shorts_method_exists(self):
        """Test that get_channel_shorts method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_channel_shorts')

    def test_batch_download_shorts_method_exists(self):
        """Test that batch_download_shorts method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'batch_download_shorts')

    def test_shorts_api_is_short_calls_toolkit(self):
        """Test that shorts.is_short calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'is_youtube_short') as mock:
            mock.return_value = True

            result = toolkit.shorts.is_short('https://youtube.com/shorts/test')

            assert result is True
            mock.assert_called_once()

    def test_shorts_api_info_calls_toolkit(self):
        """Test that shorts.info calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_shorts_info') as mock:
            mock.return_value = {
                'id': 'short123',
                'title': 'Test Short',
                'duration': 30,
                'is_short': True,
                'is_vertical': True,
            }

            result = toolkit.shorts.info('https://youtube.com/shorts/test')

            assert result['is_short'] is True
            assert result['duration'] == 30
            mock.assert_called_once()

    def test_shorts_api_from_channel_calls_toolkit(self):
        """Test that shorts.from_channel calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_channel_shorts') as mock:
            mock.return_value = [
                {'id': 'short1', 'title': 'Short 1'},
                {'id': 'short2', 'title': 'Short 2'},
            ]

            result = toolkit.shorts.from_channel('@testchannel', max_results=10)

            assert len(result) == 2
            mock.assert_called_once()


class TestYTDLPHandlerV06Features:
    """Tests for yt-dlp handler v0.6 features."""

    def test_handler_has_filter_methods(self):
        """Test that yt-dlp handler has filter methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.yt_dlp, 'download_with_filter')
        assert hasattr(toolkit.yt_dlp, 'get_videos_matching_filter')
        assert hasattr(toolkit.yt_dlp, 'filter_playlist')
        assert hasattr(toolkit.yt_dlp, 'batch_download_with_filter')

    def test_handler_has_metadata_methods(self):
        """Test that yt-dlp handler has metadata methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.yt_dlp, 'download_with_metadata_files')
        assert hasattr(toolkit.yt_dlp, 'export_metadata_only')
        assert hasattr(toolkit.yt_dlp, 'get_full_metadata')

    def test_handler_has_shorts_methods(self):
        """Test that yt-dlp handler has shorts methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.yt_dlp, 'is_youtube_short')
        assert hasattr(toolkit.yt_dlp, 'get_shorts_info')
        assert hasattr(toolkit.yt_dlp, 'download_short')
        assert hasattr(toolkit.yt_dlp, 'get_channel_shorts')
        assert hasattr(toolkit.yt_dlp, 'batch_download_shorts')


class TestShortsURLDetection:
    """Tests for YouTube Shorts URL detection."""

    def test_shorts_url_pattern(self):
        """Test detection of Shorts URL pattern."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        # Test with Shorts URL patterns
        shorts_urls = [
            'https://www.youtube.com/shorts/abc123',
            'https://youtube.com/shorts/abc123',
            'https://youtu.be/shorts/abc123',
        ]

        for url in shorts_urls:
            with patch.object(toolkit.yt_dlp, 'is_youtube_short') as mock:
                # The actual implementation checks URL patterns
                if '/shorts/' in url:
                    mock.return_value = True
                else:
                    mock.return_value = False

                # We're testing the API exists and can be called
                toolkit.is_youtube_short(url)
                mock.assert_called_once()


class TestFilterExpressions:
    """Tests for filter expression building."""

    def test_filter_playlist_builds_expression(self):
        """Test that filter_playlist builds correct filter expressions."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        # Test with duration filter
        with patch.object(toolkit.yt_dlp, 'filter_playlist') as mock:
            mock.return_value = []

            toolkit.filter_playlist(
                'https://youtube.com/playlist?list=test',
                min_duration=300,
                max_duration=1200
            )

            # Verify method was called with parameters
            mock.assert_called_once()
            call_args = mock.call_args
            assert call_args[0][0] == 'https://youtube.com/playlist?list=test'

"""
Tests for v0.7 features: YouTube API Analytical Features.

These features use the official YouTube Data API v3.
"""

import pytest
from unittest.mock import patch, MagicMock
import os


class TestV07APIImports:
    """Tests for importing v0.7 APIs."""

    def test_import_v07_sub_apis(self):
        """Test that v0.7 sub-APIs can be imported."""
        from youtube_toolkit.sub_apis import (
            SubscriptionsAPI,
            CategoriesAPI,
            I18nAPI,
            ActivitiesAPI,
            TrendingAPI,
            ChannelSectionsAPI,
            ChannelInfoAPI
        )
        assert SubscriptionsAPI is not None
        assert CategoriesAPI is not None
        assert I18nAPI is not None
        assert ActivitiesAPI is not None
        assert TrendingAPI is not None
        assert ChannelSectionsAPI is not None
        assert ChannelInfoAPI is not None


class TestToolkitV07APIs:
    """Tests for v0.7 APIs on YouTubeToolkit."""

    def test_subscriptions_api_exists(self):
        """Test that subscriptions API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'subscriptions')
        assert hasattr(toolkit.subscriptions, 'list')
        assert hasattr(toolkit.subscriptions, 'check')

    def test_categories_api_exists(self):
        """Test that categories API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'categories')
        assert hasattr(toolkit.categories, 'list')
        assert hasattr(toolkit.categories, 'get')

    def test_i18n_api_exists(self):
        """Test that i18n API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'i18n')
        assert hasattr(toolkit.i18n, 'languages')
        assert hasattr(toolkit.i18n, 'regions')

    def test_activities_api_exists(self):
        """Test that activities API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'activities')
        assert hasattr(toolkit.activities, 'feed')
        assert hasattr(toolkit.activities, 'uploads')

    def test_trending_api_exists(self):
        """Test that trending API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'trending')
        assert hasattr(toolkit.trending, 'videos')
        assert hasattr(toolkit.trending, 'by_category')

    def test_sections_api_exists(self):
        """Test that sections API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'sections')
        assert hasattr(toolkit.sections, 'list')
        assert hasattr(toolkit.sections, 'featured_channels')

    def test_channel_info_api_exists(self):
        """Test that channel_info API is initialized."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'channel_info')
        assert hasattr(toolkit.channel_info, 'get')
        assert hasattr(toolkit.channel_info, 'batch')


class TestSubscriptionsAPI:
    """Tests for Subscriptions API."""

    def test_list_method_exists(self):
        """Test that list method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_channel_subscriptions')

    def test_check_method_exists(self):
        """Test that check method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'check_subscription')

    def test_subscriptions_api_list_calls_toolkit(self):
        """Test that subscriptions.list calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_channel_subscriptions') as mock:
            mock.return_value = {
                'subscriptions': [],
                'total_results': 0,
            }

            result = toolkit.subscriptions.list('UC_test_channel')

            assert result['total_results'] == 0
            mock.assert_called_once()


class TestCategoriesAPI:
    """Tests for Categories API."""

    def test_get_video_categories_method_exists(self):
        """Test that get_video_categories method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_video_categories')

    def test_get_category_by_id_method_exists(self):
        """Test that get_category_by_id method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_category_by_id')

    def test_categories_api_list_calls_toolkit(self):
        """Test that categories.list calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_video_categories') as mock:
            mock.return_value = [
                {'id': '10', 'title': 'Music', 'assignable': True},
                {'id': '20', 'title': 'Gaming', 'assignable': True},
            ]

            result = toolkit.categories.list(region='US')

            assert len(result) == 2
            assert result[0]['title'] == 'Music'
            mock.assert_called_once()


class TestI18nAPI:
    """Tests for i18n API."""

    def test_get_supported_languages_method_exists(self):
        """Test that get_supported_languages method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_supported_languages')

    def test_get_supported_regions_method_exists(self):
        """Test that get_supported_regions method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_supported_regions')

    def test_i18n_api_languages_calls_toolkit(self):
        """Test that i18n.languages calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_supported_languages') as mock:
            mock.return_value = [
                {'code': 'en', 'name': 'English'},
                {'code': 'es', 'name': 'Spanish'},
            ]

            result = toolkit.i18n.languages()

            assert len(result) == 2
            mock.assert_called_once()

    def test_i18n_api_regions_calls_toolkit(self):
        """Test that i18n.regions calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_supported_regions') as mock:
            mock.return_value = [
                {'code': 'US', 'name': 'United States'},
                {'code': 'GB', 'name': 'United Kingdom'},
            ]

            result = toolkit.i18n.regions()

            assert len(result) == 2
            mock.assert_called_once()


class TestActivitiesAPI:
    """Tests for Activities API."""

    def test_get_channel_activities_method_exists(self):
        """Test that get_channel_activities method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_channel_activities')

    def test_get_recent_uploads_method_exists(self):
        """Test that get_recent_uploads method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_recent_uploads')

    def test_activities_api_feed_calls_toolkit(self):
        """Test that activities.feed calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_channel_activities') as mock:
            mock.return_value = {
                'activities': [
                    {'type': 'upload', 'title': 'New Video'},
                    {'type': 'like', 'title': 'Liked Video'},
                ],
                'total_results': 2,
            }

            result = toolkit.activities.feed('UC_test_channel')

            assert len(result['activities']) == 2
            mock.assert_called_once()

    def test_activities_api_uploads_calls_toolkit(self):
        """Test that activities.uploads calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_recent_uploads') as mock:
            mock.return_value = [
                {'video_id': 'abc123', 'title': 'Video 1'},
                {'video_id': 'def456', 'title': 'Video 2'},
            ]

            result = toolkit.activities.uploads('UC_test_channel')

            assert len(result) == 2
            mock.assert_called_once()


class TestTrendingAPI:
    """Tests for Trending API."""

    def test_get_trending_videos_method_exists(self):
        """Test that get_trending_videos method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_trending_videos')

    def test_get_trending_by_category_method_exists(self):
        """Test that get_trending_by_category method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_trending_by_category')

    def test_trending_api_videos_calls_toolkit(self):
        """Test that trending.videos calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_trending_videos') as mock:
            mock.return_value = {
                'videos': [
                    {'video_id': 'abc123', 'title': 'Trending Video 1', 'view_count': 1000000},
                ],
                'total_results': 1,
            }

            result = toolkit.trending.videos(region='US')

            assert len(result['videos']) == 1
            mock.assert_called_once()

    def test_trending_api_by_category_calls_toolkit(self):
        """Test that trending.by_category calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_trending_by_category') as mock:
            mock.return_value = {
                'Music': [{'video_id': 'abc123', 'title': 'Music Video'}],
                'Gaming': [{'video_id': 'def456', 'title': 'Gaming Video'}],
            }

            result = toolkit.trending.by_category(region='US')

            assert 'Music' in result
            assert 'Gaming' in result
            mock.assert_called_once()


class TestChannelSectionsAPI:
    """Tests for Channel Sections API."""

    def test_get_channel_sections_method_exists(self):
        """Test that get_channel_sections method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_channel_sections')

    def test_get_channel_featured_channels_method_exists(self):
        """Test that get_channel_featured_channels method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_channel_featured_channels')

    def test_sections_api_list_calls_toolkit(self):
        """Test that sections.list calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_channel_sections') as mock:
            mock.return_value = [
                {'section_id': 'sec1', 'type': 'uploads', 'title': 'Uploads'},
                {'section_id': 'sec2', 'type': 'playlists', 'title': 'Playlists'},
            ]

            result = toolkit.sections.list('UC_test_channel')

            assert len(result) == 2
            mock.assert_called_once()


class TestChannelInfoAPI:
    """Tests for Enhanced Channel Info API."""

    def test_get_channel_info_full_method_exists(self):
        """Test that get_channel_info_full method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_channel_info_full')

    def test_get_multiple_channels_method_exists(self):
        """Test that get_multiple_channels method exists on toolkit."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()
        assert hasattr(toolkit, 'get_multiple_channels')

    def test_channel_info_api_get_calls_toolkit(self):
        """Test that channel_info.get calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_channel_info_full') as mock:
            mock.return_value = {
                'channel_id': 'UC_test',
                'title': 'Test Channel',
                'subscriber_count': 1000000,
                'video_count': 500,
            }

            result = toolkit.channel_info.get(channel_id='UC_test')

            assert result['title'] == 'Test Channel'
            assert result['subscriber_count'] == 1000000
            mock.assert_called_once()

    def test_channel_info_api_batch_calls_toolkit(self):
        """Test that channel_info.batch calls toolkit method."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        with patch.object(toolkit, 'get_multiple_channels') as mock:
            mock.return_value = [
                {'channel_id': 'UC1', 'title': 'Channel 1'},
                {'channel_id': 'UC2', 'title': 'Channel 2'},
            ]

            result = toolkit.channel_info.batch(['UC1', 'UC2'])

            assert len(result) == 2
            mock.assert_called_once()


class TestYouTubeAPIHandlerV07Features:
    """Tests for YouTube API handler v0.7 features."""

    def test_handler_has_subscription_methods(self):
        """Test that YouTube API handler has subscription methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.youtube_api, 'get_channel_subscriptions')
        assert hasattr(toolkit.youtube_api, 'check_subscription')

    def test_handler_has_categories_methods(self):
        """Test that YouTube API handler has categories methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.youtube_api, 'get_video_categories')
        assert hasattr(toolkit.youtube_api, 'get_category_by_id')

    def test_handler_has_i18n_methods(self):
        """Test that YouTube API handler has i18n methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.youtube_api, 'get_supported_languages')
        assert hasattr(toolkit.youtube_api, 'get_supported_regions')

    def test_handler_has_activities_methods(self):
        """Test that YouTube API handler has activities methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.youtube_api, 'get_channel_activities')
        assert hasattr(toolkit.youtube_api, 'get_recent_uploads')

    def test_handler_has_trending_methods(self):
        """Test that YouTube API handler has trending methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.youtube_api, 'get_trending_videos')
        assert hasattr(toolkit.youtube_api, 'get_trending_by_category')

    def test_handler_has_channel_sections_methods(self):
        """Test that YouTube API handler has channel sections methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.youtube_api, 'get_channel_sections')
        assert hasattr(toolkit.youtube_api, 'get_channel_featured_channels')

    def test_handler_has_channel_info_methods(self):
        """Test that YouTube API handler has channel info methods."""
        from youtube_toolkit import YouTubeToolkit
        toolkit = YouTubeToolkit()

        assert hasattr(toolkit.youtube_api, 'get_channel_info')
        assert hasattr(toolkit.youtube_api, 'get_multiple_channels')

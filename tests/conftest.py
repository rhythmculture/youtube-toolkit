"""
Pytest configuration and shared fixtures for youtube-toolkit tests.
"""

import pytest
from unittest.mock import MagicMock, patch


# Sample video data for testing
SAMPLE_VIDEO_ID = "dQw4w9WgXcQ"
SAMPLE_VIDEO_URL = f"https://www.youtube.com/watch?v={SAMPLE_VIDEO_ID}"
SAMPLE_PLAYLIST_URL = "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"


@pytest.fixture
def sample_video_info():
    """Sample video info for testing."""
    return {
        "title": "Test Video Title",
        "duration": 180,
        "views": 1000000,
        "author": "Test Channel",
        "video_id": SAMPLE_VIDEO_ID,
        "url": SAMPLE_VIDEO_URL,
        "description": "This is a test video description",
        "thumbnail": "https://i.ytimg.com/vi/dQw4w9WgXcQ/maxresdefault.jpg",
        "upload_date": "2023-01-15",
    }


@pytest.fixture
def sample_search_results():
    """Sample search results for testing."""
    return [
        {
            "video_id": "abc123",
            "title": "First Result",
            "author": "Channel 1",
            "views": 500000,
            "duration": 120,
        },
        {
            "video_id": "def456",
            "title": "Second Result",
            "author": "Channel 2",
            "views": 300000,
            "duration": 240,
        },
    ]


@pytest.fixture
def mock_toolkit():
    """Create a mock YouTubeToolkit for unit testing."""
    with patch("youtube_toolkit.YouTubeToolkit") as mock:
        yield mock


@pytest.fixture
def video_url():
    """Provide sample video URL."""
    return SAMPLE_VIDEO_URL


@pytest.fixture
def video_id():
    """Provide sample video ID."""
    return SAMPLE_VIDEO_ID

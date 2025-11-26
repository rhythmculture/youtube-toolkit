"""
Tests for core data structures (VideoInfo, DownloadResult, SearchResult).
"""

import pytest
from youtube_toolkit.core import VideoInfo, DownloadResult, SearchResult


class TestVideoInfo:
    """Tests for VideoInfo dataclass."""

    def test_basic_creation(self):
        """Test basic VideoInfo creation."""
        info = VideoInfo(
            title="Test Video",
            duration=180,
            views=1000,
            author="Test Author",
            video_id="abc123",
            url="https://youtube.com/watch?v=abc123",
        )
        assert info.title == "Test Video"
        assert info.duration == 180
        assert info.views == 1000
        assert info.author == "Test Author"
        assert info.video_id == "abc123"

    def test_negative_duration_fixed(self):
        """Test that negative duration is corrected to 0."""
        info = VideoInfo(
            title="Test",
            duration=-10,
            views=100,
            author="Author",
            video_id="id",
            url="url",
        )
        assert info.duration == 0

    def test_negative_views_fixed(self):
        """Test that negative views is corrected to 0."""
        info = VideoInfo(
            title="Test",
            duration=100,
            views=-500,
            author="Author",
            video_id="id",
            url="url",
        )
        assert info.views == 0

    def test_title_whitespace_stripped(self):
        """Test that title whitespace is stripped."""
        info = VideoInfo(
            title="  Test Title  ",
            duration=100,
            views=100,
            author="Author",
            video_id="id",
            url="url",
        )
        assert info.title == "Test Title"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        info = VideoInfo(
            title="Test",
            duration=100,
            views=100,
            author="Author",
            video_id="id",
            url="url",
        )
        d = info.to_dict()
        assert isinstance(d, dict)
        assert d["title"] == "Test"
        assert d["duration"] == 100
        assert "description" in d  # Optional fields should be present

    def test_from_dict(self):
        """Test creation from dictionary."""
        data = {
            "title": "Test",
            "duration": 100,
            "views": 100,
            "author": "Author",
            "video_id": "id",
            "url": "url",
        }
        info = VideoInfo.from_dict(data)
        assert info.title == "Test"
        assert info.duration == 100


class TestDownloadResult:
    """Tests for DownloadResult dataclass."""

    def test_success_result(self):
        """Test successful download result."""
        result = DownloadResult.success_result(
            file_path="/path/to/file.mp3",
            file_size=1024000,
            format="mp3",
        )
        assert result.success is True
        assert result.file_path == "/path/to/file.mp3"
        assert result.file_size == 1024000

    def test_failure_result(self):
        """Test failed download result."""
        result = DownloadResult.failure_result(
            file_path="/path/to/file.mp3",
            error_message="Network error",
        )
        assert result.success is False
        assert result.error_message == "Network error"

    def test_file_size_mb(self):
        """Test file size in MB calculation."""
        result = DownloadResult(
            file_path="/path/to/file.mp3",
            file_size=1048576,  # 1 MB
        )
        assert result.file_size_mb == 1.0

    def test_default_error_message(self):
        """Test that failed results get default error message."""
        result = DownloadResult(
            file_path="/path/to/file.mp3",
            success=False,
        )
        assert result.error_message == "Unknown error occurred"

    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = DownloadResult(file_path="/path/to/file.mp3")
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["file_path"] == "/path/to/file.mp3"
        assert "success" in d
        assert "file_exists" in d


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_basic_creation(self):
        """Test basic SearchResult creation."""
        result = SearchResult(
            items=[],
            total_results=0,
            query="test query",
        )
        assert result.query == "test query"
        assert result.total_results == 0
        assert result.items == []

    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = SearchResult(
            items=[],
            total_results=0,
            query="test",
        )
        d = result.to_dict()
        assert isinstance(d, dict)
        assert d["query"] == "test"

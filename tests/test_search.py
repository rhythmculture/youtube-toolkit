"""
Tests for search functionality and SearchFilters.
"""

import pytest
from youtube_toolkit.core.search import (
    SearchFilters,
    SearchResult,
    SearchResultItem,
    BooleanSearchQuery,
    YOUTUBE_CATEGORIES,
)


class TestSearchFilters:
    """Tests for SearchFilters dataclass."""

    def test_default_filters(self):
        """Test default filter values."""
        filters = SearchFilters()
        assert filters.type == "video"
        assert filters.order == "relevance"
        assert filters.max_results == 20

    def test_custom_filters(self):
        """Test custom filter values."""
        filters = SearchFilters(
            type="channel",
            order="viewCount",
            max_results=50,
            region_code="US",
        )
        assert filters.type == "channel"
        assert filters.order == "viewCount"
        assert filters.max_results == 50
        assert filters.region_code == "US"

    def test_duration_filter(self):
        """Test video duration filter."""
        filters = SearchFilters(video_duration="short")
        assert filters.video_duration == "short"

    def test_definition_filter(self):
        """Test video definition filter."""
        filters = SearchFilters(video_definition="high")
        assert filters.video_definition == "high"


class TestBooleanSearchQuery:
    """Tests for Boolean search query parsing."""

    def test_simple_query(self):
        """Test simple query without operators."""
        query = BooleanSearchQuery.from_string("python tutorial")
        result = query.build_query()
        assert "python tutorial" in result

    def test_not_operator(self):
        """Test NOT operator (-)."""
        query = BooleanSearchQuery.from_string("python -beginner")
        result = query.build_query()
        assert "-beginner" in result

    def test_or_operator(self):
        """Test OR operator (|)."""
        query = BooleanSearchQuery.from_string("python|javascript")
        result = query.build_query()
        assert "|" in result or "python" in result

    def test_complex_query(self):
        """Test complex query with multiple operators."""
        query = BooleanSearchQuery.from_string("tutorial -beginner python|javascript")
        result = query.build_query()
        assert isinstance(result, str)
        assert len(result) > 0


class TestSearchResultItem:
    """Tests for SearchResultItem dataclass."""

    def test_basic_creation(self):
        """Test basic SearchResultItem creation."""
        item = SearchResultItem(
            kind="youtube#video",
            etag="test_etag",
            video_id="abc123",
            title="Test Video",
            description="Test description",
            channel_title="Test Channel",
        )
        assert item.video_id == "abc123"
        assert item.title == "Test Video"

    def test_with_thumbnails(self):
        """Test SearchResultItem with thumbnails."""
        from youtube_toolkit.core.search import Thumbnails, Thumbnail

        thumb = Thumbnail(url="https://example.com/thumb.jpg", width=120, height=90)
        thumbnails = Thumbnails(default=thumb)

        item = SearchResultItem(
            kind="youtube#video",
            etag="test",
            video_id="abc123",
            title="Test",
            thumbnails=thumbnails,
        )
        assert item.thumbnails is not None
        assert item.thumbnails.default.url == "https://example.com/thumb.jpg"


class TestSearchResult:
    """Tests for SearchResult dataclass."""

    def test_empty_result(self):
        """Test empty search result."""
        result = SearchResult(
            items=[],
            total_results=0,
            query="test",
        )
        assert len(result.items) == 0
        assert result.total_results == 0

    def test_with_items(self):
        """Test search result with items."""
        items = [
            SearchResultItem(
                kind="youtube#video",
                etag="1",
                video_id="abc",
                title="Video 1",
            ),
            SearchResultItem(
                kind="youtube#video",
                etag="2",
                video_id="def",
                title="Video 2",
            ),
        ]
        result = SearchResult(
            items=items,
            total_results=2,
            query="test",
        )
        assert len(result.items) == 2
        assert result.total_results == 2

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
        assert d["total_results"] == 0


class TestYouTubeCategories:
    """Tests for YouTube category constants."""

    def test_categories_exist(self):
        """Test that common categories exist."""
        assert "Music" in YOUTUBE_CATEGORIES
        assert "Gaming" in YOUTUBE_CATEGORIES
        assert "Education" in YOUTUBE_CATEGORIES
        assert "Sports" in YOUTUBE_CATEGORIES

    def test_category_ids_are_strings(self):
        """Test that category IDs are strings."""
        for name, cat_id in YOUTUBE_CATEGORIES.items():
            assert isinstance(cat_id, str)
            assert len(cat_id) > 0

"""
Tests for comment functionality and CommentFilters.
"""

import pytest
from datetime import datetime, timedelta
from youtube_toolkit.core.comments import (
    CommentFilters,
    CommentOrder,
    CommentResult,
    Comment,
    CommentAuthor,
    CommentMetrics,
    CommentAnalytics,
)


class TestCommentFilters:
    """Tests for CommentFilters dataclass."""

    def test_default_filters(self):
        """Test default filter values."""
        filters = CommentFilters()
        assert filters.max_results == 100
        assert filters.order == CommentOrder.RELEVANCE

    def test_custom_max_results(self):
        """Test custom max results."""
        filters = CommentFilters(max_results=50)
        assert filters.max_results == 50

    def test_order_options(self):
        """Test different order options."""
        filters_relevance = CommentFilters(order=CommentOrder.RELEVANCE)
        filters_time = CommentFilters(order=CommentOrder.TIME)
        filters_rating = CommentFilters(order=CommentOrder.RATING)

        assert filters_relevance.order == CommentOrder.RELEVANCE
        assert filters_time.order == CommentOrder.TIME
        assert filters_rating.order == CommentOrder.RATING

    def test_date_filters(self):
        """Test date range filters."""
        now = datetime.now()
        week_ago = now - timedelta(days=7)

        filters = CommentFilters(
            published_after=week_ago,
            published_before=now,
        )
        assert filters.published_after == week_ago
        assert filters.published_before == now

    def test_min_likes_filter(self):
        """Test minimum likes filter."""
        filters = CommentFilters(min_likes=10)
        assert filters.min_likes == 10


class TestCommentAuthor:
    """Tests for CommentAuthor dataclass."""

    def test_basic_creation(self):
        """Test basic author creation."""
        author = CommentAuthor(
            display_name="Test User",
            channel_id="UC123456",
            profile_image_url="https://example.com/avatar.jpg",
        )
        assert author.display_name == "Test User"
        assert author.channel_id == "UC123456"

    def test_optional_fields(self):
        """Test optional fields."""
        author = CommentAuthor(
            display_name="Test User",
            channel_id="UC123456",
            is_verified=True,
            is_channel_owner=True,
        )
        assert author.is_verified is True
        assert author.is_channel_owner is True


class TestCommentMetrics:
    """Tests for CommentMetrics dataclass."""

    def test_basic_metrics(self):
        """Test basic metrics creation."""
        metrics = CommentMetrics(
            like_count=100,
            reply_count=10,
        )
        assert metrics.like_count == 100
        assert metrics.reply_count == 10


class TestComment:
    """Tests for Comment dataclass."""

    def test_basic_creation(self):
        """Test basic comment creation."""
        author = CommentAuthor(display_name="User", channel_id="UC123")
        metrics = CommentMetrics(like_count=5, reply_count=1)

        comment = Comment(
            comment_id="comment123",
            text="This is a test comment",
            author=author,
            published_at=datetime.now(),
            metrics=metrics,
        )
        assert comment.comment_id == "comment123"
        assert comment.text == "This is a test comment"
        assert comment.author.display_name == "User"

    def test_reply_comment(self):
        """Test reply comment with parent_id."""
        author = CommentAuthor(display_name="User", channel_id="UC123")
        metrics = CommentMetrics(like_count=0, reply_count=0)

        comment = Comment(
            comment_id="reply123",
            text="This is a reply",
            author=author,
            published_at=datetime.now(),
            metrics=metrics,
            parent_id="comment123",
        )
        assert comment.parent_id == "comment123"
        assert comment.is_reply is True
        assert comment.is_top_level is False


class TestCommentResult:
    """Tests for CommentResult dataclass."""

    def test_empty_result(self):
        """Test empty comment result."""
        result = CommentResult(
            comments=[],
            total_results=0,
        )
        assert len(result.comments) == 0
        assert result.total_results == 0

    def test_with_comments(self):
        """Test result with comments."""
        author = CommentAuthor(display_name="User", channel_id="UC123")
        metrics = CommentMetrics(like_count=5, reply_count=0)
        comment = Comment(
            comment_id="c1",
            text="Test",
            author=author,
            published_at=datetime.now(),
            metrics=metrics,
        )

        result = CommentResult(
            comments=[comment],
            total_results=1,
        )
        assert len(result.comments) == 1
        assert result.total_results == 1
        assert result.comment_count == 1


class TestCommentAnalytics:
    """Tests for CommentAnalytics dataclass."""

    def test_basic_analytics(self):
        """Test basic analytics creation."""
        analytics = CommentAnalytics(
            total_comments=100,
            total_replies=50,
            total_likes=500,
            unique_authors=80,
        )
        assert analytics.total_comments == 100
        assert analytics.total_replies == 50
        assert analytics.total_likes == 500
        assert analytics.unique_authors == 80

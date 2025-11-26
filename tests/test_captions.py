"""
Tests for caption functionality and CaptionFilters.
"""

import pytest
from youtube_toolkit.core.captions import (
    CaptionFilters,
    CaptionResult,
    CaptionTrack,
    CaptionTrackType,
    CaptionStatus,
    CaptionContent,
    CaptionCue,
    CaptionFormatConverter,
    CaptionAnalyzer,
)


class TestCaptionFilters:
    """Tests for CaptionFilters dataclass."""

    def test_default_filters(self):
        """Test default filter values."""
        filters = CaptionFilters()
        assert filters.language_codes is None or len(filters.language_codes) == 0

    def test_language_filter(self):
        """Test language codes filter."""
        filters = CaptionFilters(language_codes=["en", "es"])
        assert "en" in filters.language_codes
        assert "es" in filters.language_codes


class TestCaptionCue:
    """Tests for CaptionCue dataclass."""

    def test_basic_creation(self):
        """Test basic cue creation."""
        cue = CaptionCue(
            start_time=0.0,
            end_time=5.0,
            text="Hello world",
        )
        assert cue.start_time == 0.0
        assert cue.end_time == 5.0
        assert cue.text == "Hello world"

    def test_duration_property(self):
        """Test duration calculation."""
        cue = CaptionCue(
            start_time=10.0,
            end_time=15.5,
            text="Test",
        )
        assert cue.duration == 5.5

    def test_formatted_time(self):
        """Test formatted time strings."""
        cue = CaptionCue(
            start_time=3661.5,  # 1:01:01.5
            end_time=3665.0,
            text="Test",
        )
        assert "01:01" in cue.formatted_start
        assert "01:05" in cue.formatted_end


class TestCaptionTrack:
    """Tests for CaptionTrack dataclass."""

    def test_basic_creation(self):
        """Test basic track creation."""
        track = CaptionTrack(
            caption_id="cap123",
            language="English",
            language_code="en",
            name="English (auto-generated)",
            track_type=CaptionTrackType.ASR,
            status=CaptionStatus.SERVING,
            is_auto_generated=True,
            is_cc=False,
            is_draft=False,
            is_easy_reader=False,
            is_large=False,
        )
        assert track.caption_id == "cap123"
        assert track.language == "English"
        assert track.language_code == "en"

    def test_auto_generated_detection(self):
        """Test auto-generated caption detection."""
        track = CaptionTrack(
            caption_id="cap123",
            language="English",
            language_code="en",
            name="English",
            track_type=CaptionTrackType.ASR,
            status=CaptionStatus.SERVING,
            is_auto_generated=True,
            is_cc=False,
            is_draft=False,
            is_easy_reader=False,
            is_large=False,
        )
        assert track.is_auto_generated is True
        assert track.is_manual is False


class TestCaptionFormatConverter:
    """Tests for caption format conversion."""

    def test_srt_to_vtt(self):
        """Test SRT to VTT conversion."""
        srt_content = """1
00:00:00,000 --> 00:00:02,000
Hello world

2
00:00:02,000 --> 00:00:04,000
Test subtitle
"""
        vtt = CaptionFormatConverter.srt_to_vtt(srt_content)
        assert "WEBVTT" in vtt
        assert "Hello world" in vtt

    def test_srt_to_txt(self):
        """Test SRT to plain text conversion."""
        srt_content = """1
00:00:00,000 --> 00:00:02,000
Hello world

2
00:00:02,000 --> 00:00:04,000
Test subtitle
"""
        txt = CaptionFormatConverter.srt_to_txt(srt_content)
        assert "Hello world" in txt
        assert "Test subtitle" in txt
        assert "-->" not in txt

    def test_parse_srt(self):
        """Test SRT parsing to cues."""
        srt_content = """1
00:00:00,000 --> 00:00:02,000
Hello world

2
00:00:02,000 --> 00:00:04,000
Test subtitle
"""
        cues = CaptionFormatConverter.parse_srt(srt_content)
        assert len(cues) == 2
        assert cues[0].text == "Hello world"
        assert cues[1].text == "Test subtitle"


class TestCaptionResult:
    """Tests for CaptionResult dataclass."""

    def test_empty_result(self):
        """Test empty caption result."""
        result = CaptionResult(tracks=[])
        assert len(result.tracks) == 0

    def test_get_best_track(self):
        """Test getting best track for language."""
        tracks = [
            CaptionTrack(
                caption_id="1",
                language="English",
                language_code="en",
                name="English",
                track_type=CaptionTrackType.STANDARD,
                status=CaptionStatus.SERVING,
                is_auto_generated=False,
                is_cc=False,
                is_draft=False,
                is_easy_reader=False,
                is_large=False,
            ),
            CaptionTrack(
                caption_id="2",
                language="English",
                language_code="en",
                name="English (auto)",
                track_type=CaptionTrackType.ASR,
                status=CaptionStatus.SERVING,
                is_auto_generated=True,
                is_cc=False,
                is_draft=False,
                is_easy_reader=False,
                is_large=False,
            ),
        ]
        result = CaptionResult(tracks=tracks)

        # Should prefer non-auto-generated
        best = result.get_best_track("en")
        assert best is not None
        assert best.is_auto_generated is False


class TestCaptionAnalyzer:
    """Tests for CaptionAnalyzer utility class."""

    def test_analyze_reading_speed(self):
        """Test reading speed analysis."""
        cues = [
            CaptionCue(start_time=0.0, end_time=10.0, text="This is a test sentence with several words"),
            CaptionCue(start_time=10.0, end_time=20.0, text="Another sentence here with words"),
        ]
        analysis = CaptionAnalyzer.analyze_reading_speed(cues)
        assert "average_wpm" in analysis
        assert analysis["average_wpm"] > 0

    def test_find_gaps(self):
        """Test gap detection between cues."""
        cues = [
            CaptionCue(start_time=0.0, end_time=5.0, text="First"),
            CaptionCue(start_time=10.0, end_time=15.0, text="Second"),  # 5 second gap
        ]
        gaps = CaptionAnalyzer.find_gaps(cues, min_gap=1.0)
        assert len(gaps) == 1
        assert gaps[0]["duration"] == 5.0

"""
Advanced Caption Models for YouTube Toolkit.

This module provides enhanced caption functionality with listing, filtering,
analysis, format conversion, and comprehensive caption management.
"""

from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from enum import Enum
import re


class CaptionTrackType(Enum):
    """Caption track types."""
    STANDARD = "standard"
    ASR = "asr"  # Automatic Speech Recognition


class CaptionStatus(Enum):
    """Caption status."""
    SERVING = "serving"
    SYNCING = "syncing"
    FAILED = "failed"


class CaptionFormat(Enum):
    """Caption formats supported by YouTube API."""
    SRT = "srt"  # SubRip subtitle
    VTT = "vtt"  # Web Video Text Tracks caption
    TTML = "ttml"  # Timed Text Markup Language caption
    SBV = "sbv"  # SubViewer subtitle
    SCC = "scc"  # Scenarist Closed Caption format
    TXT = "txt"  # Plain text (converted)


class CaptionQuality(Enum):
    """Caption quality levels."""
    EXCELLENT = "excellent"
    GOOD = "good"
    FAIR = "fair"
    POOR = "poor"
    UNKNOWN = "unknown"


@dataclass
class CaptionTranslation:
    """Caption translation information."""
    source_language: str
    target_language: str
    is_machine_translated: bool = True
    translation_service: str = "google_translate"
    confidence_score: Optional[float] = None
    
    @property
    def translation_direction(self) -> str:
        """Get translation direction string."""
        return f"{self.source_language} -> {self.target_language}"


@dataclass
class CaptionDownloadOptions:
    """Advanced caption download options."""
    caption_id: str
    format: CaptionFormat = CaptionFormat.SRT
    target_language: Optional[str] = None  # For translation
    on_behalf_of_content_owner: Optional[str] = None
    validate_format: bool = True
    include_metadata: bool = True
    
    def validate_options(self) -> List[str]:
        """Validate download options."""
        errors = []
        
        if not self.caption_id:
            errors.append("Caption ID is required")
        
        if self.target_language and len(self.target_language) != 2:
            errors.append("Target language must be a 2-letter ISO code")
        
        return errors


@dataclass
class CaptionQualityMetrics:
    """Caption quality assessment metrics."""
    overall_quality: CaptionQuality = CaptionQuality.UNKNOWN
    timing_accuracy: float = 0.0  # 0-1 score
    text_quality: float = 0.0  # 0-1 score
    completeness: float = 0.0  # 0-1 score
    consistency: float = 0.0  # 0-1 score
    issues: List[str] = field(default_factory=list)
    
    @property
    def average_score(self) -> float:
        """Get average quality score."""
        scores = [self.timing_accuracy, self.text_quality, self.completeness, self.consistency]
        return sum(scores) / len(scores) if scores else 0.0
    
    def get_quality_summary(self) -> Dict[str, Any]:
        """Get quality summary."""
        return {
            'overall_quality': self.overall_quality.value,
            'average_score': self.average_score,
            'timing_accuracy': self.timing_accuracy,
            'text_quality': self.text_quality,
            'completeness': self.completeness,
            'consistency': self.consistency,
            'issues_count': len(self.issues),
            'issues': self.issues
        }


@dataclass
class CaptionTrack:
    """Individual caption track information."""
    caption_id: str
    language: str
    language_code: str
    name: str
    track_type: CaptionTrackType
    status: CaptionStatus
    is_auto_generated: bool
    is_cc: bool
    is_draft: bool
    is_easy_reader: bool
    is_large: bool
    last_updated: Optional[datetime] = None
    
    @property
    def is_manual(self) -> bool:
        """Check if this is a manually created caption track."""
        return not self.is_auto_generated
    
    @property
    def is_accessible(self) -> bool:
        """Check if this caption track is accessible."""
        return self.status == CaptionStatus.SERVING
    
    @property
    def display_name(self) -> str:
        """Get display name for the caption track."""
        if self.name:
            return f"{self.name} ({self.language})"
        return self.language


@dataclass
class CaptionCue:
    """Individual caption cue/timestamp."""
    start_time: float  # seconds
    end_time: float    # seconds
    text: str
    speaker: Optional[str] = None
    
    @property
    def duration(self) -> float:
        """Get cue duration in seconds."""
        return self.end_time - self.start_time
    
    @property
    def formatted_start(self) -> str:
        """Get formatted start time (HH:MM:SS,mmm)."""
        return self._format_time(self.start_time)
    
    @property
    def formatted_end(self) -> str:
        """Get formatted end time (HH:MM:SS,mmm)."""
        return self._format_time(self.end_time)
    
    def _format_time(self, seconds: float) -> str:
        """Format seconds to HH:MM:SS,mmm format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"


@dataclass
class CaptionContent:
    """Caption content with cues and metadata."""
    caption_id: str
    language: str
    language_code: str
    cues: List[CaptionCue] = field(default_factory=list)
    format: CaptionFormat = CaptionFormat.SRT
    raw_content: Optional[str] = None
    
    @property
    def total_duration(self) -> float:
        """Get total caption duration in seconds."""
        if not self.cues:
            return 0.0
        return max(cue.end_time for cue in self.cues)
    
    @property
    def word_count(self) -> int:
        """Get total word count."""
        return sum(len(cue.text.split()) for cue in self.cues)
    
    @property
    def cue_count(self) -> int:
        """Get number of cues."""
        return len(self.cues)
    
    @property
    def average_cue_duration(self) -> float:
        """Get average cue duration."""
        if not self.cues:
            return 0.0
        return sum(cue.duration for cue in self.cues) / len(self.cues)
    
    def get_cues_in_timeframe(self, start_time: float, end_time: float) -> List[CaptionCue]:
        """Get cues within a specific timeframe."""
        return [
            cue for cue in self.cues
            if cue.start_time >= start_time and cue.end_time <= end_time
        ]
    
    def search_text(self, search_term: str, case_sensitive: bool = False) -> List[CaptionCue]:
        """Search for text within captions."""
        if not case_sensitive:
            search_term = search_term.lower()
        
        matching_cues = []
        for cue in self.cues:
            cue_text = cue.text if case_sensitive else cue.text.lower()
            if search_term in cue_text:
                matching_cues.append(cue)
        
        return matching_cues


@dataclass
class CaptionFilters:
    """Advanced caption filtering options."""
    # Language filtering
    language_codes: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    
    # Track type filtering
    track_types: Optional[List[CaptionTrackType]] = None
    auto_generated_only: Optional[bool] = None
    manual_only: Optional[bool] = None
    
    # Status filtering
    statuses: Optional[List[CaptionStatus]] = None
    accessible_only: bool = True
    
    # Feature filtering
    cc_only: Optional[bool] = None
    draft_only: Optional[bool] = None
    easy_reader_only: Optional[bool] = None
    large_only: Optional[bool] = None
    
    def validate_filters(self) -> List[str]:
        """Validate filter combinations."""
        errors = []
        
        if self.auto_generated_only and self.manual_only:
            errors.append("Cannot filter for both auto-generated and manual captions")
        
        if self.draft_only and self.accessible_only:
            errors.append("Draft captions are not accessible")
        
        return errors


@dataclass
class CaptionAnalytics:
    """Caption analytics and insights."""
    total_tracks: int = 0
    available_tracks: int = 0
    auto_generated_tracks: int = 0
    manual_tracks: int = 0
    languages: List[str] = field(default_factory=list)
    language_distribution: Dict[str, int] = field(default_factory=dict)
    total_duration: float = 0.0
    total_word_count: int = 0
    average_words_per_minute: float = 0.0
    cue_statistics: Dict[str, float] = field(default_factory=dict)
    
    def calculate_words_per_minute(self) -> float:
        """Calculate words per minute."""
        if self.total_duration == 0:
            return 0.0
        return (self.total_word_count / self.total_duration) * 60
    
    def get_language_summary(self) -> Dict[str, Any]:
        """Get language distribution summary."""
        return {
            'total_languages': len(self.languages),
            'languages': self.languages,
            'distribution': self.language_distribution,
            'most_common': max(self.language_distribution.items(), key=lambda x: x[1])[0] if self.language_distribution else None
        }


@dataclass
class CaptionResult:
    """Comprehensive caption result with analytics."""
    tracks: List[CaptionTrack] = field(default_factory=list)
    content: Optional[CaptionContent] = None
    analytics: Optional[CaptionAnalytics] = None
    filters_applied: Optional[CaptionFilters] = None
    quota_cost: int = 50  # Captions API costs 50 units per request
    
    @property
    def available_tracks(self) -> List[CaptionTrack]:
        """Get only accessible caption tracks."""
        return [track for track in self.tracks if track.is_accessible]
    
    @property
    def auto_generated_tracks(self) -> List[CaptionTrack]:
        """Get auto-generated caption tracks."""
        return [track for track in self.tracks if track.is_auto_generated]
    
    @property
    def manual_tracks(self) -> List[CaptionTrack]:
        """Get manually created caption tracks."""
        return [track for track in self.tracks if track.is_manual]
    
    def get_tracks_by_language(self, language_code: str) -> List[CaptionTrack]:
        """Get tracks by language code."""
        return [track for track in self.tracks if track.language_code == language_code]
    
    def get_best_track(self, preferred_language: str = 'en') -> Optional[CaptionTrack]:
        """Get the best available track (manual > auto, preferred language)."""
        available = self.available_tracks
        
        # Try to find manual track in preferred language
        for track in available:
            if track.is_manual and track.language_code == preferred_language:
                return track
        
        # Try to find any manual track
        for track in available:
            if track.is_manual:
                return track
        
        # Fall back to auto-generated in preferred language
        for track in available:
            if track.language_code == preferred_language:
                return track
        
        # Return first available track
        return available[0] if available else None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'tracks': [
                {
                    'caption_id': track.caption_id,
                    'language': track.language,
                    'language_code': track.language_code,
                    'name': track.name,
                    'track_type': track.track_type.value,
                    'status': track.status.value,
                    'is_auto_generated': track.is_auto_generated,
                    'is_cc': track.is_cc,
                    'is_draft': track.is_draft,
                    'is_easy_reader': track.is_easy_reader,
                    'is_large': track.is_large,
                    'last_updated': track.last_updated.isoformat() if track.last_updated else None,
                    'display_name': track.display_name
                } for track in self.tracks
            ],
            'content': {
                'caption_id': self.content.caption_id,
                'language': self.content.language,
                'language_code': self.content.language_code,
                'format': self.content.format.value,
                'total_duration': self.content.total_duration,
                'word_count': self.content.word_count,
                'cue_count': self.content.cue_count,
                'average_cue_duration': self.content.average_cue_duration,
                'cues': [
                    {
                        'start_time': cue.start_time,
                        'end_time': cue.end_time,
                        'duration': cue.duration,
                        'text': cue.text,
                        'formatted_start': cue.formatted_start,
                        'formatted_end': cue.formatted_end
                    } for cue in self.content.cues
                ]
            } if self.content else None,
            'analytics': {
                'total_tracks': self.analytics.total_tracks,
                'available_tracks': self.analytics.available_tracks,
                'auto_generated_tracks': self.analytics.auto_generated_tracks,
                'manual_tracks': self.analytics.manual_tracks,
                'languages': self.analytics.languages,
                'language_distribution': self.analytics.language_distribution,
                'total_duration': self.analytics.total_duration,
                'total_word_count': self.analytics.total_word_count,
                'words_per_minute': self.analytics.calculate_words_per_minute()
            } if self.analytics else None,
            'quota_cost': self.quota_cost
        }


class CaptionFormatConverter:
    """Convert between different caption formats."""
    
    @staticmethod
    def srt_to_vtt(srt_content: str) -> str:
        """Convert SRT format to WebVTT format."""
        lines = srt_content.strip().split('\n')
        vtt_lines = ['WEBVTT', '']
        
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():  # Cue number
                i += 1
                if i < len(lines):
                    # Time line
                    time_line = lines[i].replace(',', '.')
                    vtt_lines.append(time_line)
                    i += 1
                    # Text lines
                    text_lines = []
                    while i < len(lines) and lines[i].strip():
                        text_lines.append(lines[i])
                        i += 1
                    vtt_lines.extend(text_lines)
                    vtt_lines.append('')
            else:
                i += 1
        
        return '\n'.join(vtt_lines)
    
    @staticmethod
    def srt_to_txt(srt_content: str) -> str:
        """Convert SRT format to plain text."""
        lines = srt_content.strip().split('\n')
        text_lines = []
        
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():  # Cue number
                i += 2  # Skip number and time
                # Collect text lines
                while i < len(lines) and lines[i].strip():
                    text_lines.append(lines[i])
                    i += 1
            else:
                i += 1
        
        return '\n'.join(text_lines)
    
    @staticmethod
    def srt_to_sbv(srt_content: str) -> str:
        """Convert SRT format to SubViewer (SBV) format."""
        lines = srt_content.strip().split('\n')
        sbv_lines = []
        
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():  # Cue number
                i += 1
                if i < len(lines):
                    # Parse time line
                    time_line = lines[i]
                    start_time, end_time = CaptionFormatConverter._parse_srt_time(time_line)
                    sbv_time = f"{CaptionFormatConverter._format_sbv_time(start_time)},{CaptionFormatConverter._format_sbv_time(end_time)}"
                    i += 1
                    
                    # Collect text lines
                    text_lines = []
                    while i < len(lines) and lines[i].strip():
                        text_lines.append(lines[i])
                        i += 1
                    
                    if text_lines:
                        sbv_lines.append(sbv_time)
                        sbv_lines.append('\n'.join(text_lines))
                        sbv_lines.append('')
        
        return '\n'.join(sbv_lines)
    
    @staticmethod
    def srt_to_ttml(srt_content: str) -> str:
        """Convert SRT format to TTML format."""
        lines = srt_content.strip().split('\n')
        cues = CaptionFormatConverter.parse_srt(srt_content)
        
        ttml_lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<tt xmlns="http://www.w3.org/ns/ttml" xmlns:tts="http://www.w3.org/ns/ttml#styling">',
            '  <head>',
            '    <styling>',
            '      <style id="default" tts:fontSize="16px" tts:color="white"/>',
            '    </styling>',
            '  </head>',
            '  <body>',
            '    <div>'
        ]
        
        for cue in cues:
            start_time = CaptionFormatConverter._format_ttml_time(cue.start_time)
            end_time = CaptionFormatConverter._format_ttml_time(cue.end_time)
            text = cue.text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            ttml_lines.append(f'      <p begin="{start_time}" end="{end_time}">{text}</p>')
        
        ttml_lines.extend([
            '    </div>',
            '  </body>',
            '</tt>'
        ])
        
        return '\n'.join(ttml_lines)
    
    @staticmethod
    def _format_sbv_time(seconds: float) -> str:
        """Format time for SBV format (HH:MM:SS.mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    @staticmethod
    def _format_ttml_time(seconds: float) -> str:
        """Format time for TTML format (HH:MM:SS.mmm)."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{millis:03d}"
    
    @staticmethod
    def validate_format(content: str, format_type: CaptionFormat) -> Dict[str, Any]:
        """Validate caption format."""
        validation_result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'stats': {}
        }
        
        try:
            if format_type == CaptionFormat.SRT:
                cues = CaptionFormatConverter.parse_srt(content)
                validation_result['stats'] = {
                    'cue_count': len(cues),
                    'total_duration': max(cue.end_time for cue in cues) if cues else 0,
                    'average_cue_duration': sum(cue.duration for cue in cues) / len(cues) if cues else 0
                }
                
                # Check for common SRT issues
                if not cues:
                    validation_result['errors'].append("No valid cues found")
                    validation_result['is_valid'] = False
                
                # Check for timing issues
                for i, cue in enumerate(cues):
                    if cue.start_time >= cue.end_time:
                        validation_result['errors'].append(f"Cue {i+1}: Start time >= End time")
                        validation_result['is_valid'] = False
                    
                    if cue.duration > 10:  # Very long cue
                        validation_result['warnings'].append(f"Cue {i+1}: Very long duration ({cue.duration:.1f}s)")
            
            elif format_type == CaptionFormat.VTT:
                if not content.startswith('WEBVTT'):
                    validation_result['errors'].append("Missing WEBVTT header")
                    validation_result['is_valid'] = False
            
            elif format_type == CaptionFormat.TTML:
                if '<?xml' not in content or '<tt' not in content:
                    validation_result['errors'].append("Invalid TTML format")
                    validation_result['is_valid'] = False
        
        except Exception as e:
            validation_result['is_valid'] = False
            validation_result['errors'].append(f"Validation error: {str(e)}")
        
        return validation_result
    
    @staticmethod
    def parse_srt(srt_content: str) -> List[CaptionCue]:
        """Parse SRT content into CaptionCue objects."""
        lines = srt_content.strip().split('\n')
        cues = []
        
        i = 0
        while i < len(lines):
            if lines[i].strip().isdigit():  # Cue number
                i += 1
                if i < len(lines):
                    # Parse time line
                    time_line = lines[i]
                    start_time, end_time = CaptionFormatConverter._parse_srt_time(time_line)
                    i += 1
                    
                    # Collect text lines
                    text_lines = []
                    while i < len(lines) and lines[i].strip():
                        text_lines.append(lines[i])
                        i += 1
                    
                    if text_lines:
                        cue = CaptionCue(
                            start_time=start_time,
                            end_time=end_time,
                            text=' '.join(text_lines)
                        )
                        cues.append(cue)
            else:
                i += 1
        
        return cues
    
    @staticmethod
    def _parse_srt_time(time_line: str) -> tuple[float, float]:
        """Parse SRT time format (HH:MM:SS,mmm --> HH:MM:SS,mmm)."""
        # Remove arrow and split
        start_str, end_str = time_line.split(' --> ')
        
        def parse_time(time_str: str) -> float:
            # Replace comma with dot for milliseconds
            time_str = time_str.replace(',', '.')
            # Parse HH:MM:SS.mmm
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            seconds_parts = parts[2].split('.')
            seconds = int(seconds_parts[0])
            milliseconds = int(seconds_parts[1]) if len(seconds_parts) > 1 else 0
            
            return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        
        return parse_time(start_str), parse_time(end_str)


class CaptionAnalyzer:
    """Analyze caption content for insights."""
    
    @staticmethod
    def analyze_language(content: str) -> Dict[str, Any]:
        """Simple language detection based on common words."""
        # Common words in different languages
        language_indicators = {
            'en': ['the', 'and', 'is', 'in', 'to', 'of', 'a', 'that', 'it', 'with'],
            'es': ['el', 'la', 'de', 'que', 'y', 'a', 'en', 'un', 'es', 'se'],
            'fr': ['le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir'],
            'de': ['der', 'die', 'und', 'in', 'den', 'von', 'zu', 'das', 'mit', 'sich'],
            'it': ['il', 'di', 'e', 'a', 'in', 'un', 'per', 'è', 'con', 'da'],
            'pt': ['o', 'de', 'e', 'do', 'da', 'em', 'um', 'para', 'com', 'não'],
            'ru': ['и', 'в', 'не', 'на', 'я', 'быть', 'с', 'он', 'а', 'как'],
            'ja': ['の', 'に', 'は', 'を', 'が', 'で', 'と', 'も', 'から', 'まで'],
            'ko': ['이', '그', '저', '의', '에', '를', '을', '가', '는', '은'],
            'zh': ['的', '了', '在', '是', '我', '有', '和', '就', '不', '人']
        }
        
        content_lower = content.lower()
        word_counts = {}
        
        for lang, words in language_indicators.items():
            count = sum(content_lower.count(word) for word in words)
            word_counts[lang] = count
        
        # Return language with highest count
        detected_lang = max(word_counts.items(), key=lambda x: x[1])[0]
        confidence = word_counts[detected_lang] / len(content.split()) if content.split() else 0
        
        return {
            'detected_language': detected_lang,
            'confidence': confidence,
            'word_counts': word_counts
        }
    
    @staticmethod
    def analyze_reading_speed(cues: List[CaptionCue]) -> Dict[str, float]:
        """Analyze reading speed and timing."""
        if not cues:
            return {'average_wpm': 0.0, 'average_cue_duration': 0.0}
        
        total_words = sum(len(cue.text.split()) for cue in cues)
        total_duration = sum(cue.duration for cue in cues)
        
        average_wpm = (total_words / total_duration * 60) if total_duration > 0 else 0.0
        average_cue_duration = total_duration / len(cues)
        
        return {
            'average_wpm': average_wpm,
            'average_cue_duration': average_cue_duration,
            'total_words': total_words,
            'total_duration': total_duration
        }
    
    @staticmethod
    def find_gaps(cues: List[CaptionCue], min_gap: float = 0.5) -> List[Dict[str, float]]:
        """Find gaps between caption cues."""
        gaps = []
        
        for i in range(len(cues) - 1):
            current_end = cues[i].end_time
            next_start = cues[i + 1].start_time
            
            if next_start - current_end >= min_gap:
                gaps.append({
                    'start': current_end,
                    'end': next_start,
                    'duration': next_start - current_end
                })
        
        return gaps


class CaptionQualityAssessor:
    """Assess caption quality and provide recommendations."""
    
    @staticmethod
    def assess_quality(cues: List[CaptionCue], content: str) -> CaptionQualityMetrics:
        """Assess overall caption quality."""
        metrics = CaptionQualityMetrics()
        
        if not cues:
            metrics.overall_quality = CaptionQuality.POOR
            metrics.issues.append("No caption cues found")
            return metrics
        
        # Assess timing accuracy
        timing_score = CaptionQualityAssessor._assess_timing_accuracy(cues)
        metrics.timing_accuracy = timing_score
        
        # Assess text quality
        text_score = CaptionQualityAssessor._assess_text_quality(cues, content)
        metrics.text_quality = text_score
        
        # Assess completeness
        completeness_score = CaptionQualityAssessor._assess_completeness(cues)
        metrics.completeness = completeness_score
        
        # Assess consistency
        consistency_score = CaptionQualityAssessor._assess_consistency(cues)
        metrics.consistency = consistency_score
        
        # Determine overall quality
        avg_score = metrics.average_score
        if avg_score >= 0.9:
            metrics.overall_quality = CaptionQuality.EXCELLENT
        elif avg_score >= 0.7:
            metrics.overall_quality = CaptionQuality.GOOD
        elif avg_score >= 0.5:
            metrics.overall_quality = CaptionQuality.FAIR
        else:
            metrics.overall_quality = CaptionQuality.POOR
        
        return metrics
    
    @staticmethod
    def _assess_timing_accuracy(cues: List[CaptionCue]) -> float:
        """Assess timing accuracy (0-1 score)."""
        if not cues:
            return 0.0
        
        score = 1.0
        issues = 0
        
        for cue in cues:
            # Check for invalid timing
            if cue.start_time >= cue.end_time:
                issues += 1
                continue
            
            # Check for very short cues (< 0.5s)
            if cue.duration < 0.5:
                issues += 0.5
            
            # Check for very long cues (> 10s)
            if cue.duration > 10:
                issues += 0.5
        
        # Calculate score based on issues
        if issues > 0:
            score = max(0.0, 1.0 - (issues / len(cues)))
        
        return score
    
    @staticmethod
    def _assess_text_quality(cues: List[CaptionCue], content: str) -> float:
        """Assess text quality (0-1 score)."""
        if not cues:
            return 0.0
        
        score = 1.0
        issues = 0
        
        for cue in cues:
            text = cue.text.strip()
            
            # Check for empty cues
            if not text:
                issues += 1
                continue
            
            # Check for very short text
            if len(text) < 2:
                issues += 0.5
            
            # Check for excessive length
            if len(text) > 200:
                issues += 0.5
            
            # Check for common issues
            if text.count('\n') > 3:  # Too many line breaks
                issues += 0.3
            
            if text.count('[') != text.count(']'):  # Unmatched brackets
                issues += 0.2
        
        # Calculate score based on issues
        if issues > 0:
            score = max(0.0, 1.0 - (issues / len(cues)))
        
        return score
    
    @staticmethod
    def _assess_completeness(cues: List[CaptionCue]) -> float:
        """Assess completeness (0-1 score)."""
        if not cues:
            return 0.0
        
        # Check for gaps
        gaps = CaptionAnalyzer.find_gaps(cues, min_gap=1.0)
        
        # Calculate completeness based on gaps
        if gaps:
            total_gap_time = sum(gap['duration'] for gap in gaps)
            total_duration = max(cue.end_time for cue in cues)
            gap_ratio = total_gap_time / total_duration if total_duration > 0 else 0
            return max(0.0, 1.0 - gap_ratio)
        
        return 1.0
    
    @staticmethod
    def _assess_consistency(cues: List[CaptionCue]) -> float:
        """Assess consistency (0-1 score)."""
        if not cues:
            return 0.0
        
        # Check duration consistency
        durations = [cue.duration for cue in cues]
        avg_duration = sum(durations) / len(durations)
        
        # Calculate variance
        variance = sum((d - avg_duration) ** 2 for d in durations) / len(durations)
        std_dev = variance ** 0.5
        
        # Score based on consistency (lower std dev = higher score)
        consistency_score = max(0.0, 1.0 - (std_dev / avg_duration) if avg_duration > 0 else 0)
        
        return consistency_score
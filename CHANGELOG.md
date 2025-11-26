# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-11-26

### Added
- Initial public release
- Multi-backend architecture (PyTubeFix, yt-dlp, YouTube API)
- Automatic fallback between backends
- Audio download (WAV, MP3, M4A formats)
- Video download (multiple quality options)
- Video information extraction
- YouTube search with filters
- Caption/subtitle extraction and conversion (SRT, VTT, TXT, TTML)
- Comment retrieval with pagination and analytics
- Playlist processing
- Anti-detection measures (rate limiting, user-agent rotation)
- Progress tracking for downloads
- Advanced search filters (Boolean queries, categories, live content)
- Comment analytics and sentiment analysis
- Caption analytics and format conversion
- LICENSE file (MIT)
- CHANGELOG.md for version tracking
- CONTRIBUTING.md with contribution guidelines
- Comprehensive pytest test suite
- requirements.txt for pip users

### Core Features
- `YouTubeToolkit` - Main interface class
- `VideoInfo` - Standardized video information dataclass
- `DownloadResult` - Standardized download result dataclass
- `SearchResult` - Standardized search result dataclass
- `SearchFilters` - Advanced search filtering
- `CommentFilters` - Comment filtering options
- `CaptionFilters` - Caption filtering options

### Handlers
- `PyTubeFixHandler` - Primary download backend
- `YTDLPHandler` - Fallback download backend
- `YouTubeAPIHandler` - Official API for metadata and search

[Unreleased]: https://github.com/rhythmculture/youtube-toolkit/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/rhythmculture/youtube-toolkit/releases/tag/v0.1.0

# YouTube Toolkit

A robust Python toolkit for downloading YouTube content with automatic fallback between multiple backends. Built for reliability and ease of use.

## What This Package Does

YouTube Toolkit automatically handles YouTube operations by trying multiple methods in sequence:
- **PyTubeFix** - Fast and reliable primary method
- **YT-DLP** - Robust fallback with advanced features
- **YouTube API** - Official API for metadata and search

If one method fails, it automatically tries the next one, ensuring your operations succeed.

## Key Features

- **5 Core APIs** - Get, Download, Search, Analyze, Stream
- **Audio Download** - Download audio in WAV, MP3, or M4A formats
- **Video Download** - Download videos in various qualities (720p, 1080p, etc.)
- **Video Information** - Get video details, duration, views, etc.
- **Search Videos** - Search YouTube with filters and trending
- **Analyze Content** - SponsorBlock segments, engagement heatmaps, metadata
- **Stream to Buffer** - Stream audio/video to memory without saving to disk
- **Live Streams** - Check status and download live streams
- **Automatic Fallback** - If one method fails, tries another automatically

## Installation

### Prerequisites

**Python 3.10+** is required.

```bash
# Install FFmpeg (required for audio conversion)
# Ubuntu/Debian
sudo apt update && sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

### Install the Package

```bash
# Install directly from GitHub with uv (recommended)
uv pip install git+https://github.com/rhythmculture/youtube-toolkit.git

# Or install a specific version
uv pip install git+https://github.com/rhythmculture/youtube-toolkit.git@v1.0.0

# Or with pip
pip install git+https://github.com/rhythmculture/youtube-toolkit.git
```

### YouTube API Setup (Required for some features)

Some features require a YouTube API key (trending, categories, regions, languages, comments via API).

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **YouTube Data API v3**
4. Go to **Credentials** → **Create Credentials** → **API Key**
5. Copy the API key and set it as an environment variable:

```bash
# Option 1: Create a .env file in your project directory
echo "YOUTUBE_API_KEY=your_api_key_here" > .env

# Option 2: Export directly (Linux/macOS)
export YOUTUBE_API_KEY=your_api_key_here

# Option 3: Set in Windows
set YOUTUBE_API_KEY=your_api_key_here
```

**Note**: Most features work without an API key. The API key is only needed for:
- `search.trending()`, `search.categories()`, `search.regions()`, `search.languages()`
- `analyze.comments()` via YouTube API (yt-dlp fallback works without key)
- `get.comments()` via YouTube API

## Quick Start - 5 Core APIs

```python
from youtube_toolkit import YouTubeToolkit

toolkit = YouTubeToolkit()
```

### 1. GET - Retrieve Information

```python
# Smart auto-detect
video = toolkit.get("https://youtube.com/watch?v=example")
print(f"{video.title} - {video.duration}s")

# Explicit methods
chapters = toolkit.get.chapters(url)
transcript = toolkit.get.transcript(url)
comments = toolkit.get.comments(url, max_results=50)
captions = toolkit.get.captions(url)
formats = toolkit.get.formats(url)           # Available download formats
keywords = toolkit.get.keywords(url)         # Video tags
restriction = toolkit.get.restriction(url)   # Age/region restrictions
embed_url = toolkit.get.embed_url(url)       # Embeddable URL

# Channel operations
channel_videos = toolkit.get.channel.videos("@Fireship", limit=50)
channel_info = toolkit.get.channel("@Fireship")
channel_shorts = toolkit.get.channel.shorts("@Fireship")

# Playlist operations
playlist_videos = toolkit.get.playlist.videos(playlist_url)
playlist_info = toolkit.get.playlist.info(playlist_url)
```

### 2. DOWNLOAD - Save Content to Disk

```python
# Smart download (returns DownloadResult)
result = toolkit.download(url, type='audio', format='mp3')
if result.success:
    print(f"Downloaded to: {result.file_path}")

# Explicit methods (return file paths)
audio_path = toolkit.download.audio(url, format='mp3', bitrate='192k')
video_path = toolkit.download.video(url, quality='720p')
caption_path = toolkit.download.captions(url, lang='en')
thumb_path = toolkit.download.thumbnail(url)
results = toolkit.download.playlist(url, type='audio')

# Advanced downloads
toolkit.download.shorts(url)                              # YouTube Shorts
toolkit.download.live(url, from_start=True)               # Live streams
toolkit.download.with_sponsorblock(url, action='remove')  # Skip sponsors
toolkit.download.with_metadata(url, embed_thumbnail=True) # With ID3 tags
toolkit.download.with_filter(url, match_filter="duration > 600")
toolkit.download.with_archive(url, archive_file="downloaded.txt")
toolkit.download.with_cookies(url, browser='chrome')      # Age-restricted
```

### 3. SEARCH - Find Content

```python
# Smart search (returns SearchResult)
results = toolkit.search("python tutorial", max_results=10)
for item in results.items:
    print(f"- {item.title}")

# Explicit methods
videos = toolkit.search.videos("python tutorial", limit=20)
channels = toolkit.search.channels("python")
playlists = toolkit.search.playlists("python course")

# Advanced search with filters
filtered = toolkit.search.with_filters(
    "python tutorial",
    duration='medium',      # 'short', 'medium', 'long'
    upload_date='month',    # 'hour', 'today', 'week', 'month', 'year'
    sort_by='views'         # 'relevance', 'date', 'views', 'rating'
)

# Search autocomplete suggestions
suggestions = toolkit.search.suggestions("python tut")

# Trending content (requires YouTube API key)
trending = toolkit.search.trending()                    # Trending videos
trending_by_cat = toolkit.search.trending.by_category() # By category
categories = toolkit.search.categories()                # Video categories
regions = toolkit.search.regions()                      # Supported regions
languages = toolkit.search.languages()                  # Supported languages
```

### 4. ANALYZE - Analyze Content

```python
# Full metadata analysis
metadata = toolkit.analyze(url)                    # 50+ fields
metadata = toolkit.analyze.metadata(url)           # Same as above

# Engagement data
engagement = toolkit.analyze.engagement(url)       # Heatmap + key moments
print(engagement['heatmap'])                       # Most replayed sections
print(engagement['key_moments'])                   # AI-generated moments

# Other analysis
comments = toolkit.analyze.comments(url, max_comments=100, sort='relevance')
captions = toolkit.analyze.captions(url)
segments = toolkit.analyze.sponsorblock(url)       # Sponsor segments
channel = toolkit.analyze.channel("@Fireship")     # Channel analytics
filesize = toolkit.analyze.filesize(url)           # Preview filesizes
```

### 5. STREAM - Stream to Buffer

```python
# Stream audio/video to memory (no file saved)
audio_bytes = toolkit.stream(url)                  # Audio buffer (default)
audio_bytes = toolkit.stream.audio(url, quality='best')
video_bytes = toolkit.stream.video(url, quality='720p')

# Live stream operations
status = toolkit.stream.live.status(url)           # Live stream info
is_live = toolkit.stream.live.is_live(url)         # Check if live
path = toolkit.stream.live.download(url, from_start=True)
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│           Consolidated API v1.0 (sub_apis.py)               │
│     GetAPI │ DownloadAPI │ SearchAPI │ AnalyzeAPI │ StreamAPI│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (api.py)                       │
│         YouTubeToolkit (Unified Interface)                  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Backend Layer (handlers/)                    │
├─────────────┬─────────────┬──────────────┬─────────────────┤
│ PyTubeFix   │   YT-DLP    │ YouTube API  │  ScrapeTube     │
│  Handler    │   Handler   │   Handler    │   Handler       │
│ (Primary)   │ (Fallback)  │ (Metadata)   │ (Optional)      │
└─────────────┴─────────────┴──────────────┴─────────────────┘
```

## API Reference

### GET API
| Method | Returns | Description |
|--------|---------|-------------|
| `get(url)` | `VideoInfo` | Smart auto-detect video info |
| `get.video(url)` | `VideoInfo` | Video metadata |
| `get.chapters(url)` | `List[Dict]` | Video chapters |
| `get.transcript(url)` | `str` | Video transcript |
| `get.comments(url)` | `CommentResult` | Video comments |
| `get.captions(url)` | `CaptionResult` | Available captions |
| `get.formats(url)` | `Dict` | Available formats |
| `get.keywords(url)` | `List[str]` | Video tags |
| `get.restriction(url)` | `Dict` | Age/region restrictions |
| `get.embed_url(url)` | `str` | Embed URL |
| `get.channel(channel)` | `Dict` | Channel info |
| `get.channel.videos(channel)` | `List[Dict]` | Channel videos |
| `get.channel.shorts(channel)` | `List[Dict]` | Channel shorts |
| `get.playlist.videos(url)` | `List[Dict]` | Playlist videos |
| `get.playlist.info(url)` | `Dict` | Playlist info |

### DOWNLOAD API
| Method | Returns | Description |
|--------|---------|-------------|
| `download(url, type, format)` | `DownloadResult` | Smart download |
| `download.audio(url, format)` | `str` | Download audio |
| `download.video(url, quality)` | `str` | Download video |
| `download.captions(url, lang)` | `str` | Download captions |
| `download.thumbnail(url)` | `str` | Download thumbnail |
| `download.playlist(url)` | `Dict` | Download playlist |
| `download.shorts(url)` | `str` | Download YouTube Short |
| `download.live(url)` | `str` | Download live stream |
| `download.with_sponsorblock(url)` | `str` | Skip sponsors |
| `download.with_metadata(url)` | `str` | With ID3 tags |
| `download.with_filter(url)` | `str` | With match filter |
| `download.with_archive(url)` | `str` | Track downloads |
| `download.with_cookies(url)` | `str` | Use browser cookies |

### SEARCH API
| Method | Returns | Description |
|--------|---------|-------------|
| `search(query)` | `SearchResult` | Smart search |
| `search.videos(query)` | `List[Dict]` | Search videos |
| `search.channels(query)` | `List[Dict]` | Search channels |
| `search.playlists(query)` | `List[Dict]` | Search playlists |
| `search.with_filters(query)` | `Dict` | Filtered search |
| `search.suggestions(query)` | `List[str]` | Autocomplete |
| `search.trending()` | `Dict` | Trending videos |
| `search.trending.by_category()` | `Dict` | Trending by category |
| `search.categories()` | `List[Dict]` | Video categories |
| `search.regions()` | `List[Dict]` | Supported regions |
| `search.languages()` | `List[Dict]` | Supported languages |

### ANALYZE API
| Method | Returns | Description |
|--------|---------|-------------|
| `analyze(url)` | `Dict` | Full metadata |
| `analyze.metadata(url)` | `Dict` | 50+ field metadata |
| `analyze.engagement(url)` | `Dict` | Heatmap + key moments |
| `analyze.comments(url)` | `CommentResult` | Comment analytics |
| `analyze.captions(url)` | `CaptionResult` | Caption analysis |
| `analyze.sponsorblock(url)` | `List[Dict]` | Sponsor segments |
| `analyze.channel(channel)` | `Dict` | Channel analytics |
| `analyze.filesize(url)` | `Dict` | Filesize preview |

### STREAM API
| Method | Returns | Description |
|--------|---------|-------------|
| `stream(url)` | `bytes` | Stream to buffer |
| `stream.audio(url)` | `bytes` | Stream audio |
| `stream.video(url)` | `bytes` | Stream video |
| `stream.live.status(url)` | `Dict` | Live stream status |
| `stream.live.is_live(url)` | `bool` | Check if live |
| `stream.live.download(url)` | `str` | Download live |

## Legacy API (Still Supported)

```python
# These methods still work for backward compatibility
video = toolkit.get_video(url)               # VideoInfo dataclass
result = toolkit.download(url, type='audio') # DownloadResult
results = toolkit.search('query')            # SearchResult
audio_path = toolkit.download_audio(url)     # str path
video_path = toolkit.download_video(url)     # str path
info = toolkit.get_video_info(url)           # Dict
```

## Troubleshooting

### FFmpeg Not Found
```bash
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

### YouTube API Key
```bash
echo "YOUTUBE_API_KEY=your_api_key_here" > .env
```

### Test Your Setup
```python
status = toolkit.test_handlers('https://youtube.com/watch?v=example')
print(status)
```

## Project Structure
```
youtube-toolkit/
├── youtube_toolkit/
│   ├── api.py              # YouTubeToolkit class
│   ├── sub_apis.py         # 5 Core APIs: Get, Download, Search, Analyze, Stream
│   ├── handlers/           # Backend handlers
│   │   ├── pytubefix_handler.py
│   │   ├── yt_dlp_handler.py
│   │   ├── youtube_api_handler.py
│   │   └── scrapetube_handler.py
│   ├── core/               # Data structures
│   └── utils/              # Utilities
├── tests/                  # Test suite (200+ tests)
└── README.md
```

## License

MIT License - see the LICENSE file for details.

## Acknowledgments

- **PyTubeFix** - Primary download engine
- **YT-DLP** - Advanced download backend
- **MoviePy** - Video processing
- **FFmpeg** - Audio/video conversion

---

**Happy downloading!**

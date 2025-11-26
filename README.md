# YouTube Toolkit

A robust Python toolkit for downloading YouTube content with automatic fallback between multiple backends. Built for reliability and ease of use.

## 🎯 What This Package Does

YouTube Toolkit automatically handles YouTube downloads by trying multiple methods in sequence:
- **PyTubeFix** - Fast and reliable primary method
- **YT-DLP** - Robust fallback with advanced features
- **YouTube API** - Official API for metadata and search

If one method fails, it automatically tries the next one, ensuring your downloads succeed.

## 🚀 Key Features

- **Audio Download** - Download audio in WAV, MP3, or M4A formats
- **Video Download** - Download videos in various qualities (720p, 1080p, etc.)
- **Video Information** - Get video details, duration, views, etc.
- **Search Videos** - Search YouTube with automatic fallback
- **Automatic Fallback** - If one method fails, tries another automatically
- **Progress Tracking** - See download progress in real-time
- **Channel Support** - Get channel videos, shorts, streams, and metadata (v0.3+)
- **Video Chapters** - Extract chapter timestamps and key moments (v0.3+)
- **Advanced Search** - Search with native filters without API quota (v0.3+)
- **SponsorBlock** - Skip/remove sponsored segments automatically (v0.5+)
- **Live Streams** - Download live streams from start or current position (v0.5+)
- **Browser Cookies** - Use Chrome/Firefox cookies for age-restricted content (v0.5+)
- **Comments** - Extract video comments with structured data (v0.5+)
- **Heatmap** - Get viewer engagement data (most replayed sections) (v0.5+)
- **Archive Mode** - Track downloads to prevent re-downloading (v0.5+)
- **Chapter Splitting** - Split videos by chapters into separate files (v0.5+)
- **Enhanced Audio** - Download audio with embedded metadata and artwork (v0.5+)

## 🏗️ Architecture

YouTube Toolkit uses a **three-layer architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│              Action-Based API (sub_apis.py) v0.4+           │
│           GetAPI  │  DownloadAPI  │  SearchAPI              │
│   toolkit.get()   │ toolkit.download() │ toolkit.search()   │
│   .channel.videos │ .audio(), .video() │ .videos(), .with_  │
│   .playlist.info  │ .playlist()        │   filters()        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    API Layer (api.py)                       │
│         YouTubeToolkit (Unified Interface)                  │
│   - get_video(), download(), search(), get_channel_videos() │
│   - Automatic fallback, consistent return types             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                Backend Layer (handlers/)                    │
│                  (Handler Classes)                          │
├─────────────┬─────────────┬──────────────┬─────────────────┤
│ PyTubeFix   │   YT-DLP    │ YouTube API  │  ScrapeTube     │
│  Handler    │   Handler   │   Handler    │   Handler       │
│ (Primary)   │ (Fallback)  │ (Metadata)   │ (Optional)      │
└─────────────┴─────────────┴──────────────┴─────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                  External Packages                          │
│   pytubefix  │  yt-dlp  │  google-api  │  scrapetube       │
└─────────────────────────────────────────────────────────────┘
```

- **Action-Based API** (`sub_apis.py`): `GetAPI`, `DownloadAPI`, `SearchAPI` - intuitive action-based interface (v0.4+)
- **API Layer** (`api.py`): `YouTubeToolkit` class provides a unified, user-friendly interface
- **Backend Layer** (`handlers/`): Handler classes act as bridges to each underlying package

## 📦 What Packages We Use

### Core Dependencies (Always Installed)
| Package | Handler | Role |
|---------|---------|------|
| **PyTubeFix** | `PyTubeFixHandler` | Primary download engine, channel support, chapters |
| **YT-DLP** | `YTDLPHandler` | Robust fallback with advanced features |
| **YouTube Data API v3** | `YouTubeAPIHandler` | Rich metadata, comments, official search |
| **MoviePy** | - | Video processing and audio/video combination |
| **FFmpeg** | - | Audio format conversion |

### Optional Dependencies
| Package | Handler | Install | Role |
|---------|---------|---------|------|
| **ScrapeTube** | `ScrapeTubeHandler` | `pip install youtube-toolkit[scrapers]` | Unlimited channel videos, no API quota |

## 🛠️ Installation

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

**Note:** Recent versions of yt-dlp may require an external JavaScript runtime (like [Deno](https://deno.land/)) for full YouTube support. If you experience issues with downloads, install Deno:
```bash
# Ubuntu/Debian
curl -fsSL https://deno.land/install.sh | sh

# macOS
brew install deno

# Windows
irm https://deno.land/install.ps1 | iex
```

### Install the Package
```bash
# Clone the repository
git clone https://github.com/rhythmculture/youtube-toolkit.git
cd youtube-toolkit

# Install with uv (recommended)
uv sync

# Or install with pip
pip install .
```

### Environment Variables (Optional)
```bash
# Create a .env file in your project directory
echo "YOUTUBE_API_KEY=your_api_key_here" > .env

# Or manually create .env file with:
# YOUTUBE_API_KEY=your_actual_api_key_here
```

**Note**: The toolkit automatically loads environment variables from a `.env` file in your project directory. No need to use `export` commands.

### Getting a YouTube API Key
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Copy the API key to your `.env` file

## 🎵 Quick Start

### Action-Based API (v0.4+ Recommended)

The Action-Based API provides 3 core actions: `get`, `download`, `search`. Each action is callable with smart defaults and has explicit sub-methods for full control:

```python
from youtube_toolkit import YouTubeToolkit

toolkit = YouTubeToolkit()

# === GET - Retrieve information ===
# Smart auto-detect (returns VideoInfo, chapters, etc.)
video = toolkit.get("https://youtube.com/watch?v=example")
print(f"{video.title} - {video.duration}s")

# Explicit sub-methods for specific data
chapters = toolkit.get.chapters("https://youtube.com/watch?v=example")
transcript = toolkit.get.transcript("https://youtube.com/watch?v=example")
comments = toolkit.get.comments("https://youtube.com/watch?v=example", max_results=50)
captions = toolkit.get.captions("https://youtube.com/watch?v=example")

# Channel sub-API
channel_videos = toolkit.get.channel.videos("@Fireship", limit=50)
channel_info = toolkit.get.channel.info("@Fireship")
channel_shorts = toolkit.get.channel.shorts("@Fireship")

# Playlist sub-API
playlist_videos = toolkit.get.playlist.videos("https://youtube.com/playlist?list=...")
playlist_info = toolkit.get.playlist.info("https://youtube.com/playlist?list=...")

# === DOWNLOAD - Download content ===
# Smart download (returns DownloadResult for backward compatibility)
result = toolkit.download("https://youtube.com/watch?v=example", type='audio', format='mp3')
if result.success:
    print(f"Downloaded to: {result.file_path}")

# Explicit sub-methods (return file paths directly)
audio_path = toolkit.download.audio("https://youtube.com/watch?v=example", format='mp3')
video_path = toolkit.download.video("https://youtube.com/watch?v=example", quality='720p')
caption_path = toolkit.download.captions("https://youtube.com/watch?v=example", lang='en')
thumb_path = toolkit.download.thumbnail("https://youtube.com/watch?v=example")

# Playlist downloads
results = toolkit.download.playlist("https://youtube.com/playlist?list=...", type='audio')

# === SEARCH - Find content ===
# Smart search (returns SearchResult for backward compatibility)
results = toolkit.search("python tutorial", max_results=10)
for item in results.items:
    print(f"- {item.title}")

# Explicit sub-methods (return List[Dict])
videos = toolkit.search.videos("python tutorial", limit=20)
channels = toolkit.search.channels("python")
playlists = toolkit.search.playlists("python course")

# Advanced search with filters
filtered = toolkit.search.with_filters(
    "python tutorial",
    duration='medium',       # 'short', 'medium', 'long'
    upload_date='month',     # 'hour', 'today', 'week', 'month', 'year'
    sort_by='views'          # 'relevance', 'date', 'views', 'rating'
)
```

### Clean API (v0.1+)
```python
from youtube_toolkit import YouTubeToolkit

toolkit = YouTubeToolkit()

# Get video info as dataclass
video = toolkit.get_video('https://youtube.com/watch?v=example')
print(f"Title: {video.title}")
print(f"Duration: {video.duration} seconds")
print(f"Views: {video.views:,}")

# Download with detailed result
result = toolkit.download('https://youtube.com/watch?v=example', type='audio', format='mp3')
if result.success:
    print(f"Downloaded to: {result.file_path}")
    print(f"Size: {result.file_size_mb} MB")
else:
    print(f"Error: {result.error_message}")

# Search with typed results
results = toolkit.search('python tutorial', max_results=5)
for item in results.items:
    print(f"- {item.title}")
```

### Legacy API (Still Supported)
```python
from youtube_toolkit import YouTubeToolkit

toolkit = YouTubeToolkit()

# Download audio (returns path string)
audio_path = toolkit.download_audio('https://youtube.com/watch?v=example')
print(f"Audio downloaded to: {audio_path}")

# Get video information (returns dict)
info = toolkit.get_video_info('https://youtube.com/watch?v=example')
print(f"Title: {info['title']}")
print(f"Duration: {info['duration']} seconds")
```

### Quiet Mode (Reduced Verbose Output)
```python
# Initialize toolkit with minimal verbose output
toolkit = YouTubeToolkit(verbose=False)

# Download video with reduced progress output
video_path = toolkit.download_video('https://youtube.com/watch?v=example', quality='720p')
print(f"Video downloaded to: {video_path}")
```

**Verbose Options:**
- `verbose=True` (default): Shows detailed progress, fallback messages, and processing steps
- `verbose=False`: Minimal output - only essential progress information

### Improved Format Handling
The toolkit now includes better format selection and automatic fallback:
- **Automatic Quality Fallback**: If requested quality isn't available, automatically tries best available
- **Progressive Stream Support**: Uses progressive streams when available for faster downloads
- **Format Compatibility**: Better handling of different video formats and resolutions
- **Error Recovery**: Automatic fallback between different download methods

### Interactive Demo
```bash
# Run the interactive demo
python main.py
# Enter any YouTube URL when prompted
```

## 📺 Channel & Video Features (v0.3+)

### Channel Videos

Get videos, shorts, or streams from any YouTube channel:

```python
from youtube_toolkit import YouTubeToolkit

toolkit = YouTubeToolkit()

# Get channel videos (default: uses PyTubeFix)
videos = toolkit.get_channel_videos("@Fireship", limit=50)
for video in videos:
    print(f"{video['title']} - {video['views']} views")

# Get channel shorts
shorts = toolkit.get_channel_videos("@Fireship", content_type='shorts', limit=20)

# Get live streams
streams = toolkit.get_channel_videos("@Fireship", content_type='live')

# Get channel playlists
playlists = toolkit.get_channel_videos("@Fireship", content_type='playlists')
```

### Unlimited Channel Videos (ScrapeTube)

For channels with many videos, use ScrapeTube to get ALL videos without limits:

```bash
# Install optional dependency
pip install youtube-toolkit[scrapers]
```

```python
# Get ALL videos from a channel (no 500 video limit!)
all_videos = toolkit.get_all_channel_videos("@Fireship")
print(f"Total videos: {len(all_videos)}")

# Or use the flag with get_channel_videos
videos = toolkit.get_channel_videos("@Fireship", use_scrapetube=True)
```

### Channel Metadata

```python
# Get channel information
info = toolkit.get_channel_info("@Fireship")
print(f"Channel: {info['channel_name']}")
print(f"Subscribers: {info['total_views']} total views")
print(f"Videos: {info['video_count']}")
```

### Video Chapters

Extract chapter timestamps from videos:

```python
# Get video chapters
chapters = toolkit.get_video_chapters("https://youtube.com/watch?v=...")

for chapter in chapters:
    print(f"{chapter['formatted_start']} - {chapter['title']}")
# Output:
# 0:00 - Introduction
# 2:30 - Getting Started
# 10:15 - Advanced Topics

# Get AI-generated key moments
key_moments = toolkit.get_key_moments("https://youtube.com/watch?v=...")

# Get viewer engagement heatmap (most replayed sections)
heatmap = toolkit.get_replayed_heatmap("https://youtube.com/watch?v=...")
```

### Advanced Search (No API Quota)

Search with YouTube's native filters without using API quota:

```python
# Search with filters
results = toolkit.search_with_filters(
    "python tutorial",
    duration='medium',      # 'short' (<4min), 'medium' (4-20min), 'long' (>20min)
    upload_date='month',    # 'hour', 'today', 'week', 'month', 'year'
    sort_by='views',        # 'relevance', 'date', 'views', 'rating'
    features=['hd', 'cc'],  # 'hd', '4k', 'live', 'cc', 'creative_commons', 'hdr'
    max_results=20
)

for video in results['videos']:
    print(f"{video['title']} - {video['views']} views")

# Also returns: shorts, channels, playlists, completion_suggestions
print(f"Suggestions: {results['completion_suggestions']}")
```

### Playlist Information

```python
# Get detailed playlist info
info = toolkit.get_playlist_info("https://youtube.com/playlist?list=...")
print(f"Playlist: {info['title']}")
print(f"Owner: {info['owner']}")
print(f"Videos: {info['video_count']}")
print(f"Views: {info['views']}")
```

### Search Without API

Use ScrapeTube for search when you want to avoid API quota:

```python
# Search without API quota (uses scrapetube if installed, falls back to pytubefix)
results = toolkit.search_without_api("python tutorial", limit=20)
```

## 🔥 Advanced Features (v0.5+)

### SponsorBlock Integration

Automatically detect and handle sponsored segments:

```python
from youtube_toolkit import YouTubeToolkit

toolkit = YouTubeToolkit()

# Get sponsored segments for a video
segments = toolkit.sponsorblock.segments("https://youtube.com/watch?v=...")
for seg in segments:
    print(f"{seg['category']}: {seg['start_time']:.1f}s - {seg['end_time']:.1f}s")
# Output:
# sponsor: 30.0s - 90.0s
# intro: 0.0s - 5.0s

# Download video with sponsors removed
path = toolkit.sponsorblock.download("url", action='remove')

# Or mark sponsors as chapters instead of removing
path = toolkit.sponsorblock.download("url", action='mark')
```

### Live Stream Downloads

Download live streams or archived streams:

```python
# Check if a video is live
if toolkit.live.is_live("url"):
    print("Stream is currently live!")

# Get live stream status
status = toolkit.live.status("url")
print(f"Live: {status['is_live']}, Was Live: {status['was_live']}")

# Download live stream from the beginning
path = toolkit.live.download("url", from_start=True)

# Download only first 5 minutes
path = toolkit.live.download("url", duration=300)
```

### Browser Cookie Authentication

Access age-restricted or member-only content using browser cookies:

```python
# Get video info using Chrome cookies (for age-restricted content)
info = toolkit.cookies.get_video("url", browser='chrome')

# Supported browsers
browsers = toolkit.cookies.supported_browsers()
# ['chrome', 'firefox', 'safari', 'edge', 'opera', 'brave', 'chromium', 'vivaldi']
```

### Viewer Engagement Data

Get heatmap and comment analytics:

```python
# Get most replayed sections (heatmap)
heatmap = toolkit.engagement.heatmap("url")
for segment in heatmap:
    print(f"{segment['start_time']:.0f}s: {segment['value']:.0%} engagement")

# Get video comments with structured data
comments = toolkit.engagement.comments("url", max_comments=50, sort='top')
for comment in comments:
    print(f"{comment['author']}: {comment['text'][:50]}... ({comment['like_count']} likes)")

# Get AI-generated key moments
moments = toolkit.engagement.key_moments("url")
```

### Archive Mode (Prevent Re-downloads)

Track downloaded videos to avoid duplicates:

```python
# Set archive file
toolkit.archive.set_archive_file("./downloaded.txt")

# Download (skips if already in archive)
path = toolkit.archive.download("url")
if path is None:
    print("Already downloaded!")

# Check if video is in archive
if toolkit.archive.contains("url"):
    print("Already have this one")
```

### Chapter Splitting

Split videos by chapters into separate files:

```python
# Get chapters
chapters = toolkit.chapters.get("url")
for ch in chapters:
    print(f"{ch['formatted_start']} - {ch['title']}")

# Download and split by chapters
files = toolkit.chapters.split("url", format='mp3')
print(f"Created {len(files)} files")
```

### Enhanced Audio Downloads

Download audio with embedded metadata and artwork:

```python
# Download MP3 with cover art and ID3 tags
path = toolkit.audio_enhanced.download("url", format='mp3')

# Download without artwork
path = toolkit.audio_enhanced.download("url", embed_thumbnail=False)

# Download FLAC with metadata
path = toolkit.audio_enhanced.download("url", format='flac', add_metadata=True)
```

### Thumbnail Downloads

Download video thumbnails:

```python
# Download thumbnail
path = toolkit.thumbnail.download("url")

# Get thumbnail URL without downloading
thumb_url = toolkit.thumbnail.url("url")
```

### Subtitle Conversion

Download and convert subtitles:

```python
# Download subtitles
path = toolkit.subtitles.download("url", lang='en')

# Convert subtitle format
vtt_path = toolkit.subtitles.convert("video.srt", to='vtt')

# Supported formats
formats = toolkit.subtitles.supported_formats()
# ['srt', 'vtt', 'ass', 'json3', 'ttml']
```

## 📚 Usage Examples

### Download Audio
```python
# Download as WAV (default)
audio_path = toolkit.download_audio('https://youtube.com/watch?v=example')

# Download as MP3
audio_path = toolkit.download_audio('https://youtube.com/watch?v=example', format='mp3')

# Download to custom location
audio_path = toolkit.download_audio(
    'https://youtube.com/watch?v=example', 
    format='mp3', 
    output_path='/path/to/music/'
)
```

### Download Video
```python
# Download best quality
video_path = toolkit.download_video('https://youtube.com/watch?v=example')

# Download specific quality
video_path = toolkit.download_video('https://youtube.com/watch?v=example', quality='720p')

# Download to custom location
video_path = toolkit.download_video(
    'https://youtube.com/watch?v=example', 
    quality='1080p', 
    output_path='/path/to/videos/'
)
```

### Search Videos
```python
# Search for videos
search_results = toolkit.search_videos('super shy', max_results=5)

for result in search_results:
    print(f"Title: {result['title']}")
    print(f"URL: {result['watch_url']}")
    print(f"Channel: {result['author']}")
```

### Get Video Information
```python
# Get comprehensive video info
info = toolkit.get_video_info('https://youtube.com/watch?v=example')

print(f"Title: {info['title']}")
print(f"Channel: {info['channel']}")
print(f"Duration: {info['duration']} seconds")
print(f"Views: {info['view_count']:,}")
print(f"Upload Date: {info['upload_date']}")
```

## 🆕 API Reference

### Action-Based API (v0.4+)

The Action-Based API provides 3 core actions with smart defaults and explicit sub-methods:

#### GET Action
| Method | Returns | Description |
|--------|---------|-------------|
| `get(url)` | `VideoInfo` | Smart auto-detect video info |
| `get.video(url)` | `VideoInfo` | Explicit video metadata |
| `get.chapters(url)` | `List[Dict]` | Video chapter timestamps |
| `get.transcript(url)` | `str` | Video transcript text |
| `get.comments(url, max_results)` | `CommentResult` | Video comments |
| `get.captions(url)` | `CaptionResult` | Available caption tracks |
| `get.channel.videos(channel, limit)` | `List[Dict]` | Channel videos |
| `get.channel.info(channel)` | `Dict` | Channel metadata |
| `get.channel.shorts(channel, limit)` | `List[Dict]` | Channel shorts |
| `get.channel.streams(channel, limit)` | `List[Dict]` | Channel live streams |
| `get.channel.all_videos(channel)` | `List[Dict]` | ALL videos (scrapetube) |
| `get.playlist.videos(url, limit)` | `List[Dict]` | Playlist videos |
| `get.playlist.info(url)` | `Dict` | Playlist metadata |
| `get.playlist.urls(url)` | `List[str]` | Playlist video URLs |

#### DOWNLOAD Action
| Method | Returns | Description |
|--------|---------|-------------|
| `download(url, type, ...)` | `DownloadResult` | Smart download (backward compatible) |
| `download.audio(url, format, bitrate)` | `str` | Download audio, return path |
| `download.video(url, quality)` | `str` | Download video, return path |
| `download.captions(url, lang)` | `str` | Download captions, return path |
| `download.thumbnail(url, quality)` | `str` | Download thumbnail, return path |
| `download.playlist(url, type)` | `Dict` | Download entire playlist |

#### SEARCH Action
| Method | Returns | Description |
|--------|---------|-------------|
| `search(query, max_results, filters)` | `SearchResult` | Smart search (backward compatible) |
| `search.videos(query, limit)` | `List[Dict]` | Search videos only |
| `search.channels(query, limit)` | `List[Dict]` | Search channels only |
| `search.playlists(query, limit)` | `List[Dict]` | Search playlists only |
| `search.with_filters(query, ...)` | `Dict` | Advanced filtered search |

### Legacy API (Still Supported)

| Method | Returns | Description |
|--------|---------|-------------|
| `get_video(url)` | `VideoInfo` | Video metadata as dataclass |
| `download(url, type, ...)` | `DownloadResult` | Download with success/error info |
| `search(query, ...)` | `SearchResult` | Search results with items list |
| `comments(url, ...)` | `CommentResult` | Comments with analytics |
| `captions(url, ...)` | `CaptionResult` | Available caption tracks |
| `playlist(url)` | `List[str]` | Video URLs from playlist |
| `download_audio(url, ...)` | `str` | Download audio (path) |
| `download_video(url, ...)` | `str` | Download video (path) |
| `search_videos(query, ...)` | `List[Dict]` | Search videos |
| `get_video_info(url)` | `Dict` | Video info as dict |

### Channel API (v0.3+)

| Method | Returns | Description |
|--------|---------|-------------|
| `get_channel_videos(channel, ...)` | `List[Dict]` | Channel videos/shorts/streams |
| `get_channel_info(channel)` | `Dict` | Channel metadata |
| `get_all_channel_videos(channel)` | `List[Dict]` | ALL videos (requires scrapetube) |
| `get_video_chapters(url)` | `List[Dict]` | Video chapter timestamps |
| `get_key_moments(url)` | `List[Dict]` | AI-generated key moments |
| `get_replayed_heatmap(url)` | `List[Dict]` | Viewer engagement data |
| `search_with_filters(query, ...)` | `Dict` | Search with native YouTube filters |
| `get_playlist_info(url)` | `Dict` | Playlist metadata |
| `search_without_api(query, ...)` | `List[Dict]` | Search without API quota |

### Advanced API (v0.5+)

| Sub-API | Method | Returns | Description |
|---------|--------|---------|-------------|
| `sponsorblock` | `.segments(url)` | `List[Dict]` | Get SponsorBlock segments |
| | `.download(url, action)` | `str` | Download with sponsors handled |
| `live` | `.status(url)` | `Dict` | Get live stream status |
| | `.download(url, from_start)` | `str` | Download live stream |
| | `.is_live(url)` | `bool` | Check if currently live |
| `archive` | `.download(url)` | `str\|None` | Download with archive tracking |
| | `.contains(url)` | `bool` | Check if in archive |
| | `.set_archive_file(path)` | `None` | Set archive file path |
| `engagement` | `.heatmap(url)` | `List[Dict]` | Get engagement heatmap |
| | `.comments(url, max)` | `List[Dict]` | Get structured comments |
| | `.key_moments(url)` | `List[Dict]` | Get AI key moments |
| `cookies` | `.get_video(url, browser)` | `Dict` | Get info with browser cookies |
| | `.supported_browsers()` | `List[str]` | List supported browsers |
| `subtitles` | `.download(url, lang)` | `str` | Download subtitles |
| | `.convert(path, to)` | `str` | Convert subtitle format |
| | `.supported_formats()` | `List[str]` | List supported formats |
| `chapters` | `.get(url)` | `List[Dict]` | Get video chapters |
| | `.split(url, format)` | `List[str]` | Split video by chapters |
| `thumbnail` | `.download(url)` | `str` | Download thumbnail |
| | `.url(url)` | `str` | Get thumbnail URL |
| `audio_enhanced` | `.download(url, ...)` | `str` | Audio with metadata/artwork |

### Using Filters
```python
from youtube_toolkit import YouTubeToolkit, SearchFilters, CommentFilters, CommentOrder

toolkit = YouTubeToolkit()

# Search with filters (both APIs work)
filters = SearchFilters(video_duration='short', order='viewCount')
results = toolkit.search('music video', filters=filters)  # Action-based
# OR
results = toolkit.search('music video', filters=filters)  # Same method

# Comments with filters
comment_filters = CommentFilters(order=CommentOrder.TIME, min_likes=10)
comments = toolkit.get.comments(url, filters=comment_filters)  # Action-based
# OR
comments = toolkit.comments(url, filters=comment_filters)  # Legacy
```

### Return Types
```python
from youtube_toolkit import VideoInfo, DownloadResult, SearchResult

# VideoInfo fields
video: VideoInfo = toolkit.get("url")  # or toolkit.get_video(url)
video.title       # str
video.duration    # int (seconds)
video.views       # int
video.author      # str
video.video_id    # str
video.description # Optional[str]
video.thumbnail   # Optional[str]

# DownloadResult fields
result: DownloadResult = toolkit.download(url, type='audio')
result.success       # bool
result.file_path     # str
result.error_message # Optional[str]
result.file_size     # Optional[int]
result.file_size_mb  # Optional[float]
result.download_time # Optional[float]

# SearchResult fields
results: SearchResult = toolkit.search("query")
results.items        # List[SearchResultItem]
results.total_results # int
results.query        # str
results.has_results  # bool
```

## 🔧 Advanced Features

### Handler Preferences
```python
# Prefer yt-dlp over pytubefix
audio_path = toolkit.download_audio('url', prefer_yt_dlp=True)
video_path = toolkit.download_video('url', prefer_yt_dlp=True)
```

### Custom Output Paths
```python
# For PyTubeFix: Full file path including filename
output_path = "/path/to/folder/video.mp4"

# For YT-DLP: Directory path only (filename auto-generated)
output_path = "/path/to/folder/"
```

### Playlist Downloads
```python
# Download all audio from a playlist
results = toolkit.download_playlist_media(
    "https://www.youtube.com/playlist?list=PL...",
    media_type="audio",
    format="mp3",
    include_captions=True
)

# Download all videos from a playlist
results = toolkit.download_playlist_media(
    "https://www.youtube.com/playlist?list=PL...",
    media_type="video",
    quality="720p",
    include_captions=False
)

print(f"Downloaded {results['metadata']['download_summary']['successful_downloads']} videos")
print(f"Files saved to: {results['playlist_dir']}")
```

#### Extract Playlist URLs
```python
# Get all video URLs from a playlist
urls = toolkit.get_playlist_urls("https://www.youtube.com/playlist?list=PL...")
print(f"Found {len(urls)} videos in playlist")

# Process each video individually
for url in urls:
    info = toolkit.get_video_info(url)
    print(f"Processing: {info['title']}")
```

### Progress Callbacks
```python
# Disable progress display
audio_path = toolkit.download_audio('url', progress_callback=False)
```

## 🚨 Troubleshooting

### Common Issues

#### 1. FFmpeg Not Found
```bash
# Install FFmpeg first
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

#### 2. PyTubeFix Search Fails
```python
# Use basic search without filters
search_results = toolkit.search_videos('query', max_results=5)

# Or use YouTube API search
api_results = toolkit.youtube_api.search_videos('query', max_results=10)
```

#### 3. MoviePy Import Error
```bash
# Install MoviePy
pip install moviepy
```

#### 4. YouTube API Issues
```bash
# Create a .env file in your project directory
echo "YOUTUBE_API_KEY=your_api_key_here" > .env

# Or manually create .env file with your actual API key
# YOUTUBE_API_KEY=your_actual_api_key_here

# Install API client
pip install google-api-python-client
```

### Test Your Setup
```python
# Test which handlers are working
status = toolkit.test_handlers('https://youtube.com/watch?v=example')
print(status)

# Test search functionality
search_test = toolkit.test_search('test')
print(search_test)
```

## 📁 Project Structure
```
youtube-toolkit/
├── youtube_toolkit/
│   ├── api.py                      # API Layer: YouTubeToolkit class
│   ├── sub_apis.py                 # Action-Based API: GetAPI, DownloadAPI, SearchAPI (v0.4+)
│   ├── handlers/                   # Backend Layer: Handler classes
│   │   ├── pytubefix_handler.py    # PyTubeFix backend (primary)
│   │   ├── yt_dlp_handler.py       # YT-DLP backend (fallback)
│   │   ├── youtube_api_handler.py  # YouTube API backend (metadata)
│   │   └── scrapetube_handler.py   # ScrapeTube backend (optional, v0.3+)
│   ├── core/                       # Core data structures (VideoInfo, etc.)
│   └── utils/                      # Utility functions
├── tests/                          # Test suite (146 tests)
├── examples/                       # Usage examples
├── pyproject.toml                  # Package configuration
└── README.md                       # This file
```

### Backend Layer Details

| Handler | Package | Features |
|---------|---------|----------|
| `PyTubeFixHandler` | pytubefix | Downloads, channel videos, chapters, advanced search |
| `YTDLPHandler` | yt-dlp | Downloads (fallback), transcripts, format support |
| `YouTubeAPIHandler` | google-api | Comments, rich metadata, official search |
| `ScrapeTubeHandler` | scrapetube | Unlimited channel videos, search (optional) |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **PyTubeFix** - Primary download engine
- **YT-DLP** - Advanced download backend
- **MoviePy** - Video processing capabilities
- **FFmpeg** - Audio/video conversion

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Search existing issues
3. Create a new issue with details about your problem

---

**Happy downloading! 🎵**

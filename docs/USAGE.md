# YouTube Toolkit Usage Guide

This guide covers how to use youtube-toolkit effectively.

## Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [The 5 Core APIs](#the-5-core-apis)
- [Common Use Cases](#common-use-cases)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)

## Installation

```bash
# Install from GitHub
uv pip install git+https://github.com/rhythmculture/youtube-toolkit.git

# Or with pip
pip install git+https://github.com/rhythmculture/youtube-toolkit.git
```

## Quick Start

```python
from youtube_toolkit import YouTubeToolkit

# Initialize the toolkit
toolkit = YouTubeToolkit()

# Get video information
video = toolkit.get("https://youtube.com/watch?v=dQw4w9WgXcQ")
print(f"Title: {video['title']}")
print(f"Duration: {video['duration']} seconds")

# Download audio
result = toolkit.download("https://youtube.com/watch?v=dQw4w9WgXcQ", type='audio', format='mp3')
if result['success']:
    print(f"Downloaded to: {result['file_path']}")

# Search for videos
results = toolkit.search("python tutorial", max_results=5)
for item in results:
    print(f"- {item['title']}")
```

## The 5 Core APIs

youtube-toolkit is organized into 5 intuitive APIs:

### 1. GET API - Retrieve Information

Use `toolkit.get` to retrieve information without downloading.

```python
# Video information
video = toolkit.get(url)                    # Returns VideoInfo dataclass
video = toolkit.get.video(url)              # Same as above

# Video details
chapters = toolkit.get.chapters(url)        # List of chapter timestamps
transcript = toolkit.get.transcript(url)    # Full transcript text
comments = toolkit.get.comments(url)        # CommentResult with comments
captions = toolkit.get.captions(url)        # Available caption tracks
formats = toolkit.get.formats(url)          # Available download formats
keywords = toolkit.get.keywords(url)        # Video tags/keywords
heatmap = toolkit.get.heatmap(url)          # Viewer engagement data
restriction = toolkit.get.restriction(url)  # Age/region restrictions
embed_url = toolkit.get.embed_url(url)      # Embeddable URL

# Channel operations
info = toolkit.get.channel("@ChannelName")              # Channel info
videos = toolkit.get.channel.videos("@ChannelName")     # Channel videos
shorts = toolkit.get.channel.shorts("@ChannelName")     # Channel shorts
streams = toolkit.get.channel.streams("@ChannelName")   # Live streams

# Playlist operations
videos = toolkit.get.playlist.videos(playlist_url)      # Playlist videos
info = toolkit.get.playlist.info(playlist_url)          # Playlist metadata
urls = toolkit.get.playlist.urls(playlist_url)          # Just the URLs
```

### 2. DOWNLOAD API - Save to Disk

Use `toolkit.download` to save content to your filesystem.

```python
# Basic downloads
result = toolkit.download(url, type='audio', format='mp3')  # Returns DownloadResult
audio_path = toolkit.download.audio(url, format='mp3')      # Returns file path
video_path = toolkit.download.video(url, quality='720p')    # Returns file path

# Captions and thumbnails
caption_path = toolkit.download.captions(url, lang='en')
thumb_path = toolkit.download.thumbnail(url)

# Playlist download
results = toolkit.download.playlist(playlist_url, type='audio', format='mp3')

# Advanced downloads
toolkit.download.shorts(url)                              # YouTube Shorts
toolkit.download.live(url, from_start=True)               # Live streams
toolkit.download.with_sponsorblock(url, action='remove')  # Skip sponsors
toolkit.download.with_metadata(url, embed_thumbnail=True) # With ID3 tags
toolkit.download.with_filter(url, match_filter="duration > 600")
toolkit.download.with_archive(url, archive_file="downloaded.txt")
toolkit.download.with_cookies(url, browser='chrome')      # Age-restricted
```

### 3. SEARCH API - Find Content

Use `toolkit.search` to find videos, channels, and playlists.

```python
# Basic search
results = toolkit.search("query")                   # Returns SearchResult
results = toolkit.search("query", max_results=20)   # Limit results

# Type-specific search
videos = toolkit.search.videos("query")             # Only videos
channels = toolkit.search.channels("query")         # Only channels
playlists = toolkit.search.playlists("query")       # Only playlists

# Advanced search with filters
results = toolkit.search.with_filters(
    "python tutorial",
    duration='medium',      # 'short' (<4min), 'medium' (4-20min), 'long' (>20min)
    upload_date='month',    # 'hour', 'today', 'week', 'month', 'year'
    sort_by='views',        # 'relevance', 'date', 'views', 'rating'
    features=['hd', 'cc']   # 'hd', '4k', 'live', 'cc', 'creative_commons'
)

# Autocomplete suggestions
suggestions = toolkit.search.suggestions("python tut")

# Trending (requires API key)
trending = toolkit.search.trending()
trending_by_cat = toolkit.search.trending.by_category()

# Reference data (requires API key)
categories = toolkit.search.categories()
regions = toolkit.search.regions()
languages = toolkit.search.languages()
```

### 4. ANALYZE API - Analyze Content

Use `toolkit.analyze` for deep content analysis.

```python
# Full metadata (50+ fields)
metadata = toolkit.analyze(url)
metadata = toolkit.analyze.metadata(url)

# Engagement data
engagement = toolkit.analyze.engagement(url)
print(engagement['heatmap'])      # Most replayed sections
print(engagement['key_moments'])  # AI-generated moments

# Other analysis
comments = toolkit.analyze.comments(url, max_comments=100)
captions = toolkit.analyze.captions(url)
segments = toolkit.analyze.sponsorblock(url)  # Sponsor segments
channel = toolkit.analyze.channel("@ChannelName")
filesize = toolkit.analyze.filesize(url)      # Preview without downloading
```

### 5. STREAM API - Stream to Buffer

Use `toolkit.stream` to get content as bytes without saving to disk.

```python
# Stream to memory
audio_bytes = toolkit.stream(url)                   # Audio buffer
audio_bytes = toolkit.stream.audio(url)             # Same
video_bytes = toolkit.stream.video(url)             # Video buffer

# Live stream operations
status = toolkit.stream.live.status(url)
is_live = toolkit.stream.live.is_live(url)
path = toolkit.stream.live.download(url, from_start=True)
```

## Common Use Cases

### Download a YouTube Playlist as MP3s

```python
toolkit = YouTubeToolkit()

# Download entire playlist
results = toolkit.download.playlist(
    "https://youtube.com/playlist?list=PLxxxxx",
    type='audio',
    format='mp3'
)

print(f"Downloaded {results['metadata']['download_summary']['successful_downloads']} files")
```

### Get All Videos from a Channel

```python
toolkit = YouTubeToolkit()

# Get recent videos
videos = toolkit.get.channel.videos("@Fireship", limit=50)

# Get ALL videos (requires scrapetube: pip install youtube-toolkit[scrapers])
all_videos = toolkit.get.channel.all_videos("@Fireship")

for video in videos:
    print(f"{video['title']} - {video['views']} views")
```

### Download Video Without Sponsor Segments

```python
toolkit = YouTubeToolkit()

# Remove sponsor segments
path = toolkit.download.with_sponsorblock(url, action='remove')

# Or just mark them as chapters
path = toolkit.download.with_sponsorblock(url, action='mark')
```

### Check Video Engagement

```python
toolkit = YouTubeToolkit()

# Get heatmap (most replayed sections)
engagement = toolkit.analyze.engagement(url)

for point in engagement['heatmap']:
    print(f"Time {point['start_time']}s: {point['value']:.0%} engagement")
```

### Download Age-Restricted Content

```python
toolkit = YouTubeToolkit()

# Use browser cookies for authentication
path = toolkit.download.with_cookies(url, browser='chrome')
```

## Error Handling

```python
from youtube_toolkit import YouTubeToolkit

toolkit = YouTubeToolkit()

# Using download result
result = toolkit.download(url, type='audio')
if result['success']:
    print(f"Downloaded: {result['file_path']}")
    print(f"Size: {result.get('file_size_mb', 'N/A')} MB")
else:
    print(f"Error: {result.get('error_message', 'Unknown error')}")

# Using try/except for sub-API methods
try:
    path = toolkit.download.audio(url)
    print(f"Downloaded to: {path}")
except Exception as e:
    print(f"Download failed: {e}")
```

## Best Practices

### 1. Use the Right API for the Job

- Need info without downloading? → `toolkit.get`
- Saving to disk? → `toolkit.download`
- Finding content? → `toolkit.search`
- Deep analysis? → `toolkit.analyze`
- Processing in memory? → `toolkit.stream`

### 2. Handle Rate Limits

```python
import time

urls = [...]  # List of URLs
for url in urls:
    toolkit.download.audio(url)
    time.sleep(1)  # Be nice to YouTube
```

### 3. Use Archive Mode for Batch Downloads

```python
# Prevents re-downloading the same video
for url in urls:
    toolkit.download.with_archive(url, archive_file="downloaded.txt")
```

### 4. Check Formats Before Downloading

```python
formats = toolkit.get.formats(url)
print("Available audio:", formats['audio'])
print("Available video:", formats['video'])
```

### 5. Preview Filesize Before Large Downloads

```python
filesize = toolkit.analyze.filesize(url)
print(f"Audio: {filesize['best_audio']['filesize_mb']} MB")
print(f"Video: {filesize['best_video']['filesize_mb']} MB")
```

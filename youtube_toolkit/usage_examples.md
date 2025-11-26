# YouTubeToolkit Usage Examples

This file contains short code snippets for each individual function in the YouTubeToolkit.

## Basic Setup

```python
from youtube_toolkit import YouTubeToolkit

# Initialize the toolkit
toolkit = YouTubeToolkit()
```

## 1. Video Information

### Get Video Info
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_info = toolkit.get_video_info(url)

print(f"Title: {video_info['title']}")
print(f"Duration: {video_info['duration']} seconds")
print(f"Channel: {video_info['channel']}")
print(f"Views: {video_info['view_count']:,}")
```

### Get Available Formats
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
formats = toolkit.get_available_formats(url)

print("Available video formats:")
for resolution, format_list in formats['video_formats'].items():
    print(f"  {resolution}: {len(format_list)} options")

print("Available audio formats:")
for bitrate, format_list in formats['audio_formats'].items():
    print(f"  {bitrate}: {len(format_list)} options")
```

### Extract Video ID
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
video_id = toolkit.extract_video_id(url)

print(f"Video ID: {video_id}")
# Output: Video ID: dQw4w9WgXcQ
```

## 2. Download Functions

### Download Audio
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download with default settings (WAV format, current directory)
audio_path = toolkit.download_audio(url)
print(f"Audio downloaded to: {audio_path}")

# Download with custom format and path
audio_path = toolkit.download_audio(
    url, 
    format='mp3', 
    output_path='/path/to/custom/folder/'
)
print(f"MP3 downloaded to: {audio_path}")

# Prefer yt-dlp over pytubefix
audio_path = toolkit.download_audio(url, prefer_yt_dlp=True)
```

### Download Video
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download with best quality
video_path = toolkit.download_video(url)
print(f"Video downloaded to: {video_path}")

# Download with specific quality
video_path = toolkit.download_video(url, quality='720p')
print(f"720p video downloaded to: {video_path}")

# Download with custom path
video_path = toolkit.download_video(
    url, 
    quality='1080p', 
    output_path='/path/to/videos/'
)
print(f"1080p video downloaded to: {video_path}")

# Prefer yt-dlp over pytubefix
video_path = toolkit.download_video(url, prefer_yt_dlp=True)
```

**Note**: PyTubeFix video downloads require MoviePy (`pip install moviepy`). If MoviePy fails, it automatically falls back to downloading a progressive stream (video + audio combined) instead of separate streams.

## 3. Search Functions

### Search Videos
```python
search_query = "super shy"
search_results = toolkit.search_videos(search_query, max_results=3)

for i, result in enumerate(search_results, 1):
    print(f"{i}. {result['title']}")
    print(f"   Channel: {result['author']}")
    print(f"   Duration: {result['length']} seconds")
    print(f"   URL: {result['watch_url']}")
    print()

# Get first result details
chosen_title = search_results[0]['title']
chosen_url = search_results[0]['watch_url']
print(f"Chosen: {chosen_title} : {chosen_url}")
```

**Note**: PyTubeFix search currently has some limitations with filters. The system automatically falls back to basic search and YouTube API to ensure you get results.

### Search with Filters
```python
search_query = "python programming"
filters = {
    'type': 'Video',
    'sort_by': 'Relevance',
    'upload_date': 'This year'
}
search_results = toolkit.search_videos(search_query, filters=filters, max_results=5)

for result in search_results:
    print(f"• {result['title']} by {result['author']}")
```

**Note**: Filter support is currently limited in PyTubeFix. For advanced filtering, consider using YouTube API search which provides better filter options.

### Test Search Functionality
```python
# Test if search is working across all handlers
search_test = toolkit.test_search("super shy")
print(f"Search test results: {search_test}")

# Test with a simple query
simple_test = toolkit.test_search("test")
print(f"Simple test results: {simple_test}")
```

## 4. Caption Functions

### Get Available Captions
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
captions = toolkit.get_captions(url)

print(f"Total captions available: {captions['total_captions']}")
for caption in captions['available_captions']:
    lang = caption['language_code']
    auto_gen = " (Auto)" if caption['is_auto_generated'] else ""
    print(f"  {lang}{auto_gen}: {caption['language']}")
```

### Download Captions
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download English captions
caption_path = toolkit.download_captions(url, language_code='en')
print(f"Captions downloaded to: {caption_path}")

# Download with custom path
caption_path = toolkit.download_captions(
    url, 
    language_code='en', 
    output_path='/path/to/captions/english.txt'
)
print(f"Captions downloaded to: {caption_path}")
```

## 5. Metadata Functions

### Get Rich Metadata
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
metadata = toolkit.get_rich_metadata(url)

print(f"Title: {metadata['title']}")
print(f"Description: {metadata['description'][:200]}...")
print(f"Tags: {', '.join(metadata['tags'][:5])}")
print(f"Category: {metadata['categories'][0] if metadata['categories'] else 'None'}")
```

### Get Video Description
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
description = toolkit.get_video_description(url)

print("Video Description:")
print(description[:500] + "..." if len(description) > 500 else description)
```

## 6. Comment Functions

### Get Comments
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
comments = toolkit.get_comments(url, max_results=10, sort_by='relevance')

for i, comment in enumerate(comments, 1):
    print(f"{i}. {comment['author']} (👍 {comment['like_count']})")
    print(f"   {comment['text']}")
    print()
```

### Display Top Comments
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
toolkit.display_comments(url, top_n=5, sort_by='relevance')
```

## 7. Testing Functions

### Test Handlers
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
handler_status = toolkit.test_handlers(url)

for handler, status in handler_status.items():
    status_icon = "✅" if status else "❌"
    print(f"{status_icon} {handler}: {'Working' if status else 'Failed'}")
```

### Test Anti-Detection
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
anti_detection_results = toolkit.test_anti_detection(url)

print("Anti-Detection Test Results:")
for handler, result in anti_detection_results.items():
    if isinstance(result, dict) and 'success' in result:
        print(f"  {handler}: {'✅' if result['success'] else '❌'}")
        if 'time_taken' in result:
            print(f"    Time: {result['time_taken']:.2f}s")
```

### Get Anti-Detection Status
```python
status = toolkit.get_anti_detection_status()

print("Global Status:", status['global_status'])
print("\nHandler Status:")
for handler, handler_status in status['handlers'].items():
    print(f"  {handler}: {handler_status}")
```

## 8. Advanced Usage Examples

### Batch Download Multiple Videos
```python
urls = [
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
    "https://www.youtube.com/watch?v=9bZkp7q19f0",
    "https://www.youtube.com/watch?v=kJQP7kiw5Fk"
]

for url in urls:
    try:
        print(f"Downloading: {url}")
        video_path = toolkit.download_video(url, quality='720p')
        print(f"✅ Downloaded to: {video_path}")
    except Exception as e:
        print(f"❌ Failed: {e}")
    print()
```

### Download with Custom Naming
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Get video info first
info = toolkit.get_video_info(url)
title = info['title'].replace(' ', '_')[:50]  # Limit length

# Download with custom filename
audio_path = toolkit.download_audio(
    url, 
    format='mp3', 
    output_path=f'/path/to/music/{title}.mp3'
)
print(f"Audio saved as: {audio_path}")
```

### Error Handling Example
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

try:
    # Try to download with pytubefix first
    video_path = toolkit.download_video(url, prefer_yt_dlp=False)
    print(f"Downloaded with PyTubeFix: {video_path}")
except Exception as e:
    print(f"PyTubeFix failed: {e}")
    try:
        # Fallback to yt-dlp
        video_path = toolkit.download_video(url, prefer_yt_dlp=True)
        print(f"Downloaded with YT-DLP: {video_path}")
    except Exception as e2:
        print(f"YT-DLP also failed: {e2}")
        print("All download methods failed")
```

## 9. Handler-Specific Examples

### Use Specific Handler for Audio
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Force use of yt-dlp
audio_path = toolkit.yt_dlp.download_audio(url, format='mp3')
print(f"YT-DLP audio: {audio_path}")

# Force use of pytubefix
audio_path = toolkit.pytubefix.download_audio(url, format='wav')
print(f"PyTubeFix audio: {audio_path}")
```

### Get Handler-Specific Formats
```python
url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# PyTubeFix formats
pytube_formats = toolkit.pytubefix.get_available_formats(url)
print("PyTubeFix formats:", pytube_formats)

# YT-DLP formats
ytdlp_formats = toolkit.yt_dlp.get_available_formats(url)
print("YT-DLP formats:", ytdlp_formats)
```

## Notes

- All functions automatically fall back to alternative methods if the primary method fails
- The `output_path` parameter behavior differs between handlers:
  - **PyTubeFix**: Expects full file path including filename
  - **YT-DLP**: Expects directory path (filename auto-generated)
- Use `prefer_yt_dlp=True` to prioritize yt-dlp over pytubefix
- Progress callbacks can be disabled with `progress_callback=False`
- Error handling is built-in with automatic fallbacks

## Troubleshooting

### Common Issues and Solutions

#### 1. MoviePy Import Error
```python
# Error: "MoviePy is required for video downloads"
# Solution: Install MoviePy
pip install moviepy
```

#### 2. PyTubeFix Video Download Fails
```python
# If you get MoviePy parameter errors, try using yt-dlp instead:
video_path = toolkit.download_video(url, prefer_yt_dlp=True)

# Or install/update MoviePy:
pip install --upgrade moviepy
```

#### 3. Audio/Video Combination Fails
```python
# PyTubeFix automatically falls back to progressive streams if MoviePy fails
# This downloads video + audio together (lower quality but more reliable)
# Check the console output for fallback messages
```

#### 4. Search Issues
```python
# Test search functionality:
search_test = toolkit.test_search("test")
print(search_test)

# If PyTubeFix search fails, try YouTube API:
try:
    results = toolkit.youtube_api.search_videos("your query", max_results=10)
    print(f"API search results: {len(results)}")
except Exception as e:
    print(f"API search also failed: {e}")

# Check if YouTube API key is set:
import os
if not os.getenv("YOUTUBE_API_KEY"):
    print("YouTube API key not set. Set YOUTUBE_API_KEY environment variable.")

# Try simple search without filters:
try:
    simple_results = toolkit.pytubefix.simple_search("your query", max_results=5)
    print(f"Simple search results: {len(simple_results)}")
except Exception as e:
    print(f"Simple search failed: {e}")
```

#### 5. Search Filter Issues
```python
# If you get "dictionary update sequence element #0 has length 1; 2 is required":
# This is a known PyTubeFix limitation. Use basic search instead:

# ❌ This may fail:
# search_results = toolkit.search_videos("query", filters={'type': 'Video'})

# ✅ Use this instead:
search_results = toolkit.search_videos("query", max_results=5)

# For advanced filtering, use YouTube API:
if os.getenv("YOUTUBE_API_KEY"):
    api_results = toolkit.youtube_api.search_videos("query", max_results=10)
    # YouTube API provides better filtering options
```

#### 6. Handler Connection Issues
```python
# Test which handlers are working:
status = toolkit.test_handlers(url)
print(status)

# Use a specific working handler:
if status['yt_dlp']:
    video_path = toolkit.yt_dlp.download_video(url)
elif status['pytubefix']:
    video_path = toolkit.pytubefix.download_video(url)
```

#### 7. Anti-Detection Issues
```python
# Check anti-detection status:
status = toolkit.get_anti_detection_status()
print(status)

# Test anti-detection:
results = toolkit.test_anti_detection(url)
print(results)
```

#### 8. Output Path Issues
```python
# For PyTubeFix: Provide full path including filename
output_path = "/path/to/folder/video.mp4"

# For YT-DLP: Provide directory path only
output_path = "/path/to/folder/"

# Let the toolkit handle it automatically:
output_path = None  # Uses default location with video title
```

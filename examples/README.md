# YouTube Toolkit Examples

This directory contains practical examples demonstrating how to use the youtube-toolkit for building YouTube agents and applications.

## Examples Overview

### 1. YouTube Agent Example (`youtube_agent_example.py`)
A complete example showing how to build a YouTube agent with:
- **Video Analysis**: Extract metadata, captions, and content analysis
- **Search Functionality**: Find similar videos and content
- **Download Capabilities**: Download video and audio content
- **Content Classification**: Determine content type and educational value

**Usage:**
```bash
cd examples
python youtube_agent_example.py
```

### 2. Advanced Captions Examples (`advanced_captions_examples.py`)
Demonstrates advanced caption functionality:
- Caption listing and filtering
- Format conversion (SRT, VTT, TXT, TTML)
- Caption analysis and insights
- Search within captions

### 3. Advanced Comments Examples (`advanced_comments_examples.py`)
Shows comment analysis capabilities:
- Extract comments with pagination
- Filter comments by engagement
- Analyze comment sentiment
- Export comment data

### 4. Advanced Search Examples (`advanced_search_examples.py`)
Demonstrates sophisticated search features:
- Advanced filtering options
- Boolean search queries
- Category-based search
- Pagination and result management

### 5. Advanced Features Examples (`advanced_features_examples.py`)
Comprehensive feature showcase:
- Anti-detection mechanisms
- Playlist processing
- Batch operations
- Error handling

## Quick Start

### Basic Video Analysis
```python
from youtube_toolkit import YouTubeToolkit

# Initialize toolkit
toolkit = YouTubeToolkit(verbose=True)

# Analyze a video
url = "https://www.youtube.com/watch?v=VIDEO_ID"
info = toolkit.get_video_info(url)
captions = toolkit.advanced_download_captions(url, 'en', 'srt')

print(f"Title: {info['title']}")
print(f"Captions: {'Available' if captions['success'] else 'Not available'}")
```

### Search Videos
```python
# Search for videos
results = toolkit.search_videos("python tutorial", max_results=10)

for video in results:
    print(f"Title: {video['title']}")
    print(f"Channel: {video['channel_title']}")
    print(f"Views: {video['view_count']}")
    print("---")
```

### Download Content
```python
# Download audio
audio_result = toolkit.download_audio(url, format='mp3')

# Download video
video_result = toolkit.download_video(url, quality='best')

print(f"Downloaded: {audio_result['file_path']}")
```

## Building Your Own Agent

### 1. Basic Agent Structure
```python
class MyYouTubeAgent:
    def __init__(self):
        self.toolkit = YouTubeToolkit()
    
    def process_video(self, url: str):
        # Get metadata
        info = self.toolkit.get_video_info(url)
        
        # Get captions
        captions = self.toolkit.advanced_download_captions(url, 'en', 'srt')
        
        # Analyze content
        analysis = self.analyze_content(info, captions)
        
        return {
            'metadata': info,
            'captions': captions,
            'analysis': analysis
        }
```

### 2. Error Handling
```python
def robust_video_processing(self, url: str):
    try:
        result = self.toolkit.get_video_info(url)
        return {'status': 'success', 'data': result}
    except Exception as e:
        return {'status': 'error', 'error': str(e)}
```

### 3. Rate Limiting
```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

@rate_limit(calls_per_minute=30)
def search_videos(self, query: str):
    return self.toolkit.search_videos(query)
```

## Best Practices

### 1. Always Handle Errors
```python
try:
    result = toolkit.advanced_download_captions(url, 'en', 'srt')
    if result['success']:
        # Process successful result
        pass
    else:
        # Handle failure case
        print(f"Caption download failed: {result['error']}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

### 2. Use Fallback Mechanisms
```python
def get_captions_with_fallback(self, url: str):
    try:
        # Try YouTube API first
        result = toolkit.advanced_download_captions(url, 'en', 'srt')
        if result['success']:
            return result
    except Exception:
        pass
    
    try:
        # Fallback to yt-dlp
        result = toolkit.yt_dlp.download_captions(url, 'en')
        return {'success': True, 'output_path': result}
    except Exception as e:
        return {'success': False, 'error': str(e)}
```

### 3. Cache Results
```python
import json
import hashlib
from pathlib import Path

class CachedAgent:
    def __init__(self, cache_dir="cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_cached_result(self, url: str, operation: str):
        cache_key = hashlib.md5(f"{url}_{operation}".encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            with open(cache_file, 'r') as f:
                return json.load(f)
        return None
    
    def cache_result(self, url: str, operation: str, result: dict):
        cache_key = hashlib.md5(f"{url}_{operation}".encode()).hexdigest()
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        with open(cache_file, 'w') as f:
            json.dump(result, f)
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the correct directory and have installed dependencies
2. **API Key Issues**: Some features require YouTube API key - check your `.env` file
3. **Network Issues**: Implement retry logic for network requests
4. **Rate Limiting**: Use rate limiting decorators to avoid hitting API limits

### Getting Help

- Check the main documentation in `docs/YOUTUBE_AGENT_GUIDE.md`
- Review error messages carefully
- Test with simple examples first
- Use verbose mode for debugging

## Contributing

Feel free to add your own examples to this directory! When contributing:

1. Follow the existing code style
2. Include comprehensive error handling
3. Add comments explaining complex logic
4. Test your examples thoroughly
5. Update this README if adding new examples

Happy coding! 🚀
# Extending YouTube Toolkit

This guide explains how to extend youtube-toolkit with new features while following the established architecture.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Adding New Methods to Existing APIs](#adding-new-methods-to-existing-apis)
- [Adding New Handler Methods](#adding-new-handler-methods)
- [Creating Custom Post-Processors](#creating-custom-post-processors)
- [Using Hooks and Callbacks](#using-hooks-and-callbacks)

## Architecture Overview

youtube-toolkit follows a **three-layer architecture**:

```
┌─────────────────────────────────────────────────────────────┐
│           Sub-APIs (sub_apis.py) - User Interface           │
│     GetAPI │ DownloadAPI │ SearchAPI │ AnalyzeAPI │ StreamAPI│
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              API Layer (api.py) - YouTubeToolkit            │
│         Orchestration, fallback logic, unified interface    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│              Handler Layer (handlers/*.py)                  │
│   PyTubeFixHandler │ YTDLPHandler │ YouTubeAPIHandler       │
└─────────────────────────────────────────────────────────────┘
```

**Key Principle**: Sub-APIs call `api.py` methods, NOT handlers directly. This allows for fallback logic and cross-cutting concerns.

## Adding New Methods to Existing APIs

### Step 1: Add Handler Method

First, implement the raw functionality in the appropriate handler:

```python
# youtube_toolkit/handlers/pytubefix_handler.py

def get_video_statistics(self, url: str) -> Dict[str, Any]:
    """
    Get video statistics.
    
    Args:
        url: YouTube video URL
        
    Returns:
        Dict with views, likes, comments count
    """
    self._ensure_initialized()
    
    try:
        yt = self._create_yt(url)
        return {
            'views': yt.views,
            'length': yt.length,
            'rating': getattr(yt, 'rating', None),
        }
    except Exception as e:
        raise RuntimeError(f"Failed to get statistics: {e}")
```

### Step 2: Add API Layer Method (if fallback needed)

Add a method in `api.py` if you need fallback between handlers:

```python
# youtube_toolkit/api.py

def get_video_statistics(self, url: str) -> Dict[str, Any]:
    """Get video statistics with fallback."""
    try:
        return self.pytubefix.get_video_statistics(url)
    except Exception:
        # Fallback to yt-dlp
        return self.yt_dlp.get_video_statistics(url)
```

### Step 3: Expose in Sub-API

Add the user-facing method in the appropriate Sub-API:

```python
# youtube_toolkit/sub_apis.py

class GetAPI:
    # ... existing methods ...
    
    def statistics(self, url: str) -> Dict[str, Any]:
        """
        Get video statistics (views, likes, etc.).
        
        Args:
            url: Video URL
            
        Returns:
            Dict with video statistics
        """
        return self._toolkit.get_video_statistics(url)
```

### Step 4: Add Tests

```python
# tests/test_new_feature.py

def test_get_statistics_method_exists():
    from youtube_toolkit import YouTubeToolkit
    toolkit = YouTubeToolkit()
    assert hasattr(toolkit.get, 'statistics')
```

## Adding New Handler Methods

### Handler Method Template

```python
def new_method(self, url: str, **kwargs) -> ReturnType:
    """
    Brief description.
    
    Args:
        url: YouTube video URL
        **kwargs: Additional arguments
        
    Returns:
        Description of return value
        
    Raises:
        RuntimeError: If operation fails
    """
    self._ensure_initialized()
    
    try:
        # Implementation here
        pass
    except Exception as e:
        raise RuntimeError(f"Failed to do X: {e}")
```

### Handler Best Practices

1. **Always call `_ensure_initialized()`** at the start
2. **Use try/except** and raise `RuntimeError` with descriptive messages
3. **Document parameters and return types** in docstrings
4. **Return dictionaries** for complex data (easier to extend)

## Creating Custom Post-Processors

Post-processors transform downloaded content:

```python
from youtube_toolkit.core.post_processors import PostProcessorFactory

# Get available post-processors
factory = PostProcessorFactory()

# Create a custom post-processor
class CustomProcessor:
    def process(self, input_path: str, output_path: str, **kwargs) -> str:
        """
        Process the file.
        
        Args:
            input_path: Path to input file
            output_path: Desired output path
            
        Returns:
            Path to processed file
        """
        # Your processing logic here
        return output_path
```

## Using Hooks and Callbacks

### Progress Callbacks

```python
def my_progress_callback(percentage: float, message: str):
    print(f"Progress: {percentage:.1f}% - {message}")

# Use with downloads
toolkit.download.audio(url, progress_callback=my_progress_callback)
```

### Extending with Wrapper Classes

Create wrapper classes for custom behavior:

```python
from youtube_toolkit import YouTubeToolkit

class MyToolkit(YouTubeToolkit):
    """Custom toolkit with additional features."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_count = 0
    
    def download_audio(self, url: str, **kwargs) -> str:
        """Download audio with tracking."""
        result = super().download_audio(url, **kwargs)
        self.download_count += 1
        print(f"Total downloads: {self.download_count}")
        return result
```

## Example: Adding a New Sub-API

If you need an entirely new Sub-API:

```python
# youtube_toolkit/sub_apis.py

class MyCustomAPI:
    """
    Custom API for specific functionality.
    
    Usage:
        toolkit.custom.method(url)
    """
    
    def __init__(self, toolkit: 'YouTubeToolkit'):
        self._toolkit = toolkit
    
    def __call__(self, url: str) -> Any:
        """Default callable behavior."""
        return self.default_method(url)
    
    def default_method(self, url: str) -> Any:
        """The default method."""
        return self._toolkit.some_api_method(url)
    
    def other_method(self, url: str) -> Any:
        """Another method."""
        return self._toolkit.another_api_method(url)
```

Then register it in `api.py`:

```python
# youtube_toolkit/api.py

class YouTubeToolkit:
    def __init__(self, **kwargs):
        # ... existing initialization ...
        
        from .sub_apis import MyCustomAPI
        self.custom = MyCustomAPI(self)
```

## Contributing Guidelines

1. **Follow the layer architecture** - Don't skip layers
2. **Add tests** for new functionality
3. **Update documentation** (this file, README, docstrings)
4. **Use type hints** for all public methods
5. **Handle errors gracefully** with informative messages

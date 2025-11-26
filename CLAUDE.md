# CLAUDE.md - Development Principles for youtube-toolkit

This document contains development principles and architecture guidelines for Claude (or any AI assistant) when working on this codebase.

## Architecture Principles

### Three-Layer Architecture

The youtube-toolkit follows a strict three-layer architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                 api.py (YouTubeToolkit)                     │
│              THE HIGHEST LEVEL ENTRY POINT                  │
│                                                             │
│   Direct Methods:                                           │
│   - get_video_info(), download_audio(), search()            │
│   - get_sponsorblock_segments(), get_heatmap(), etc.        │
│                                                             │
│   Sub-APIs (attached as properties):                        │
│   - toolkit.get, toolkit.download, toolkit.search           │
│   - toolkit.sponsorblock, toolkit.live, toolkit.engagement  │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   sub_apis.py                               │
│   Sub-API classes that call api.py methods                  │
│   (GetAPI, DownloadAPI, SponsorBlockAPI, etc.)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   handlers/                                 │
│   Backend implementations                                   │
│   (PyTubeFixHandler, YTDLPHandler, YouTubeAPIHandler)       │
└─────────────────────────────────────────────────────────────┘
```

### CRITICAL: Layer Communication Rules

**Sub-APIs MUST call api.py methods, NOT handlers directly.**

```python
# ❌ WRONG - Sub-API calling handler directly
class SponsorBlockAPI:
    def segments(self, url: str):
        return self._toolkit.yt_dlp.get_sponsorblock_segments(url)  # BAD!

# ✅ CORRECT - Sub-API calling api.py method
class SponsorBlockAPI:
    def segments(self, url: str):
        return self._toolkit.get_sponsorblock_segments(url)  # GOOD!
```

**Why this matters:**
1. **Fallback Logic**: api.py methods can implement fallback between handlers
2. **Cross-cutting Concerns**: Logging, caching, rate limiting can be added at api.py level
3. **Consistency**: Single point of control for each feature
4. **Testability**: Easier to mock at api.py level

### Adding New Features

When adding a new feature, follow this pattern:

1. **Handler Layer** (`handlers/*.py`): Implement the raw functionality
   ```python
   # handlers/yt_dlp_handler.py
   def get_new_feature(self, url: str) -> Dict:
       # Raw implementation using yt-dlp
       ...
   ```

2. **API Layer** (`api.py`): Add wrapper method with fallback logic
   ```python
   # api.py
   def get_new_feature(self, url: str) -> Dict:
       # Try primary handler, fallback to secondary
       try:
           return self.pytubefix.get_new_feature(url)
       except Exception:
           return self.yt_dlp.get_new_feature(url)
   ```

3. **Sub-API Layer** (`sub_apis.py`): Add user-friendly interface
   ```python
   # sub_apis.py
   class NewFeatureAPI:
       def get(self, url: str) -> Dict:
           return self._toolkit.get_new_feature(url)  # Calls api.py!
   ```

4. **Initialize in api.py**
   ```python
   # api.py __init__
   from .sub_apis import NewFeatureAPI
   self.new_feature = NewFeatureAPI(self)
   ```

## Code Organization

### File Structure

```
youtube_toolkit/
├── api.py                 # Main entry point (YouTubeToolkit class)
├── sub_apis.py            # Sub-API classes (GetAPI, DownloadAPI, etc.)
├── handlers/
│   ├── pytubefix_handler.py    # Primary handler
│   ├── yt_dlp_handler.py       # Fallback handler
│   ├── youtube_api_handler.py  # Official API handler
│   └── scrapetube_handler.py   # Optional scraping handler
├── core/                  # Data classes and models
└── utils/                 # Utility functions
```

### Naming Conventions

- **api.py methods**: Use descriptive names like `get_video_info()`, `download_audio()`
- **sub_apis.py classes**: Use `*API` suffix like `GetAPI`, `DownloadAPI`, `SponsorBlockAPI`
- **handlers**: Use `*Handler` suffix like `YTDLPHandler`, `PyTubeFixHandler`

## Testing

- Tests are in `tests/` directory
- Run tests with: `uv run pytest tests/ -v`
- When adding new features, add corresponding tests
- Mock at the handler level for unit tests

## Version History

- **v0.3**: Added channel support, chapters, advanced search
- **v0.4**: Added Action-Based API (get, download, search sub-APIs)
- **v0.5**: Added advanced yt-dlp features (SponsorBlock, live streams, engagement data, etc.)

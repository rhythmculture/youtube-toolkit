# YouTube Toolkit API Guide

A focused tour of the five Sub-APIs exposed by `YouTubeToolkit`. Pair this with [`docs/REFERENCE.md`](REFERENCE.md) for architecture/background context.

## 1. Instantiating the Toolkit
```python
from youtube_toolkit import YouTubeToolkit
kit = YouTubeToolkit(verbose=True)  # verbose prints handler fallbacks
```
The instance wires up PyTubeFix, YT-DLP, the official YouTube API, and loads optional helpers (e.g., ScrapeTube) lazily.

## 2. Action Overview
| Action     | Call signature             | Default return |
|------------|---------------------------|----------------|
| `kit.get()`      | `kit.get(url, include=None)` | Dict (video/channel/playlist info) |
| `kit.download()` | `kit.download(url, *, type='audio', format='wav')` | `DownloadResult` |
| `kit.search()`   | `kit.search(query, max_results=20, filters=None)` | `SearchResult` |
| `kit.analyze()`  | `kit.analyze(url)` | Dict (insights) |
| `kit.stream()`   | `kit.stream(url, stream_type='audio')` | `bytes` |
Each action is callable (smart default) and exposes scoped helpers for advanced use.

## 3. GET API Snippets
```python
video = kit.get.video(url, include=['chapters','heatmap'])
channel = kit.get.channel("@fireship", limit=100)
playlist = kit.get.playlist(url)
comments = kit.get.comments(url, limit=50, order='time')
```
Extras such as transcripts, key moments, heatmaps, and restriction checks live under `kit.get.*`.

## 4. DOWNLOAD API Snippets
```python
# Audio
res = kit.download.audio(url, format='mp3', bitrate='320k')
# Video
res = kit.download.video(url, quality='1080p')
# Playlists / extras
kit.download.playlist(playlist_url, type='audio', format='m4a')
kit.download.captions(url, language_code='en', format='srt')
kit.download.with_sponsorblock(url)
```
Every helper returns a `DownloadResult` (path, backend, timing, success flag). Errors bubble up as `HandlerExecutionError` if all backends fail.

## 5. SEARCH API Snippets
```python
result = kit.search("python tutorial", max_results=25)
kit.search.videos("lofi", limit=10)
kit.search.with_filters(
    "ai news",
    duration='short',
    upload_date='week',
    features=['hd','live']
)
kit.search.trending(region='US')
```
The fallback order is PyTubeFix → PyTubeFix simple → YouTube API → ScrapeTube (if installed), all orchestrated by `YouTubeToolkit.search_videos`.

## 6. ANALYZE API Snippets
```python
kit.analyze(url)                       # rich metadata
kit.analyze.engagement(url)            # heatmap + key moments
kit.analyze.comments(url, limit=200)   # analytics + sentiment
kit.analyze.channel("@fireship")       # channel insights
kit.analyze.sponsorblock(url)          # sponsor segments
```

## 7. STREAM API Snippets
```python
buffer = kit.stream.audio(url, format='mp4', quality='best')
video_buffer = kit.stream.video(url, quality='720p')
kit.stream.live.status(live_url)
kit.stream.live.is_live(live_url)
```

## 8. Configuration Tips
- Set `YOUTUBE_API_KEY` for the official API features.
- Provide `YOUTUBE_COOKIES_FILE` to access region/age-restricted videos with YT-DLP.
- Install extras when needed:
  - `pip install youtube-toolkit[api]` for Google API client.
  - `pip install youtube-toolkit[scrapers]` for ScrapeTube.
- Use `kit.test_handlers(url)` to see which backends currently work.

## 9. Error Handling
```python
from youtube_toolkit import HandlerExecutionError

try:
    kit.download.audio(url)
except HandlerExecutionError as exc:
    for failure in exc.failures:
        print(failure.handler, failure.error)
```
The toolkit records each handler failure and surfaces them in one exception.

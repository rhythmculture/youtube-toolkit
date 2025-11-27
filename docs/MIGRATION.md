# API Migration Guide (Old → New)

The toolkit consolidated 27 ad-hoc helpers into five Sub-APIs (`get`, `download`, `search`, `analyze`, `stream`). Use this guide to map older method names/entry points to the modern equivalents.

## Quick Mapping Table
| Old call / concept | New call |
|--------------------|----------|
| `toolkit.get_video_info(url)` | `toolkit.get.video(url)` or `toolkit.get(url)` |
| `toolkit.download_audio(url, format='mp3')` | `toolkit.download.audio(url, format='mp3')` |
| `toolkit.download_video(url, quality='720p')` | `toolkit.download.video(url, quality='720p')` |
| `toolkit.search_videos(query)` | `toolkit.search(query)` or `toolkit.search.videos(query)` |
| `toolkit.get_channel_videos(handle, limit=50)` | `toolkit.get.channel.videos(handle, limit=50)` |
| `toolkit.get_channel_playlists(handle)` | `toolkit.get.channel.playlists(handle)` |
| `toolkit.get_playlist_info(url)` | `toolkit.get.playlist(url)` |
| `toolkit.get_playlist_urls(url)` | `toolkit.get.playlist.urls(url)` |
| `toolkit.get_comments(url, max_results=100)` | `toolkit.get.comments(url, limit=100, order='relevance')` |
| `toolkit.get_transcript(url)` | `toolkit.get.transcript(url)` |
| `toolkit.download_captions(url)` | `toolkit.download.captions(url, lang='en', format='srt')` |
| `toolkit.download_thumbnail(url)` | `toolkit.download.thumbnail(url, quality='maxres')` |
| `toolkit.download_playlist_audio(url)` | `toolkit.download.playlist(url, type='audio')` |
| `toolkit.download_with_sponsorblock(url)` | `toolkit.download.with_sponsorblock(url)` |
| `toolkit.stream_audio(url)` | `toolkit.stream.audio(url)` |
| `toolkit.stream_video(url)` | `toolkit.stream.video(url)` |
| `toolkit.get_live_status(url)` | `toolkit.stream.live.status(url)` |
| `toolkit.is_live(url)` | `toolkit.stream.live.is_live(url)` |
| `toolkit.get_rich_metadata(url)` | `toolkit.analyze(url)` |
| `toolkit.get_heatmap(url)` | `toolkit.analyze.engagement(url)` |

## Notes
- The new Sub-API objects are fully namespaced Python objects. Use dot-chaining (`toolkit.search.trending.by_category()`) instead of importing helper classes directly.
- All Sub-API calls route through `YouTubeToolkit` helpers, so handler fallbacks and new integrations happen automatically.
- Explicit helper methods (e.g., `toolkit.analyze.sponsorblock`, `toolkit.download.with_archive`) map 1:1 to earlier standalone helpers; only the namespace changed.
- For scripts that relied on direct handler usage (`toolkit.pytubefix.*`), prefer the new toolkit helpers. Direct handler usage is still possible but no longer required.

## Error Handling Changes
- Formerly silent failures now raise `HandlerExecutionError` once every handler fails; inspect `exc.failures` for handler-by-handler diagnostics.

## When in Doubt
- Search the README’s examples or skim `docs/API_GUIDE.md` for more detailed snippets.

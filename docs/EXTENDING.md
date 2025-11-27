# Extending YouTube Toolkit

This guide explains how to integrate a new backend (handler) or module without changing the public `YouTubeToolkit` API.

## 1. Understand the Layers
1. **Handlers (`youtube_toolkit/handlers/`)** wrap third-party libraries.
2. **Toolkit helpers (`youtube_toolkit/api.py`)** orchestrate handlers and implement fallback logic.
3. **Sub-APIs (`youtube_toolkit/sub_apis.py`)** call toolkit helpers only.

When you add a new capability, touch those layers in that order.

## 2. Adding a New Handler
1. **Create the handler class** in `youtube_toolkit/handlers/your_handler.py`.
   ```python
   class PyYTSearchHandler:
       def __init__(self):
           ...
       def search_videos(self, query: str, max_results: int) -> list[dict]:
           ...
   ```
2. **Import it in `api.py`** (guarded if optional).
   ```python
   try:
       from .handlers.py_yt_search_handler import PyYTSearchHandler
   except ImportError:
       PyYTSearchHandler = None
   ```
3. **Instantiate lazily** (if optional) via a helper similar to `_get_scrapetube_handler`.
4. **Wire it into orchestration** by updating the relevant helper, e.g.:
   ```python
   attempts.append(("PyYTSearch", lambda: self.py_yt_search.search_videos(...)))
   ```
5. **Expose configuration** if needed (constructor flags, env vars).

## 3. Updating Fallback Logic
- Keep fallback order fast → resilient → official.
- Use `_record_handler_failure(...)` so verbose output and `HandlerExecutionError` include the new handler’s failures.
- Prefer declarative lists (e.g., `attempts = [("PyTubeFix", func), ...]`) for clarity.

## 4. Extending Sub-APIs
Because Sub-APIs call toolkit helpers, most new functionality only requires:
1. Add a helper on `YouTubeToolkit` (e.g., `def get_sponsor_segments(...)`).
2. Expose it through the relevant Sub-API by calling that helper.

Avoid importing handlers directly inside Sub-APIs; this keeps the public API stable and makes new handlers automatic.

## 5. Exposing Optional Extras
Provide an installation extra when the handler needs additional packages.
```toml
[project.optional-dependencies]
scrapers = ["scrapetube>=2.0"]
pyyt = ["py-yt-search"]
```
Document the extra in README/REFERENCE so users know how to enable it.

## 6. Testing
- Add handler-specific unit tests under `tests/` (mock third-party APIs when necessary).
- Run the whole suite (`uv run pytest`) to ensure fallbacks still pass existing expectations.

Following this pattern keeps the five core Sub-APIs unchanged even as new modules are added.

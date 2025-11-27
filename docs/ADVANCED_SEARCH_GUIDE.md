# Advanced Search Guide - YouTube Toolkit

This guide covers the enhanced search capabilities integrated from YouTube API v3, providing comprehensive filtering, thumbnail management, live content detection, and rich metadata extraction.

## Table of Contents

1. [Overview](#overview)
2. [Enhanced Search Models](#enhanced-search-models)
3. [Advanced Search Filters](#advanced-search-filters)
4. [Thumbnail Management](#thumbnail-management)
5. [Live Content Detection](#live-content-detection)
6. [Event Type Filtering](#event-type-filtering)
7. [Category Filtering](#category-filtering)
8. [Boolean Search Operators](#boolean-search-operators)
9. [Pagination Support](#pagination-support)
10. [Content Ownership Features](#content-ownership-features)
11. [Quota Management](#quota-management)
12. [Search Examples](#search-examples)
13. [API Reference](#api-reference)

## Overview

The enhanced search functionality provides:

- **Rich metadata extraction** with thumbnails, live content status, and comprehensive details
- **Advanced filtering** by date, duration, quality, captions, license, and more
- **Multiple resource types** (videos, channels, playlists)
- **Thumbnail management** with multiple resolutions
- **Live content detection** (live streams, upcoming broadcasts)
- **Event type filtering** (live, upcoming, completed broadcasts)
- **Category filtering** (Gaming, Music, Education, etc.)
- **Boolean search operators** (NOT -, OR |)
- **Pagination support** for large result sets
- **Content ownership features** (enterprise-level)
- **Sponsored content detection**
- **Quota management** awareness
- **Filter validation** to prevent API errors
- **Backward compatibility** with existing search methods

## Enhanced Search Models

### SearchResultItem

Represents individual search results with comprehensive metadata:

```python
from youtube_toolkit import SearchResultItem

item = SearchResultItem(
    kind="youtube#video",  # Resource type
    etag="unique_etag",
    video_id="dQw4w9WgXcQ",
    title="Video Title",
    description="Video description...",
    channel_title="Channel Name",
    published_at=datetime.now(),
    thumbnails=thumbnails_object,
    live_broadcast_content="none"  # none, live, upcoming
)
```

### SearchFilters

Comprehensive filtering options matching YouTube API v3:

```python
from youtube_toolkit import SearchFilters
from datetime import datetime, timedelta

filters = SearchFilters(
    # Resource type filtering
    type="video",  # video, channel, playlist
    
    # Channel filtering
    channel_id="UC_x5XG1OV2P6uZZ5FSM9Ttw",
    channel_type="any",  # any, show
    
    # Date filtering
    published_after=datetime.now() - timedelta(days=30),
    published_before=datetime.now(),
    
    # Duration filtering
    video_duration="medium",  # any, short, medium, long
    
    # Quality filtering
    video_definition="high",  # any, high, standard
    video_dimension="2d",  # any, 2d, 3d
    
    # Content filtering
    video_caption="closedCaption",  # any, closedCaption, none
    video_license="creativeCommon",  # any, creativeCommon, youtube
    video_embeddable="true",  # any, true
    video_syndicated="any",  # any, true
    video_type="any",  # any, episode, movie
    
    # Ordering
    order="viewCount",  # relevance, date, rating, viewCount, title
    
    # Location and language
    location="37.42307,-122.08427",  # latitude,longitude
    location_radius="1000km",  # radius
    relevance_language="en",  # language code
    
    # Region and safety
    region_code="US",  # country code
    safe_search="moderate"  # moderate, none, strict
)
```

### Thumbnails

Multi-resolution thumbnail management:

```python
from youtube_toolkit import Thumbnails, Thumbnail

# Thumbnail qualities available:
# - default: 120x90 (video) or 88x88 (channel)
# - medium: 320x180 (video) or 240x240 (channel)
# - high: 480x360 (video) or 800x800 (channel)
# - standard: 640x480 (video only)
# - maxres: 1280x720 (video only)

thumbnails = Thumbnails(
    default=Thumbnail(url="...", width=120, height=90),
    medium=Thumbnail(url="...", width=320, height=180),
    high=Thumbnail(url="...", width=480, height=360),
    standard=Thumbnail(url="...", width=640, height=480),
    maxres=Thumbnail(url="...", width=1280, height=720)
)

# Get best available thumbnail
best_thumbnail = thumbnails.get_best_thumbnail()

# Get thumbnail by preferred size
medium_thumbnail = thumbnails.get_thumbnail_by_size(preferred_width=320)
```

## Advanced Search Filters

### Resource Type Filtering

```python
# Search for videos only
filters = SearchFilters(type="video")

# Search for channels only
filters = SearchFilters(type="channel")

# Search for playlists only
filters = SearchFilters(type="playlist")

# Search for all types
filters = SearchFilters(type="video,channel,playlist")
```

### Date Range Filtering

```python
from datetime import datetime, timedelta

# Last 30 days
filters = SearchFilters(
    published_after=datetime.now() - timedelta(days=30),
    published_before=datetime.now()
)

# Specific date range
filters = SearchFilters(
    published_after=datetime(2024, 1, 1),
    published_before=datetime(2024, 12, 31)
)
```

### Duration Filtering

```python
# Short videos (under 4 minutes)
filters = SearchFilters(video_duration="short")

# Medium videos (4-20 minutes)
filters = SearchFilters(video_duration="medium")

# Long videos (over 20 minutes)
filters = SearchFilters(video_duration="long")
```

### Quality and Content Filtering

```python
# High definition only
filters = SearchFilters(video_definition="high")

# Must have captions
filters = SearchFilters(video_caption="closedCaption")

# Creative Commons license
filters = SearchFilters(video_license="creativeCommon")

# Embeddable videos only
filters = SearchFilters(video_embeddable="true")
```

### Ordering Options

```python
# Sort by relevance (default)
filters = SearchFilters(order="relevance")

# Sort by upload date
filters = SearchFilters(order="date")

# Sort by rating
filters = SearchFilters(order="rating")

# Sort by view count
filters = SearchFilters(order="viewCount")

# Sort by title
filters = SearchFilters(order="title")
```

## Thumbnail Management

### Accessing Thumbnails

```python
# Perform search
results = toolkit.advanced_search("python tutorial")

# Get thumbnails from first result
first_item = results['items'][0]
thumbnails = first_item['thumbnails']

if thumbnails:
    # Access specific resolutions
    default_url = thumbnails['default']['url']
    high_url = thumbnails['high']['url']
    maxres_url = thumbnails['maxres']['url']
```

### Thumbnail Analysis

```python
from youtube_toolkit import SearchResult

# Convert results to SearchResult object
search_result = SearchResult.from_dict(results)

# Get thumbnail summary
summary = search_result.get_thumbnails_summary()
print(f"Default thumbnails: {summary['default']}")
print(f"High quality thumbnails: {summary['high']}")
print(f"Max resolution thumbnails: {summary['maxres']}")

# Get items with specific thumbnail quality
high_quality_items = search_result.get_items_with_thumbnails(min_width=480)
```

## Live Content Detection

### Identifying Live Content

```python
# Search for live content
results = toolkit.advanced_search("gaming stream")

# Filter for live content
live_items = [item for item in results['items'] 
              if item['live_broadcast_content'] in ['live', 'upcoming']]

# Using SearchResult object
search_result = SearchResult.from_dict(results)
live_content = search_result.get_live_content()
live_streams = search_result.get_live_streams()
upcoming_streams = search_result.get_upcoming_streams()
```

### Live Content Properties

```python
for item in results['items']:
    if item['live_broadcast_content'] == 'live':
        print(f"🔴 LIVE: {item['title']}")
    elif item['live_broadcast_content'] == 'upcoming':
        print(f"⏰ UPCOMING: {item['title']}")
    else:
        print(f"📹 REGULAR: {item['title']}")
```

## Event Type Filtering

### Live Broadcast Management

```python
# Search for currently live streams
live_results = toolkit.search_live_content("gaming", event_type="live")

# Search for upcoming broadcasts
upcoming_results = toolkit.search_live_content("tech conference", event_type="upcoming")

# Search for completed broadcasts
completed_results = toolkit.search_live_content("webinar", event_type="completed")
```

### Event Type Options

- **`live`**: Currently active broadcasts
- **`upcoming`**: Scheduled broadcasts that haven't started
- **`completed`**: Finished broadcasts

## Category Filtering

### YouTube Category Search

```python
# Search in specific categories
gaming_results = toolkit.search_by_category("tutorial", "Gaming")
music_results = toolkit.search_by_category("review", "Music")
education_results = toolkit.search_by_category("course", "Education")

# Get available categories
categories = toolkit.get_search_categories()
print(f"Available categories: {list(categories.keys())}")
```

### Available Categories

```python
from youtube_toolkit import YOUTUBE_CATEGORIES

# Common categories
categories = {
    "Gaming": "20",
    "Music": "10", 
    "Education": "27",
    "Science & Technology": "28",
    "Entertainment": "24",
    "News & Politics": "25",
    "Howto & Style": "26",
    "Sports": "17",
    "Comedy": "23",
    "People & Blogs": "22"
}
```

## Boolean Search Operators

### NOT Operator (-)

```python
# Exclude specific terms
results = toolkit.search_with_boolean_query("python -tutorial")
results = toolkit.search_with_boolean_query("gaming -mobile")
```

### OR Operator (|)

```python
# Search for multiple terms
results = toolkit.search_with_boolean_query("gaming|streaming")
results = toolkit.search_with_boolean_query("python|javascript|java")
```

### Complex Boolean Queries

```python
# Complex queries with parentheses
results = toolkit.search_with_boolean_query("machine learning -beginner (tutorial|course|guide)")

# Using BooleanSearchQuery class
from youtube_toolkit import BooleanSearchQuery

query = BooleanSearchQuery()
query.add_term("artificial intelligence")
query.add_excluded_term("beginner")
query.add_or_group(["tutorial", "course", "guide"])

results = toolkit.search_with_boolean_query(str(query))
```

## Pagination Support

### Basic Pagination

```python
# First page
page1 = toolkit.search_paginated("python programming", max_results=10)

# Get next page token
next_token = page1.get('next_page_token')

# Second page
if next_token:
    page2 = toolkit.search_paginated(
        "python programming", 
        page_token=next_token, 
        max_results=10
    )
```

### Pagination with Filters

```python
filters = SearchFilters(
    type="video",
    video_duration="medium",
    order="date"
)

# First page with filters
page1 = toolkit.search_paginated("tutorial", filters, max_results=20)

# Continue pagination
next_token = page1.get('next_page_token')
while next_token:
    page = toolkit.search_paginated("tutorial", filters, next_token, 20)
    next_token = page.get('next_page_token')
```

## Content Ownership Features

### Enterprise-Level Search

```python
# Search only user's own videos (requires authentication)
filters = SearchFilters(
    type="video",
    for_mine=True,
    order="date"
)

# Search only developer-uploaded videos
filters = SearchFilters(
    type="video", 
    for_developer=True
)

# Search only content owner's videos
filters = SearchFilters(
    type="video",
    for_content_owner=True,
    on_behalf_of_content_owner="content_owner_id"
)
```

### Authentication Requirements

These features require:
- OAuth2 authentication
- Content owner permissions
- Developer account setup

## Quota Management

### Quota Awareness

```python
# Each search costs 100 quota units
results = toolkit.advanced_search("query")

print(f"Quota cost: {results.get('quota_cost')} units")
print(f"Daily limit: 10,000 units (default)")
print(f"Max searches per day: ~100")
```

### Minimizing Quota Usage

```python
# Use specific filters to reduce API calls
filters = SearchFilters(
    type="video",
    video_duration="medium",
    published_after=datetime.now() - timedelta(days=7)
)

# Cache results when possible
# Use pagination efficiently
# Monitor quota in Google Cloud Console
```

## Search Examples

### Basic Advanced Search

```python
from youtube_toolkit import YouTubeToolkit

toolkit = YouTubeToolkit(verbose=True)

# Basic advanced search
results = toolkit.advanced_search("machine learning tutorial")

print(f"Found {len(results['items'])} results")
for item in results['items'][:3]:
    print(f"- {item['title']} by {item['channel_title']}")
```

### Filtered Search

```python
from youtube_toolkit import SearchFilters
from datetime import datetime, timedelta

# Create filters
filters = SearchFilters(
    type="video",
    video_duration="medium",
    order="viewCount",
    published_after=datetime.now() - timedelta(days=7),
    video_definition="high"
)

# Search with filters
results = toolkit.advanced_search("python programming", filters, max_results=10)
```

### Channel-Specific Search

```python
# Search for channels
filters = SearchFilters(type="channel")
results = toolkit.advanced_search("tech review", filters)

for item in results['items']:
    print(f"Channel: {item['title']}")
    print(f"ID: {item['channel_id']}")
    print(f"Description: {item['description'][:100]}...")
```

### Date Range Search

```python
from datetime import datetime, timedelta

# Search for recent content
filters = SearchFilters(
    published_after=datetime.now() - timedelta(days=3),
    order="date"
)

results = toolkit.advanced_search("news", filters)
```

### Comprehensive Search

```python
# Complex search with multiple filters
filters = SearchFilters(
    type="video",
    video_duration="long",
    video_definition="high",
    video_caption="closedCaption",
    video_license="creativeCommon",
    order="rating",
    region_code="US",
    relevance_language="en",
    safe_search="strict"
)

results = toolkit.advanced_search("educational content", filters, max_results=20)
```

## API Reference

### YouTubeToolkit.advanced_search()

```python
def advanced_search(self, query: str, filters: Optional[Dict] = None, max_results: int = 20) -> Dict[str, Any]:
    """
    Advanced search with comprehensive filtering and rich results.
    
    Args:
        query: Search query string
        filters: SearchFilters object or dict with advanced filtering options
        max_results: Maximum number of results to return (max 50)
        
    Returns:
        Dictionary with comprehensive search results including thumbnails, live content, etc.
    """
```

### SearchResult Methods

```python
# Filtering methods
search_result.get_items_by_type("video")  # Get videos only
search_result.get_items_by_channel("Channel Name")  # Get items from specific channel
search_result.get_live_content()  # Get all live content
search_result.get_live_streams()  # Get currently live streams
search_result.get_upcoming_streams()  # Get upcoming streams
search_result.filter_by_date_range(start_date, end_date)  # Filter by date range

# Sorting methods
search_result.sort_by_published_date(reverse=True)  # Sort by date

# Analysis methods
search_result.get_thumbnails_summary()  # Get thumbnail availability summary
search_result.get_items_with_thumbnails(min_width=320)  # Get items with specific thumbnail quality

# Properties
search_result.video_count  # Number of video items
search_result.channel_count  # Number of channel items
search_result.playlist_count  # Number of playlist items
search_result.live_content_count  # Number of live content items
```

### SearchFilters Properties

```python
# Resource filtering
filters.type  # video, channel, playlist
filters.channel_id  # Specific channel ID
filters.channel_type  # any, show

# Date filtering
filters.published_after  # datetime object
filters.published_before  # datetime object

# Video filtering
filters.video_duration  # any, short, medium, long
filters.video_definition  # any, high, standard
filters.video_dimension  # any, 2d, 3d
filters.video_caption  # any, closedCaption, none
filters.video_license  # any, creativeCommon, youtube
filters.video_embeddable  # any, true
filters.video_syndicated  # any, true
filters.video_type  # any, episode, movie

# Ordering
filters.order  # relevance, date, rating, viewCount, title

# Location and language
filters.location  # latitude,longitude
filters.location_radius  # radius in meters/km
filters.relevance_language  # language code

# Region and safety
filters.region_code  # country code
filters.safe_search  # moderate, none, strict
```

## Setup Requirements

### API Key Setup

```bash
# Set your YouTube API key
export YOUTUBE_API_KEY="your_api_key_here"

# Get API key from Google Cloud Console
# https://console.developers.google.com/
```

### Dependencies

```bash
# Install required packages
uv add google-api-python-client
uv add python-dotenv
```

### Environment Variables

Create a `.env` file:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
```

## Best Practices

1. **Use appropriate filters** to reduce API quota usage
2. **Cache results** when possible to avoid repeated API calls
3. **Handle rate limits** gracefully with retry logic
4. **Use pagination** for large result sets
5. **Validate API key** before making requests
6. **Monitor quota usage** in Google Cloud Console

## Error Handling

```python
try:
    results = toolkit.advanced_search("query", filters)
    if results.get('error'):
        print(f"Search error: {results['error']}")
    else:
        print(f"Found {len(results['items'])} results")
except Exception as e:
    print(f"Search failed: {e}")
```

## Migration from Basic Search

The enhanced search is backward compatible. Existing code will continue to work:

```python
# Old way (still works)
results = toolkit.search_videos("query")

# New way (enhanced)
results = toolkit.advanced_search("query", filters)
```

For more examples, see `examples/advanced_search_examples.py`.
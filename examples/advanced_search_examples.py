"""
Advanced Search Examples for YouTube Toolkit

This file demonstrates the enhanced search capabilities integrated from YouTube API v3,
including thumbnails, live content detection, advanced filtering, and comprehensive results.
"""

import os
from datetime import datetime, timedelta
from youtube_toolkit import YouTubeToolkit
from youtube_toolkit.core.search import SearchFilters, SearchResult


def setup_toolkit():
    """Initialize YouTube Toolkit with verbose output."""
    return YouTubeToolkit(verbose=True)


def example_basic_advanced_search():
    """Example 1: Basic advanced search with default settings."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Advanced Search")
    print("="*60)
    
    toolkit = setup_toolkit()
    
    # Basic advanced search
    results = toolkit.advanced_search("python programming tutorial")
    
    print(f"Query: 'python programming tutorial'")
    print(f"Total results: {results.get('total_results', 0)}")
    print(f"Items found: {len(results.get('items', []))}")
    print(f"Backend used: {results.get('backend_used', 'unknown')}")
    
    # Display first few results
    for i, item in enumerate(results.get('items', [])[:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   Channel: {item.get('channel_title', 'Unknown')}")
        print(f"   Type: {item.get('kind', 'unknown')}")
        print(f"   Live content: {item.get('live_broadcast_content', 'none')}")
        if item.get('thumbnails'):
            thumbnails = item['thumbnails']
            print(f"   Thumbnails available: {[k for k, v in thumbnails.items() if v]}")


def example_search_with_filters():
    """Example 2: Search with advanced filters."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Search with Advanced Filters")
    print("="*60)
    
    toolkit = setup_toolkit()
    
    # Create search filters
    filters = SearchFilters(
        type="video",  # Only videos
        video_duration="medium",  # Medium length videos (4-20 minutes)
        order="viewCount",  # Sort by view count
        published_after=datetime.now() - timedelta(days=30),  # Last 30 days
        video_definition="high",  # High definition only
        safe_search="moderate"  # Moderate safety filter
    )
    
    results = toolkit.advanced_search("machine learning", filters, max_results=10)
    
    print(f"Query: 'machine learning' with filters")
    print(f"Filters applied:")
    print(f"  - Type: {filters.type}")
    print(f"  - Duration: {filters.video_duration}")
    print(f"  - Order: {filters.order}")
    print(f"  - Published after: {filters.published_after}")
    print(f"  - Definition: {filters.video_definition}")
    print(f"  - Safe search: {filters.safe_search}")
    
    print(f"\nResults: {len(results.get('items', []))} items found")
    
    # Display results with additional info
    for i, item in enumerate(results.get('items', [])[:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   Channel: {item.get('channel_title', 'Unknown')}")
        print(f"   Published: {item.get('published_at', 'Unknown')}")
        print(f"   Video ID: {item.get('video_id', 'Unknown')}")


def example_live_content_search():
    """Example 3: Search for live content."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Live Content Search")
    print("="*60)
    
    toolkit = setup_toolkit()
    
    # Search for live content
    results = toolkit.advanced_search("gaming live stream")
    
    print(f"Query: 'gaming live stream'")
    print(f"Total results: {results.get('total_results', 0)}")
    
    # Filter for live content
    live_items = [item for item in results.get('items', []) 
                  if item.get('live_broadcast_content') in ['live', 'upcoming']]
    
    print(f"Live/upcoming content: {len(live_items)} items")
    
    for i, item in enumerate(live_items[:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   Channel: {item.get('channel_title', 'Unknown')}")
        print(f"   Status: {item.get('live_broadcast_content', 'none')}")
        print(f"   Video ID: {item.get('video_id', 'Unknown')}")


def example_channel_search():
    """Example 4: Search for channels."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Channel Search")
    print("="*60)
    
    toolkit = setup_toolkit()
    
    # Search for channels
    filters = SearchFilters(type="channel")
    results = toolkit.advanced_search("tech review", filters, max_results=10)
    
    print(f"Query: 'tech review' channels")
    print(f"Results: {len(results.get('items', []))} channels found")
    
    for i, item in enumerate(results.get('items', [])[:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   Channel ID: {item.get('channel_id', 'Unknown')}")
        print(f"   Description: {item.get('description', 'No description')[:100]}...")


def example_thumbnail_management():
    """Example 5: Thumbnail management and analysis."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Thumbnail Management")
    print("="*60)
    
    toolkit = setup_toolkit()
    
    # Search for videos with thumbnails
    results = toolkit.advanced_search("nature documentary")
    
    print(f"Query: 'nature documentary'")
    print(f"Results: {len(results.get('items', []))} items found")
    
    # Analyze thumbnails
    thumbnail_summary = {"default": 0, "medium": 0, "high": 0, "standard": 0, "maxres": 0}
    
    for item in results.get('items', []):
        thumbnails = item.get('thumbnails', {})
        for quality in thumbnail_summary.keys():
            if thumbnails.get(quality):
                thumbnail_summary[quality] += 1
    
    print(f"\nThumbnail availability:")
    for quality, count in thumbnail_summary.items():
        print(f"  {quality}: {count} items")
    
    # Show thumbnail URLs for first result
    first_item = results.get('items', [{}])[0]
    if first_item.get('thumbnails'):
        print(f"\nFirst result thumbnails:")
        thumbnails = first_item['thumbnails']
        for quality, thumbnail_data in thumbnails.items():
            if thumbnail_data:
                print(f"  {quality}: {thumbnail_data['url']} ({thumbnail_data['width']}x{thumbnail_data['height']})")


def example_date_range_search():
    """Example 6: Search within specific date range."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Date Range Search")
    print("="*60)
    
    toolkit = setup_toolkit()
    
    # Search for videos from last week
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    
    filters = SearchFilters(
        published_after=start_date,
        published_before=end_date,
        order="date",  # Sort by date
        video_duration="short"  # Short videos only
    )
    
    results = toolkit.advanced_search("news", filters, max_results=10)
    
    print(f"Query: 'news' from last week")
    print(f"Date range: {start_date.date()} to {end_date.date()}")
    print(f"Results: {len(results.get('items', []))} items found")
    
    for i, item in enumerate(results.get('items', [])[:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   Channel: {item.get('channel_title', 'Unknown')}")
        print(f"   Published: {item.get('published_at', 'Unknown')}")


def example_comprehensive_search():
    """Example 7: Comprehensive search with multiple filters."""
    print("\n" + "="*60)
    print("EXAMPLE 7: Comprehensive Search")
    print("="*60)
    
    toolkit = setup_toolkit()
    
    # Comprehensive filters
    filters = SearchFilters(
        type="video",
        video_duration="long",  # Long videos (>20 minutes)
        video_definition="high",
        video_caption="closedCaption",  # Must have captions
        video_license="creativeCommon",  # Creative Commons license
        order="rating",  # Sort by rating
        region_code="US",  # US region
        relevance_language="en",  # English language
        safe_search="strict"  # Strict safety filter
    )
    
    results = toolkit.advanced_search("educational content", filters, max_results=15)
    
    print(f"Query: 'educational content' with comprehensive filters")
    print(f"Filters:")
    print(f"  - Duration: {filters.video_duration}")
    print(f"  - Definition: {filters.video_definition}")
    print(f"  - Captions: {filters.video_caption}")
    print(f"  - License: {filters.video_license}")
    print(f"  - Order: {filters.order}")
    print(f"  - Region: {filters.region_code}")
    print(f"  - Language: {filters.relevance_language}")
    print(f"  - Safety: {filters.safe_search}")
    
    print(f"\nResults: {len(results.get('items', []))} items found")
    
    # Show detailed results
    for i, item in enumerate(results.get('items', [])[:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   Channel: {item.get('channel_title', 'Unknown')}")
        print(f"   Description: {item.get('description', 'No description')[:150]}...")
        print(f"   Video ID: {item.get('video_id', 'Unknown')}")


def example_search_result_analysis():
    """Example 8: Analyze search results."""
    print("\n" + "="*60)
    print("EXAMPLE 8: Search Result Analysis")
    print("="*60)
    
    toolkit = setup_toolkit()
    
    # Perform search
    results = toolkit.advanced_search("python tutorial")
    
    # Convert to SearchResult object for analysis
    search_result = SearchResult.from_dict(results)
    
    print(f"Query: 'python tutorial'")
    print(f"Total results: {search_result.total_results}")
    print(f"Items found: {search_result.count}")
    print(f"Videos: {search_result.video_count}")
    print(f"Channels: {search_result.channel_count}")
    print(f"Playlists: {search_result.playlist_count}")
    print(f"Live content: {search_result.live_content_count}")
    
    # Get thumbnails summary
    thumbnail_summary = search_result.get_thumbnails_summary()
    print(f"\nThumbnail summary: {thumbnail_summary}")
    
    # Filter by channel
    channels = search_result.get_items_by_channel("TechWorld")
    print(f"\nItems from 'TechWorld' channel: {len(channels)}")
    
    # Get live content
    live_content = search_result.get_live_content()
    print(f"Live content items: {len(live_content)}")
    
    # Sort by published date
    recent_items = search_result.sort_by_published_date(reverse=True)[:3]
    print(f"\nMost recent items:")
    for i, item in enumerate(recent_items, 1):
        print(f"  {i}. {item.title} ({item.published_at})")


def main():
    """Run all examples."""
    print("YouTube Toolkit - Advanced Search Examples")
    print("=" * 60)
    
    # Check if API key is available
    if not os.getenv("YOUTUBE_API_KEY"):
        print("⚠️  Warning: YOUTUBE_API_KEY not set. Some features may not work.")
        print("   Set your API key: export YOUTUBE_API_KEY='your_api_key_here'")
        print("   Get API key from: https://console.developers.google.com/")
        print()
    
    try:
        example_basic_advanced_search()
        example_search_with_filters()
        example_live_content_search()
        example_channel_search()
        example_thumbnail_management()
        example_date_range_search()
        example_comprehensive_search()
        example_search_result_analysis()
        
        print("\n" + "="*60)
        print("All examples completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have:")
        print("1. Installed all dependencies: uv add google-api-python-client")
        print("2. Set your YouTube API key: export YOUTUBE_API_KEY='your_key'")
        print("3. Internet connection for API calls")


if __name__ == "__main__":
    main()
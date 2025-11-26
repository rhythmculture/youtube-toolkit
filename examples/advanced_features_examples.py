"""
Advanced Features Examples for YouTube Toolkit

This file demonstrates the newly integrated advanced features from the complete YouTube Search API,
including event type filtering, content ownership, category filtering, Boolean search, and more.
"""

import os
from datetime import datetime, timedelta
from youtube_toolkit import YouTubeToolkit, SearchFilters, BooleanSearchQuery, YOUTUBE_CATEGORIES


def setup_toolkit():
    """Initialize YouTube Toolkit with verbose output."""
    return YouTubeToolkit(verbose=True)


def example_event_type_filtering():
    """Example 1: Event Type Filtering (Live Broadcast Management)."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Event Type Filtering (Live Broadcast Management)")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Search for currently live streams
    print("🔴 Searching for LIVE streams...")
    live_results = toolkit.search_live_content("gaming", event_type="live", max_results=10)
    
    print(f"Live streams found: {len(live_results.get('items', []))}")
    for i, item in enumerate(live_results.get('items', [])[:3], 1):
        print(f"  {i}. {item.get('title', 'No title')}")
        print(f"     Channel: {item.get('channel_title', 'Unknown')}")
        print(f"     Status: {item.get('live_broadcast_content', 'none')}")
    
    # Search for upcoming broadcasts
    print("\n⏰ Searching for UPCOMING broadcasts...")
    upcoming_results = toolkit.search_live_content("tech conference", event_type="upcoming", max_results=5)
    
    print(f"Upcoming broadcasts found: {len(upcoming_results.get('items', []))}")
    for i, item in enumerate(upcoming_results.get('items', [])[:3], 1):
        print(f"  {i}. {item.get('title', 'No title')}")
        print(f"     Channel: {item.get('channel_title', 'Unknown')}")
        print(f"     Status: {item.get('live_broadcast_content', 'none')}")
    
    # Search for completed broadcasts
    print("\n✅ Searching for COMPLETED broadcasts...")
    completed_results = toolkit.search_live_content("webinar", event_type="completed", max_results=5)
    
    print(f"Completed broadcasts found: {len(completed_results.get('items', []))}")
    for i, item in enumerate(completed_results.get('items', [])[:3], 1):
        print(f"  {i}. {item.get('title', 'No title')}")
        print(f"     Channel: {item.get('channel_title', 'Unknown')}")


def example_category_filtering():
    """Example 2: Category Filtering."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Category Filtering")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Show available categories
    categories = toolkit.get_search_categories()
    print("Available YouTube categories:")
    for name, category_id in list(categories.items())[:10]:  # Show first 10
        print(f"  {name}: {category_id}")
    print(f"  ... and {len(categories) - 10} more categories")
    
    # Search in specific categories
    categories_to_search = ["Gaming", "Education", "Music", "Science & Technology"]
    
    for category in categories_to_search:
        print(f"\n🎯 Searching '{category}' category...")
        try:
            results = toolkit.search_by_category("tutorial", category, max_results=5)
            print(f"  Found {len(results.get('items', []))} results in {category}")
            
            for i, item in enumerate(results.get('items', [])[:2], 1):
                print(f"    {i}. {item.get('title', 'No title')}")
                print(f"       Channel: {item.get('channel_title', 'Unknown')}")
        except ValueError as e:
            print(f"  Error: {e}")


def example_sponsored_content_detection():
    """Example 3: Sponsored Content Detection."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Sponsored Content Detection")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Search for sponsored content
    print("💰 Searching for sponsored content...")
    sponsored_results = toolkit.search_sponsored_content("product review", max_results=10)
    
    print(f"Sponsored content found: {len(sponsored_results.get('items', []))}")
    print(f"Quota cost: {sponsored_results.get('quota_cost', 'Unknown')} units")
    
    for i, item in enumerate(sponsored_results.get('items', [])[:3], 1):
        print(f"  {i}. {item.get('title', 'No title')}")
        print(f"     Channel: {item.get('channel_title', 'Unknown')}")
        print(f"     Description: {item.get('description', 'No description')[:100]}...")


def example_boolean_search():
    """Example 4: Boolean Search Operators."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Boolean Search Operators")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Example 1: Exclude terms (NOT operator)
    print("❌ Searching 'python -tutorial' (exclude tutorials)...")
    exclude_results = toolkit.search_with_boolean_query("python -tutorial", max_results=10)
    
    print(f"Results (excluding tutorials): {len(exclude_results.get('items', []))}")
    for i, item in enumerate(exclude_results.get('items', [])[:3], 1):
        print(f"  {i}. {item.get('title', 'No title')}")
    
    # Example 2: OR operator
    print("\n🔄 Searching 'gaming|streaming' (gaming OR streaming)...")
    or_results = toolkit.search_with_boolean_query("gaming|streaming", max_results=10)
    
    print(f"Results (gaming OR streaming): {len(or_results.get('items', []))}")
    for i, item in enumerate(or_results.get('items', [])[:3], 1):
        print(f"  {i}. {item.get('title', 'No title')}")
    
    # Example 3: Complex Boolean query
    print("\n🧠 Complex query: 'machine learning -beginner (tutorial|course)'...")
    complex_query = "machine learning -beginner (tutorial|course)"
    complex_results = toolkit.search_with_boolean_query(complex_query, max_results=10)
    
    print(f"Complex query results: {len(complex_results.get('items', []))}")
    for i, item in enumerate(complex_results.get('items', [])[:3], 1):
        print(f"  {i}. {item.get('title', 'No title')}")
        print(f"     Channel: {item.get('channel_title', 'Unknown')}")
    
    # Example 4: Using BooleanSearchQuery class directly
    print("\n🔧 Using BooleanSearchQuery class directly...")
    boolean_query = BooleanSearchQuery()
    boolean_query.add_term("artificial intelligence")
    boolean_query.add_excluded_term("beginner")
    boolean_query.add_or_group(["tutorial", "course", "guide"])
    
    print(f"Built query: {boolean_query.build_query()}")
    print(f"Encoded query: {boolean_query.encode_for_api()}")


def example_pagination():
    """Example 5: Pagination Support."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Pagination Support")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # First page
    print("📄 First page of results...")
    page1_results = toolkit.search_paginated("python programming", max_results=5)
    
    print(f"Page 1: {len(page1_results.get('items', []))} results")
    print(f"Total results: {page1_results.get('total_results', 0)}")
    print(f"Next page token: {page1_results.get('next_page_token', 'None')}")
    
    for i, item in enumerate(page1_results.get('items', []), 1):
        print(f"  {i}. {item.get('title', 'No title')}")
    
    # Second page (if available)
    next_token = page1_results.get('next_page_token')
    if next_token:
        print(f"\n📄 Second page of results...")
        page2_results = toolkit.search_paginated(
            "python programming", 
            page_token=next_token, 
            max_results=5
        )
        
        print(f"Page 2: {len(page2_results.get('items', []))} results")
        for i, item in enumerate(page2_results.get('items', []), 1):
            print(f"  {i}. {item.get('title', 'No title')}")
    else:
        print("\nNo more pages available")


def example_comprehensive_filtering():
    """Example 6: Comprehensive Filtering with Multiple Criteria."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Comprehensive Filtering")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Create comprehensive filters
    filters = SearchFilters(
        type="video",
        video_duration="medium",  # 4-20 minutes
        video_definition="high",  # HD only
        video_caption="closedCaption",  # Must have captions
        video_license="creativeCommon",  # Creative Commons
        order="rating",  # Sort by rating
        published_after=datetime.now() - timedelta(days=30),  # Last 30 days
        region_code="US",  # US region
        relevance_language="en",  # English
        safe_search="strict",  # Strict safety filter
        max_results=10
    )
    
    print("🔍 Comprehensive search with multiple filters...")
    print("Filters applied:")
    print(f"  - Duration: {filters.video_duration}")
    print(f"  - Definition: {filters.video_definition}")
    print(f"  - Captions: {filters.video_caption}")
    print(f"  - License: {filters.video_license}")
    print(f"  - Order: {filters.order}")
    print(f"  - Published after: {filters.published_after}")
    print(f"  - Region: {filters.region_code}")
    print(f"  - Language: {filters.relevance_language}")
    print(f"  - Safety: {filters.safe_search}")
    
    results = toolkit.advanced_search("educational content", filters)
    
    print(f"\nResults: {len(results.get('items', []))} items found")
    print(f"Quota cost: {results.get('quota_cost', 'Unknown')} units")
    
    for i, item in enumerate(results.get('items', [])[:3], 1):
        print(f"\n{i}. {item.get('title', 'No title')}")
        print(f"   Channel: {item.get('channel_title', 'Unknown')}")
        print(f"   Published: {item.get('published_at', 'Unknown')}")
        print(f"   Description: {item.get('description', 'No description')[:100]}...")


def example_filter_validation():
    """Example 7: Filter Validation."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Filter Validation")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Test invalid filter combinations
    print("🧪 Testing filter validation...")
    
    # Invalid: eventType without video type
    invalid_filters1 = SearchFilters(
        type="channel",  # Wrong type
        event_type="live"  # Requires video type
    )
    
    errors1 = invalid_filters1.validate_filters()
    print(f"Invalid filters 1 errors: {errors1}")
    
    # Invalid: forContentOwner with video filters
    invalid_filters2 = SearchFilters(
        type="video",
        for_content_owner=True,
        video_duration="medium"  # Conflicts with forContentOwner
    )
    
    errors2 = invalid_filters2.validate_filters()
    print(f"Invalid filters 2 errors: {errors2}")
    
    # Valid filters
    valid_filters = SearchFilters(
        type="video",
        event_type="live",
        order="viewCount"
    )
    
    errors3 = valid_filters.validate_filters()
    print(f"Valid filters errors: {errors3}")


def example_quota_management():
    """Example 8: Quota Management Awareness."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Quota Management")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    print("💰 YouTube API Quota Information:")
    print("  - Search API call: 100 quota units")
    print("  - Daily quota limit: 10,000 units (default)")
    print("  - Maximum searches per day: ~100")
    
    # Perform a search and show quota cost
    results = toolkit.advanced_search("python tutorial", max_results=5)
    
    print(f"\nSearch completed:")
    print(f"  - Quota cost: {results.get('quota_cost', 'Unknown')} units")
    print(f"  - Results found: {len(results.get('items', []))}")
    print(f"  - API info: {results.get('api_info', {})}")
    
    # Show how to minimize quota usage
    print(f"\n💡 Tips to minimize quota usage:")
    print(f"  - Use specific filters to reduce API calls")
    print(f"  - Cache results when possible")
    print(f"  - Use pagination efficiently")
    print(f"  - Monitor quota usage in Google Cloud Console")


def example_content_ownership_features():
    """Example 9: Content Ownership Features (Enterprise)."""
    print("\n" + "="*70)
    print("EXAMPLE 9: Content Ownership Features")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    print("🏢 Enterprise Content Ownership Features:")
    print("  - forContentOwner: Search only content owner's videos")
    print("  - forDeveloper: Search only developer-uploaded videos")
    print("  - forMine: Search only authenticated user's videos")
    print("  - onBehalfOfContentOwner: Search on behalf of content owner")
    
    # Note: These features require proper authentication
    print(f"\n⚠️  Note: Content ownership features require:")
    print(f"  - Proper OAuth2 authentication")
    print(f"  - Content owner permissions")
    print(f"  - Developer account setup")
    
    # Example filter setup (won't work without proper auth)
    enterprise_filters = SearchFilters(
        type="video",
        for_mine=True,  # Would search user's own videos
        order="date"
    )
    
    print(f"\nExample enterprise filter setup:")
    print(f"  - forMine: {enterprise_filters.for_mine}")
    print(f"  - Type: {enterprise_filters.type}")
    print(f"  - Order: {enterprise_filters.order}")


def main():
    """Run all advanced feature examples."""
    print("YouTube Toolkit - Advanced Features Examples")
    print("=" * 70)
    
    # Check if API key is available
    if not os.getenv("YOUTUBE_API_KEY"):
        print("⚠️  Warning: YOUTUBE_API_KEY not set. Some features may not work.")
        print("   Set your API key: export YOUTUBE_API_KEY='your_api_key_here'")
        print("   Get API key from: https://console.developers.google.com/")
        print()
    
    try:
        example_event_type_filtering()
        example_category_filtering()
        example_sponsored_content_detection()
        example_boolean_search()
        example_pagination()
        example_comprehensive_filtering()
        example_filter_validation()
        example_quota_management()
        example_content_ownership_features()
        
        print("\n" + "="*70)
        print("All advanced feature examples completed successfully!")
        print("="*70)
        
        print("\n🎯 Key Features Demonstrated:")
        print("  ✅ Event type filtering (live, upcoming, completed)")
        print("  ✅ Category filtering (Gaming, Music, Education, etc.)")
        print("  ✅ Sponsored content detection")
        print("  ✅ Boolean search operators (NOT -, OR |)")
        print("  ✅ Pagination support")
        print("  ✅ Comprehensive filtering")
        print("  ✅ Filter validation")
        print("  ✅ Quota management awareness")
        print("  ✅ Content ownership features")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have:")
        print("1. Installed all dependencies: uv add google-api-python-client")
        print("2. Set your YouTube API key: export YOUTUBE_API_KEY='your_key'")
        print("3. Internet connection for API calls")


if __name__ == "__main__":
    main()
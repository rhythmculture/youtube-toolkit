"""
Advanced Comments Examples for YouTube Toolkit

This file demonstrates the enhanced comment functionality with pagination, filtering,
analytics, sentiment analysis, and comprehensive comment management.
"""

import os
from datetime import datetime, timedelta
from youtube_toolkit import YouTubeToolkit, CommentFilters, CommentResult, CommentSentimentAnalyzer


def setup_toolkit():
    """Initialize YouTube Toolkit with verbose output."""
    return YouTubeToolkit(verbose=True)


def example_basic_advanced_comments():
    """Example 1: Basic Advanced Comment Retrieval."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Advanced Comment Retrieval")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Basic advanced comment retrieval
    results = toolkit.advanced_get_comments("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    print(f"Total comments: {results.get('total_results', 0)}")
    print(f"Comments retrieved: {len(results.get('comments', []))}")
    print(f"Quota cost: {results.get('quota_cost', 0)} units")
    
    # Display analytics
    analytics = results.get('analytics', {})
    if analytics:
        print(f"\n📊 Analytics:")
        print(f"  - Total comments: {analytics.get('total_comments', 0)}")
        print(f"  - Total replies: {analytics.get('total_replies', 0)}")
        print(f"  - Total likes: {analytics.get('total_likes', 0)}")
        print(f"  - Engagement rate: {analytics.get('engagement_rate', 0):.2f}")
    
    # Display first few comments
    comments = results.get('comments', [])
    for i, comment in enumerate(comments[:3], 1):
        print(f"\n{i}. {comment.get('text', 'No text')[:100]}...")
        print(f"   Author: {comment.get('author', {}).get('display_name', 'Unknown')}")
        print(f"   Likes: {comment.get('metrics', {}).get('like_count', 0)}")
        print(f"   Replies: {comment.get('metrics', {}).get('reply_count', 0)}")


def example_comment_filtering():
    """Example 2: Comment Filtering."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Comment Filtering")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Filter for high engagement comments
    print("🔥 High engagement comments (10+ likes)...")
    high_engagement = toolkit.get_high_engagement_comments(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
        min_likes=10, 
        max_results=20
    )
    
    print(f"High engagement comments: {len(high_engagement.get('comments', []))}")
    for i, comment in enumerate(high_engagement.get('comments', [])[:3], 1):
        print(f"  {i}. {comment.get('text', '')[:80]}...")
        print(f"     Likes: {comment.get('metrics', {}).get('like_count', 0)}")
    
    # Search within comments
    print(f"\n🔍 Searching for 'great' in comments...")
    search_results = toolkit.search_comments(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        "great",
        max_results=10
    )
    
    print(f"Comments containing 'great': {len(search_results.get('comments', []))}")
    for i, comment in enumerate(search_results.get('comments', [])[:3], 1):
        print(f"  {i}. {comment.get('text', '')[:100]}...")


def example_comment_pagination():
    """Example 3: Comment Pagination."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Comment Pagination")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # First page
    print("📄 First page of comments...")
    page1 = toolkit.get_comments_paginated(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        max_results=10
    )
    
    print(f"Page 1: {len(page1.get('comments', []))} comments")
    print(f"Total results: {page1.get('total_results', 0)}")
    print(f"Next page token: {page1.get('next_page_token', 'None')}")
    
    # Second page (if available)
    next_token = page1.get('next_page_token')
    if next_token:
        print(f"\n📄 Second page of comments...")
        page2 = toolkit.get_comments_paginated(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            page_token=next_token,
            max_results=10
        )
        
        print(f"Page 2: {len(page2.get('comments', []))} comments")
        for i, comment in enumerate(page2.get('comments', [])[:3], 1):
            print(f"  {i}. {comment.get('text', '')[:80]}...")
    else:
        print("\nNo more pages available")


def example_comment_analytics():
    """Example 4: Comment Analytics and Insights."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Comment Analytics and Insights")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Get comments with analytics
    results = toolkit.advanced_get_comments(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        CommentFilters(max_results=50)
    )
    
    analytics = results.get('analytics', {})
    if analytics:
        print("📊 Comment Analytics:")
        print(f"  - Total comments: {analytics.get('total_comments', 0)}")
        print(f"  - Total replies: {analytics.get('total_replies', 0)}")
        print(f"  - Total likes: {analytics.get('total_likes', 0)}")
        print(f"  - Unique authors: {analytics.get('unique_authors', 0)}")
        print(f"  - Engagement rate: {analytics.get('engagement_rate', 0):.2f}")
        
        # Top authors
        top_authors = analytics.get('top_authors', [])
        if top_authors:
            print(f"\n👥 Top Contributors:")
            for i, author in enumerate(top_authors[:5], 1):
                print(f"  {i}. {author.get('name', 'Unknown')}: {author.get('comment_count', 0)} comments")
        
        # Most liked comments
        most_liked = analytics.get('most_liked_comments', [])
        if most_liked:
            print(f"\n👍 Most Liked Comments:")
            for i, comment in enumerate(most_liked[:3], 1):
                print(f"  {i}. {comment.get('text', '')[:60]}...")
                print(f"     Likes: {comment.get('metrics', {}).get('like_count', 0)}")


def example_sentiment_analysis():
    """Example 5: Comment Sentiment Analysis."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Comment Sentiment Analysis")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Get comments for sentiment analysis
    results = toolkit.advanced_get_comments(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        CommentFilters(max_results=30)
    )
    
    analytics = results.get('analytics', {})
    sentiment = analytics.get('sentiment_analysis', {})
    
    if sentiment:
        print("😊 Sentiment Analysis:")
        print(f"  - Positive: {sentiment.get('positive', 0):.2%}")
        print(f"  - Negative: {sentiment.get('negative', 0):.2%}")
        print(f"  - Neutral: {sentiment.get('neutral', 0):.2%}")
        
        # Determine overall sentiment
        if sentiment.get('positive', 0) > sentiment.get('negative', 0):
            overall = "😊 Positive"
        elif sentiment.get('negative', 0) > sentiment.get('positive', 0):
            overall = "😞 Negative"
        else:
            overall = "😐 Neutral"
        
        print(f"  - Overall sentiment: {overall}")
    
    # Manual sentiment analysis example
    print(f"\n🔍 Manual Sentiment Analysis:")
    comments = results.get('comments', [])
    for i, comment in enumerate(comments[:5], 1):
        text = comment.get('text', '')
        sentiment_scores = CommentSentimentAnalyzer.analyze_sentiment(text)
        sentiment_label = CommentSentimentAnalyzer.get_sentiment_label(sentiment_scores)
        
        print(f"  {i}. {text[:50]}...")
        print(f"     Sentiment: {sentiment_label} (P:{sentiment_scores['positive']:.2f}, N:{sentiment_scores['negative']:.2f})")


def example_recent_comments():
    """Example 6: Recent Comments Filtering."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Recent Comments Filtering")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Get recent comments (last 7 days)
    print("📅 Recent comments (last 7 days)...")
    recent_results = toolkit.get_recent_comments(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        days_back=7,
        max_results=20
    )
    
    print(f"Recent comments: {len(recent_results.get('comments', []))}")
    
    comments = recent_results.get('comments', [])
    for i, comment in enumerate(comments[:3], 1):
        published_at = comment.get('published_at', '')
        print(f"  {i}. {comment.get('text', '')[:60]}...")
        print(f"     Published: {published_at}")
        print(f"     Author: {comment.get('author', {}).get('display_name', 'Unknown')}")


def example_comment_export():
    """Example 7: Comment Export Functionality."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Comment Export Functionality")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Export comments to JSON
    print("📤 Exporting comments to JSON...")
    try:
        json_path = toolkit.export_comments(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            format='json',
            filters={'max_results': 20}
        )
        print(f"✅ Exported to: {json_path}")
    except Exception as e:
        print(f"❌ JSON export failed: {e}")
    
    # Export comments to CSV
    print(f"\n📤 Exporting comments to CSV...")
    try:
        csv_path = toolkit.export_comments(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            format='csv',
            filters={'max_results': 20}
        )
        print(f"✅ Exported to: {csv_path}")
    except Exception as e:
        print(f"❌ CSV export failed: {e}")


def example_comprehensive_comment_analysis():
    """Example 8: Comprehensive Comment Analysis."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Comprehensive Comment Analysis")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Create comprehensive filters
    filters = CommentFilters(
        max_results=100,
        include_replies=True,
        max_replies_per_comment=5,
        min_likes=1,  # At least 1 like
        order=CommentFilters.Order.RATING
    )
    
    print("🔍 Comprehensive comment analysis...")
    print("Filters applied:")
    print(f"  - Max results: {filters.max_results}")
    print(f"  - Include replies: {filters.include_replies}")
    print(f"  - Max replies per comment: {filters.max_replies_per_comment}")
    print(f"  - Min likes: {filters.min_likes}")
    print(f"  - Order: {filters.order.value}")
    
    results = toolkit.advanced_get_comments(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        filters
    )
    
    print(f"\n📊 Results:")
    print(f"  - Comments found: {len(results.get('comments', []))}")
    print(f"  - Total results: {results.get('total_results', 0)}")
    print(f"  - Quota cost: {results.get('quota_cost', 0)} units")
    
    # Analyze comment structure
    comments = results.get('comments', [])
    top_level_count = len([c for c in comments if c.get('parent_id') is None])
    reply_count = len([c for c in comments if c.get('parent_id') is not None])
    
    print(f"\n📝 Comment Structure:")
    print(f"  - Top-level comments: {top_level_count}")
    print(f"  - Replies: {reply_count}")
    
    # Show sample comments with replies
    comments_with_replies = [c for c in comments if c.get('replies')]
    if comments_with_replies:
        print(f"\n💬 Sample comment with replies:")
        sample = comments_with_replies[0]
        print(f"  Main: {sample.get('text', '')[:80]}...")
        print(f"  Likes: {sample.get('metrics', {}).get('like_count', 0)}")
        print(f"  Replies ({len(sample.get('replies', []))}):")
        for i, reply in enumerate(sample.get('replies', [])[:3], 1):
            print(f"    {i}. {reply.get('text', '')[:60]}...")


def example_comment_threading():
    """Example 9: Comment Threading and Reply Management."""
    print("\n" + "="*70)
    print("EXAMPLE 9: Comment Threading and Reply Management")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Get comments with replies
    results = toolkit.advanced_get_comments(
        "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        CommentFilters(
            max_results=20,
            include_replies=True,
            max_replies_per_comment=10
        )
    )
    
    comments = results.get('comments', [])
    
    print("🧵 Comment Threading Analysis:")
    print(f"  - Total comments: {len(comments)}")
    
    # Analyze threading
    threads_with_replies = 0
    total_replies = 0
    max_replies_in_thread = 0
    
    for comment in comments:
        replies = comment.get('replies', [])
        if replies:
            threads_with_replies += 1
            total_replies += len(replies)
            max_replies_in_thread = max(max_replies_in_thread, len(replies))
    
    print(f"  - Threads with replies: {threads_with_replies}")
    print(f"  - Total replies: {total_replies}")
    print(f"  - Max replies in single thread: {max_replies_in_thread}")
    
    # Show threaded conversation
    print(f"\n💬 Sample Threaded Conversation:")
    for i, comment in enumerate(comments[:2], 1):
        if comment.get('replies'):
            print(f"\n{i}. {comment.get('text', '')[:60]}...")
            print(f"   Author: {comment.get('author', {}).get('display_name', 'Unknown')}")
            print(f"   Likes: {comment.get('metrics', {}).get('like_count', 0)}")
            
            replies = comment.get('replies', [])
            print(f"   Replies ({len(replies)}):")
            for j, reply in enumerate(replies[:3], 1):
                print(f"     {j}. {reply.get('text', '')[:50]}...")
                print(f"        Author: {reply.get('author', {}).get('display_name', 'Unknown')}")
            
            if len(replies) > 3:
                print(f"     ... and {len(replies) - 3} more replies")


def main():
    """Run all advanced comment examples."""
    print("YouTube Toolkit - Advanced Comments Examples")
    print("=" * 70)
    
    # Check if API key is available
    if not os.getenv("YOUTUBE_API_KEY"):
        print("⚠️  Warning: YOUTUBE_API_KEY not set. Some features may not work.")
        print("   Set your API key: export YOUTUBE_API_KEY='your_api_key_here'")
        print("   Get API key from: https://console.developers.google.com/")
        print()
    
    try:
        example_basic_advanced_comments()
        example_comment_filtering()
        example_comment_pagination()
        example_comment_analytics()
        example_sentiment_analysis()
        example_recent_comments()
        example_comment_export()
        example_comprehensive_comment_analysis()
        example_comment_threading()
        
        print("\n" + "="*70)
        print("All advanced comment examples completed successfully!")
        print("="*70)
        
        print("\n🎯 Key Features Demonstrated:")
        print("  ✅ Advanced comment retrieval with rich metadata")
        print("  ✅ Comment filtering (engagement, search, date)")
        print("  ✅ Pagination support for large comment sections")
        print("  ✅ Comment analytics and insights")
        print("  ✅ Sentiment analysis")
        print("  ✅ Recent comments filtering")
        print("  ✅ Comment export (JSON/CSV)")
        print("  ✅ Comprehensive comment analysis")
        print("  ✅ Comment threading and reply management")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have:")
        print("1. Installed all dependencies: uv add google-api-python-client")
        print("2. Set your YouTube API key: export YOUTUBE_API_KEY='your_key'")
        print("3. Internet connection for API calls")


if __name__ == "__main__":
    main()
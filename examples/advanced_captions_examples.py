"""
Advanced Captions Examples for YouTube Toolkit

This file demonstrates the enhanced caption functionality with listing, filtering,
format conversion, analysis, search, and comprehensive caption management.
"""

import os
from datetime import datetime, timedelta
from youtube_toolkit import YouTubeToolkit, CaptionFilters, CaptionFormatConverter, CaptionAnalyzer


def setup_toolkit():
    """Initialize YouTube Toolkit with verbose output."""
    return YouTubeToolkit(verbose=True)


def example_caption_listing():
    """Example 1: Caption Listing and Filtering."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Caption Listing and Filtering")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # List all available captions
    print("📋 Listing all available captions...")
    caption_list = toolkit.list_captions("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    print(f"Total tracks: {caption_list.get('analytics', {}).get('total_tracks', 0)}")
    print(f"Available tracks: {caption_list.get('analytics', {}).get('available_tracks', 0)}")
    print(f"Quota cost: {caption_list.get('quota_cost', 0)} units")
    
    # Display caption tracks
    tracks = caption_list.get('tracks', [])
    for i, track in enumerate(tracks[:5], 1):
        print(f"\n{i}. {track.get('display_name', 'Unknown')}")
        print(f"   Language: {track.get('language_code', 'Unknown')}")
        print(f"   Type: {track.get('track_type', 'Unknown')}")
        print(f"   Status: {track.get('status', 'Unknown')}")
        print(f"   Auto-generated: {track.get('is_auto_generated', False)}")
        print(f"   CC: {track.get('is_cc', False)}")
    
    # Filter for manual captions only
    print(f"\n🔍 Filtering for manual captions only...")
    manual_filters = CaptionFilters(manual_only=True)
    manual_list = toolkit.list_captions("https://www.youtube.com/watch?v=dQw4w9WgXcQ", manual_filters)
    
    print(f"Manual tracks: {len(manual_list.get('tracks', []))}")
    
    # Filter for specific languages
    print(f"\n🌍 Filtering for English and Spanish...")
    language_filters = CaptionFilters(language_codes=['en', 'es'])
    language_list = toolkit.list_captions("https://www.youtube.com/watch?v=dQw4w9WgXcQ", language_filters)
    
    print(f"English/Spanish tracks: {len(language_list.get('tracks', []))}")


def example_caption_download():
    """Example 2: Advanced Caption Download."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Advanced Caption Download")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Download in different formats
    formats = ['srt', 'vtt', 'txt']
    
    for format_type in formats:
        print(f"\n📥 Downloading captions in {format_type.upper()} format...")
        try:
            result = toolkit.advanced_download_captions(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                language_code='en',
                format=format_type
            )
            
            if result.get('success'):
                print(f"✅ Downloaded: {result['output_path']}")
                print(f"   Caption ID: {result['caption_id']}")
                print(f"   Language: {result['language_code']}")
                print(f"   Format: {result['format']}")
                
                # Show analysis
                analysis = result.get('analysis', {})
                print(f"   Duration: {analysis.get('total_duration', 0):.1f} seconds")
                print(f"   Word count: {analysis.get('word_count', 0)}")
                print(f"   Cue count: {analysis.get('cue_count', 0)}")
                print(f"   Words per minute: {analysis.get('words_per_minute', 0):.1f}")
            else:
                print(f"❌ Failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error downloading {format_type}: {e}")


def example_caption_analysis():
    """Example 3: Caption Analysis and Insights."""
    print("\n" + "="*70)
    print("EXAMPLE 3: Caption Analysis and Insights")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Get caption analytics
    print("📊 Getting caption analytics...")
    try:
        analytics = toolkit.get_caption_analytics("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        
        print(f"Total duration: {analytics.get('total_duration', 0):.1f} seconds")
        print(f"Word count: {analytics.get('word_count', 0)}")
        print(f"Cue count: {analytics.get('cue_count', 0)}")
        print(f"Average cue duration: {analytics.get('average_cue_duration', 0):.1f} seconds")
        print(f"Words per minute: {analytics.get('words_per_minute', 0):.1f}")
        
        # Language analysis
        language_analysis = analytics.get('language_analysis', {})
        if language_analysis:
            print(f"\n🌍 Language Analysis:")
            print(f"   Detected language: {language_analysis.get('detected_language', 'Unknown')}")
            print(f"   Confidence: {language_analysis.get('confidence', 0):.2%}")
        
        # Gap analysis
        gaps = analytics.get('gaps', [])
        if gaps:
            print(f"\n⏱️  Timing Gaps:")
            print(f"   Total gaps: {len(gaps)}")
            if gaps:
                avg_gap = sum(gap['duration'] for gap in gaps) / len(gaps)
                print(f"   Average gap: {avg_gap:.1f} seconds")
                print(f"   Longest gap: {max(gap['duration'] for gap in gaps):.1f} seconds")
        
    except Exception as e:
        print(f"❌ Analytics failed: {e}")


def example_caption_search():
    """Example 4: Caption Content Search."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Caption Content Search")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Search for specific terms
    search_terms = ["never", "gonna", "give", "up"]
    
    for term in search_terms:
        print(f"\n🔍 Searching for '{term}' in captions...")
        try:
            matches = toolkit.search_captions(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                term,
                language_code='en'
            )
            
            print(f"Found {len(matches)} matches:")
            for i, match in enumerate(matches[:3], 1):
                print(f"  {i}. [{match['formatted_start']} - {match['formatted_end']}]")
                print(f"     {match['text']}")
            
            if len(matches) > 3:
                print(f"     ... and {len(matches) - 3} more matches")
                
        except Exception as e:
            print(f"❌ Search failed: {e}")


def example_caption_format_conversion():
    """Example 5: Caption Format Conversion."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Caption Format Conversion")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Download SRT format
    print("📥 Downloading SRT captions...")
    try:
        srt_result = toolkit.advanced_download_captions(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            language_code='en',
            format='srt'
        )
        
        if srt_result.get('success'):
            print(f"✅ SRT downloaded: {srt_result['output_path']}")
            
            # Read SRT content
            with open(srt_result['output_path'], 'r', encoding='utf-8') as f:
                srt_content = f.read()
            
            # Convert to different formats
            print(f"\n🔄 Converting formats...")
            
            # Convert to VTT
            vtt_content = CaptionFormatConverter.srt_to_vtt(srt_content)
            print(f"✅ Converted to WebVTT format ({len(vtt_content)} characters)")
            
            # Convert to plain text
            txt_content = CaptionFormatConverter.srt_to_txt(srt_content)
            print(f"✅ Converted to plain text ({len(txt_content)} characters)")
            
            # Parse SRT into cues
            cues = CaptionFormatConverter.parse_srt(srt_content)
            print(f"✅ Parsed into {len(cues)} caption cues")
            
            # Show sample cues
            print(f"\n📝 Sample caption cues:")
            for i, cue in enumerate(cues[:3], 1):
                print(f"  {i}. [{cue.formatted_start} - {cue.formatted_end}]")
                print(f"     {cue.text}")
                print(f"     Duration: {cue.duration:.1f}s")
        
    except Exception as e:
        print(f"❌ Format conversion failed: {e}")


def example_caption_export():
    """Example 6: Caption Export Functionality."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Caption Export Functionality")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Export in different formats
    export_formats = ['json', 'csv', 'vtt', 'txt']
    
    for format_type in export_formats:
        print(f"\n📤 Exporting captions as {format_type.upper()}...")
        try:
            export_path = toolkit.export_captions(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                format=format_type,
                language_code='en'
            )
            
            print(f"✅ Exported to: {export_path}")
            
            # Show file size
            file_size = os.path.getsize(export_path)
            print(f"   File size: {file_size} bytes")
            
            # Show sample content for text formats
            if format_type in ['vtt', 'txt']:
                with open(export_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"   Sample content: {content[:100]}...")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")


def example_best_caption_track():
    """Example 7: Best Caption Track Selection."""
    print("\n" + "="*70)
    print("EXAMPLE 7: Best Caption Track Selection")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Get best caption track
    print("🎯 Finding best caption track...")
    try:
        best_track = toolkit.get_best_caption_track(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            preferred_language='en'
        )
        
        if best_track:
            print(f"✅ Best track found:")
            print(f"   Caption ID: {best_track['caption_id']}")
            print(f"   Language: {best_track['language']} ({best_track['language_code']})")
            print(f"   Name: {best_track['name']}")
            print(f"   Type: {best_track['track_type']}")
            print(f"   Status: {best_track['status']}")
            print(f"   Auto-generated: {best_track['is_auto_generated']}")
            print(f"   CC: {best_track['is_cc']}")
            print(f"   Display name: {best_track['display_name']}")
        else:
            print("❌ No suitable caption track found")
    
    except Exception as e:
        print(f"❌ Best track selection failed: {e}")


def example_caption_analytics_deep_dive():
    """Example 8: Deep Dive Caption Analytics."""
    print("\n" + "="*70)
    print("EXAMPLE 8: Deep Dive Caption Analytics")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Get comprehensive analytics
    print("📊 Comprehensive caption analytics...")
    try:
        result = toolkit.advanced_download_captions(
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            language_code='en',
            format='srt'
        )
        
        if result.get('success'):
            analysis = result['analysis']
            content = result['content']
            
            print(f"\n📈 Basic Statistics:")
            print(f"   Total duration: {analysis['total_duration']:.1f} seconds")
            print(f"   Word count: {analysis['word_count']}")
            print(f"   Cue count: {analysis['cue_count']}")
            print(f"   Average cue duration: {analysis['average_cue_duration']:.1f} seconds")
            print(f"   Words per minute: {analysis['words_per_minute']:.1f}")
            
            # Reading speed analysis
            reading_speed = CaptionAnalyzer.analyze_reading_speed(content.cues)
            print(f"\n📖 Reading Speed Analysis:")
            print(f"   Average WPM: {reading_speed['average_wpm']:.1f}")
            print(f"   Average cue duration: {reading_speed['average_cue_duration']:.1f}s")
            print(f"   Total words: {reading_speed['total_words']}")
            print(f"   Total duration: {reading_speed['total_duration']:.1f}s")
            
            # Gap analysis
            gaps = CaptionAnalyzer.find_gaps(content.cues)
            print(f"\n⏱️  Gap Analysis:")
            print(f"   Total gaps: {len(gaps)}")
            if gaps:
                gap_durations = [gap['duration'] for gap in gaps]
                print(f"   Average gap: {sum(gap_durations) / len(gap_durations):.1f}s")
                print(f"   Shortest gap: {min(gap_durations):.1f}s")
                print(f"   Longest gap: {max(gap_durations):.1f}s")
            
            # Language analysis
            language_analysis = CaptionAnalyzer.analyze_language(content.raw_content)
            print(f"\n🌍 Language Analysis:")
            print(f"   Detected language: {language_analysis['detected_language']}")
            print(f"   Confidence: {language_analysis['confidence']:.2%}")
            print(f"   Word counts by language: {language_analysis['word_counts']}")
            
            # Cue distribution analysis
            cue_durations = [cue.duration for cue in content.cues]
            print(f"\n📊 Cue Distribution:")
            print(f"   Shortest cue: {min(cue_durations):.1f}s")
            print(f"   Longest cue: {max(cue_durations):.1f}s")
            print(f"   Median duration: {sorted(cue_durations)[len(cue_durations)//2]:.1f}s")
            
            # Word frequency analysis
            all_text = ' '.join([cue.text for cue in content.cues]).lower()
            words = all_text.split()
            word_freq = {}
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1
            
            # Top 10 most common words
            top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
            print(f"\n🔤 Top 10 Most Common Words:")
            for i, (word, count) in enumerate(top_words, 1):
                print(f"   {i}. '{word}': {count} times")
        
    except Exception as e:
        print(f"❌ Deep dive analytics failed: {e}")


def example_caption_filtering_advanced():
    """Example 9: Advanced Caption Filtering."""
    print("\n" + "="*70)
    print("EXAMPLE 9: Advanced Caption Filtering")
    print("="*70)
    
    toolkit = setup_toolkit()
    
    # Test different filter combinations
    filter_tests = [
        {
            'name': 'Auto-generated only',
            'filters': CaptionFilters(auto_generated_only=True)
        },
        {
            'name': 'Manual captions only',
            'filters': CaptionFilters(manual_only=True)
        },
        {
            'name': 'CC captions only',
            'filters': CaptionFilters(cc_only=True)
        },
        {
            'name': 'Accessible captions only',
            'filters': CaptionFilters(accessible_only=True)
        },
        {
            'name': 'English and Spanish',
            'filters': CaptionFilters(language_codes=['en', 'es'])
        }
    ]
    
    for test in filter_tests:
        print(f"\n🔍 Testing: {test['name']}")
        try:
            result = toolkit.list_captions(
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                test['filters']
            )
            
            tracks = result.get('tracks', [])
            print(f"   Found {len(tracks)} tracks")
            
            for track in tracks[:2]:  # Show first 2 tracks
                print(f"   - {track.get('display_name', 'Unknown')} ({track.get('language_code', 'Unknown')})")
                print(f"     Type: {track.get('track_type', 'Unknown')}, Status: {track.get('status', 'Unknown')}")
        
        except Exception as e:
            print(f"   ❌ Filter test failed: {e}")


def main():
    """Run all advanced caption examples."""
    print("YouTube Toolkit - Advanced Captions Examples")
    print("=" * 70)
    
    # Check if API key is available
    if not os.getenv("YOUTUBE_API_KEY"):
        print("⚠️  Warning: YOUTUBE_API_KEY not set. Some features may not work.")
        print("   Set your API key: export YOUTUBE_API_KEY='your_api_key_here'")
        print("   Get API key from: https://console.developers.google.com/")
        print()
    
    try:
        example_caption_listing()
        example_caption_download()
        example_caption_analysis()
        example_caption_search()
        example_caption_format_conversion()
        example_caption_export()
        example_best_caption_track()
        example_caption_analytics_deep_dive()
        example_caption_filtering_advanced()
        
        print("\n" + "="*70)
        print("All advanced caption examples completed successfully!")
        print("="*70)
        
        print("\n🎯 Key Features Demonstrated:")
        print("  ✅ Caption listing and filtering")
        print("  ✅ Advanced caption download with format conversion")
        print("  ✅ Caption analytics and insights")
        print("  ✅ Caption content search")
        print("  ✅ Format conversion (SRT, VTT, TXT)")
        print("  ✅ Caption export (JSON, CSV, formats)")
        print("  ✅ Best caption track selection")
        print("  ✅ Deep dive analytics")
        print("  ✅ Advanced filtering options")
        
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("Make sure you have:")
        print("1. Installed all dependencies: uv add google-api-python-client")
        print("2. Set your YouTube API key: export YOUTUBE_API_KEY='your_key'")
        print("3. Internet connection for API calls")


if __name__ == "__main__":
    main()
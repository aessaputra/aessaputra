"""
GitHub README Content Updater

This script fetches the latest blog posts and notes from Atom feeds
and combines them into a single list for the README.md file.

Sorted by date (newest first).
"""

import feedparser
import datetime
from typing import List, Optional
from operator import itemgetter

# Feed Configuration
POSTS_FEED_URL = "https://aessaputra.net/posts-feed.xml"
NOTES_FEED_URL = "https://aessaputra.net/notes-feed.xml"

# Output Configuration
NUM_ENTRIES = 5  # Total number of entries to show (combined)
README_FILE = "README.md"

# Markers (using existing markers)
START_MARKER = "<!-- LATEST-WRITES:START -->"
END_MARKER = "<!-- LATEST-WRITES:END -->"


def parse_date(entry) -> tuple:
    """
    Parse date from feed entry, returning both formatted string and datetime for sorting.
    Atom feeds may have 'published' or 'updated' or both.
    
    Returns:
        Tuple of (date_string, datetime_object)
    """
    try:
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            dt = datetime.datetime(*entry.published_parsed[:6])
        elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
            dt = datetime.datetime(*entry.updated_parsed[:6])
        else:
            return ('N/A', datetime.datetime.min)
        
        return (dt.strftime('%Y-%m-%d'), dt)
    except (TypeError, ValueError):
        return ('N/A', datetime.datetime.min)


def fetch_feed_entries(feed_url: str, source_type: str = "post") -> List[dict]:
    """
    Fetch all entries from an Atom feed.
    
    Args:
        feed_url: URL of the Atom feed
        source_type: Type of source ('post' or 'note') for display
        
    Returns:
        List of entry dictionaries with title, link, date, datetime, and type
    """
    try:
        feed = feedparser.parse(feed_url)
        
        if feed.bozo and feed.bozo_exception:
            print(f"Warning: Feed parsing issue for {source_type} - {feed.bozo_exception}")
        
        entries = []
        for entry in feed.entries:
            date_str, date_obj = parse_date(entry)
            entries.append({
                'title': entry.get('title', 'Untitled'),
                'link': entry.get('link', '#'),
                'date': date_str,
                'datetime': date_obj,
                'type': source_type
            })
        
        return entries
    
    except Exception as e:
        print(f"Error fetching {source_type} feed from {feed_url}: {e}")
        return []


def fetch_combined_entries(limit: int = 5) -> List[dict]:
    """
    Fetch entries from both posts and notes feeds, combine and sort by date.
    
    Args:
        limit: Maximum number of entries to return
        
    Returns:
        Combined list of entries sorted by date (newest first)
    """
    # Fetch from both feeds
    posts = fetch_feed_entries(POSTS_FEED_URL, "post")
    notes = fetch_feed_entries(NOTES_FEED_URL, "note")
    
    print(f"Fetched {len(posts)} posts and {len(notes)} notes")
    
    # Combine all entries
    all_entries = posts + notes
    
    # Sort by datetime (newest first)
    all_entries.sort(key=itemgetter('datetime'), reverse=True)
    
    # Return limited entries
    return all_entries[:limit]


def format_entries_as_markdown(entries: List[dict], show_type: bool = False) -> str:
    """
    Format feed entries as markdown list items.
    
    Args:
        entries: List of entry dictionaries
        show_type: If True, show entry type (Post/Note) prefix
        
    Returns:
        Markdown formatted string
    """
    lines = []
    for entry in entries:
        if show_type:
            type_emoji = "📝" if entry['type'] == "post" else "📒"
            lines.append(f"- {type_emoji} [{entry['title']}]({entry['link']}) - {entry['date']}")
        else:
            lines.append(f"- [{entry['title']}]({entry['link']}) - {entry['date']}")
    return "\n".join(lines)


def update_readme_section(
    content: str,
    start_marker: str,
    end_marker: str,
    new_content: str
) -> Optional[str]:
    """
    Update a section of the README between markers.
    
    Args:
        content: Current README content
        start_marker: Start marker string
        end_marker: End marker string
        new_content: New content to insert
        
    Returns:
        Updated content or None if markers not found
    """
    start_index = content.find(start_marker)
    end_index = content.find(end_marker)
    
    if start_index == -1 or end_index == -1:
        print(f"Markers not found: '{start_marker}' or '{end_marker}'")
        return None
    
    start_index += len(start_marker)
    
    return (
        content[:start_index] + 
        "\n" + new_content + "\n" + 
        content[end_index:]
    )


def update_readme():
    """Update README with combined latest posts and notes."""
    print("Fetching combined entries from posts and notes feeds...")
    
    entries = fetch_combined_entries(NUM_ENTRIES)
    
    if not entries:
        print("No entries found from any feed, skipping update.")
        return False
    
    # Format with type indicators (emoji)
    markdown_content = format_entries_as_markdown(entries, show_type=True)
    
    print(f"\nCombined entries to add:\n{markdown_content}\n")
    
    try:
        with open(README_FILE, "r", encoding="utf-8") as file:
            readme_content = file.read()
        
        updated_content = update_readme_section(
            readme_content,
            START_MARKER,
            END_MARKER,
            markdown_content
        )
        
        if updated_content is None:
            print(f"Markers not found in {README_FILE}")
            return False
        
        with open(README_FILE, "w", encoding="utf-8") as file:
            file.write(updated_content)
        
        print(f"Successfully updated README with {len(entries)} entries")
        return True
        
    except FileNotFoundError:
        print(f"README file not found: {README_FILE}")
        return False
    except Exception as e:
        print(f"Error updating README: {e}")
        return False


def main():
    """Main function to update README with latest combined content."""
    print("=" * 50)
    print("GitHub README Content Updater")
    print("=" * 50)
    
    success = update_readme()
    
    if success:
        print("\n✅ README update completed successfully!")
    else:
        print("\n❌ README update failed or no changes made.")
    
    return 0 if success else 1


if __name__ == "__main__":
    exit(main())
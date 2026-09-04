"""Update the README with the latest entries from aessaputra.net."""

import datetime
from pathlib import Path

import feedparser

FEED_URL = "https://aessaputra.net/feed.xml"
README_FILE = Path("README.md")
START_MARKER = "<!-- LATEST-WRITES:START -->"
END_MARKER = "<!-- LATEST-WRITES:END -->"
NUM_ENTRIES = 5


def parse_date(entry):
    try:
        parsed = entry.get("published_parsed") or entry.get("updated_parsed")
        date = datetime.datetime(*parsed[:6])
        return date.strftime("%Y-%m-%d"), date
    except (TypeError, ValueError):
        return "N/A", datetime.datetime.min


def fetch_entries():
    feed = feedparser.parse(FEED_URL)
    if feed.bozo and feed.bozo_exception:
        print(f"Warning: feed parsing issue: {feed.bozo_exception}")

    entries = []
    for entry in feed.entries:
        date, sort_date = parse_date(entry)
        entries.append({
            "title": entry.get("title", "Untitled"),
            "link": entry.get("link", "#"),
            "date": date,
            "sort_date": sort_date,
        })
    return sorted(entries, key=lambda entry: entry["sort_date"], reverse=True)[:NUM_ENTRIES]


def update_readme():
    entries = fetch_entries()
    if not entries:
        print("No feed entries found; README unchanged.")
        return False

    markdown = "\n".join(
        f'- 📝 [{entry["title"]}]({entry["link"]}) - {entry["date"]}'
        for entry in entries
    )

    try:
        content = README_FILE.read_text(encoding="utf-8")
    except OSError as error:
        print(f"Error reading {README_FILE}: {error}")
        return False

    start = content.find(START_MARKER)
    end = content.find(END_MARKER, start + len(START_MARKER))
    if start == -1 or end == -1:
        print(f"Markers not found in {README_FILE}")
        return False

    start += len(START_MARKER)
    updated = f"{content[:start]}\n{markdown}\n{content[end:]}"
    try:
        README_FILE.write_text(updated, encoding="utf-8")
    except OSError as error:
        print(f"Error writing {README_FILE}: {error}")
        return False

    print(f"Updated {README_FILE} with {len(entries)} entries.")
    return True


if __name__ == "__main__":
    raise SystemExit(0 if update_readme() else 1)

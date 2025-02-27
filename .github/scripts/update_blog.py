import feedparser
import datetime

# Constants
RSS_FEED_URL = "https://aessaputra.net/feed"
NUM_POSTS = 5
README_FILE = "README.md"
START_MARKER = "<!-- BLOG-POST-LIST:START -->"
END_MARKER = "<!-- BLOG-POST-LIST:END -->"

def fetch_latest_blog_posts():
    """Fetch the latest blog posts from the RSS feed."""
    feed = feedparser.parse(RSS_FEED_URL)
    posts = []
    for entry in feed.entries[:NUM_POSTS]:
        published_date = datetime.datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
        posts.append(f"- [{entry.title}]({entry.link}) - {published_date}")
    return "\n".join(posts)

def update_readme_with_posts(blog_posts):
    """Update the README file with the latest blog posts."""
    with open(README_FILE, "r") as file:
        readme_content = file.read()

    start_index = readme_content.find(START_MARKER) + len(START_MARKER)
    end_index = readme_content.find(END_MARKER)

    updated_readme = (
        readme_content[:start_index] + "\n" + blog_posts + "\n" + readme_content[end_index:]
    )

    with open(README_FILE, "w") as file:
        file.write(updated_readme)

def main():
    """Main function to fetch blog posts and update the README."""
    blog_posts = fetch_latest_blog_posts()
    update_readme_with_posts(blog_posts)

if __name__ == "__main__":
    main()
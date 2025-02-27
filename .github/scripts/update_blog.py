import feedparser
import datetime

# URL RSS feed Anda
RSS_FEED_URL = "https://aessaputra.net/feed"

# Fungsi untuk mengambil entri terbaru dari RSS feed
def get_latest_blog_posts():
    feed = feedparser.parse(RSS_FEED_URL)
    posts = []
    for entry in feed.entries[:5]:  # Ambil 5 posting terbaru
        published_date = datetime.datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
        posts.append(f"- [{entry.title}]({entry.link}) - {published_date}")
    return "\n".join(posts)

# Fungsi untuk memperbarui README.md
def update_readme(blog_posts):
    with open("README.md", "r") as file:
        readme = file.read()

    # Temukan bagian di README.md di mana Anda ingin menambahkan posting blog
    start_marker = "<!-- BLOG-POST-LIST:START -->"
    end_marker = "<!-- BLOG-POST-LIST:END -->"
    start_index = readme.find(start_marker) + len(start_marker)
    end_index = readme.find(end_marker)

    # Perbarui bagian tersebut dengan posting blog terbaru
    updated_readme = readme[:start_index] + "\n" + blog_posts + "\n" + readme[end_index:]

    with open("README.md", "w") as file:
        file.write(updated_readme)

if __name__ == "__main__":
    blog_posts = get_latest_blog_posts()
    update_readme(blog_posts)
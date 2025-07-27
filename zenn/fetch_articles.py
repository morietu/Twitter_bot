# 自分の投稿記事一覧
# zenn/fetch_articles.py

import feedparser
from datetime import datetime
import os

ZENN_USERNAME = "ej33"  # ← ご自身のZennユーザー名に変更
FEED_URL = f"https://zenn.dev/{ZENN_USERNAME}/feed"
OUTPUT_DIR = "zenn"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "zenn_articles.md")

def fetch_zenn_articles():
    feed = feedparser.parse(FEED_URL)
    articles = []

    for entry in feed.entries:
        title = entry.title
        url = entry.link
        published = entry.published
        published_date = datetime.strptime(published, "%a, %d %b %Y %H:%M:%S %Z").date()
        articles.append({
            "title": title,
            "url": url,
            "date": published_date
        })

    return articles

def save_articles_to_markdown(articles):
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 📝 {ZENN_USERNAME} のZenn記事一覧（{datetime.now().date()} 時点）\n\n")
        for article in articles:
            f.write(f"- [{article['title']}]({article['url']})（{article['date']}）\n")

    print(f"[✅] {len(articles)}件の記事を {OUTPUT_FILE} に保存しました。")

if __name__ == "__main__":
    articles = fetch_zenn_articles()
    save_articles_to_markdown(articles)

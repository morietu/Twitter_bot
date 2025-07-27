# zenn/weekly_report.py

import feedparser
from datetime import datetime, timedelta
import os

ZENN_USERNAME = "ej33"
FEED_URL = f"https://zenn.dev/{ZENN_USERNAME}/feed"
OUTPUT_DIR = "zenn"

def fetch_weekly_articles():
    feed = feedparser.parse(FEED_URL)
    today = datetime.now().date()
    monday = today - timedelta(days=today.weekday())  # 今週の月曜日
    sunday = monday + timedelta(days=6)

    articles = []
    for entry in feed.entries:
        pub_date = datetime.strptime(entry.published, "%a, %d %b %Y %H:%M:%S %Z").date()
        if monday <= pub_date <= sunday:
            articles.append({
                "title": entry.title,
                "url": entry.link,
                "date": pub_date
            })
    return articles, monday

def save_weekly_markdown(articles, monday_date):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"weekly_report_{monday_date.strftime('%Y%m%d')}.md"
    path = os.path.join(OUTPUT_DIR, filename)

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# ✨今週のZennアウトプットまとめ（{monday_date}〜）\n\n")
        if not articles:
            f.write("今週の投稿はありませんでした。\n")
        else:
            for art in articles:
                f.write(f"- [{art['title']}]({art['url']})（{art['date']}）\n")

    print(f"[✅] {len(articles)}件を {path} に保存しました。")

if __name__ == "__main__":
    articles, monday = fetch_weekly_articles()
    save_weekly_markdown(articles, monday)

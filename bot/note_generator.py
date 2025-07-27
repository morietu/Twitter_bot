# note用の日本語文章を出力
from datetime import datetime

summary = "ここに週次まとめ内容を入れる"

filename = f"articles/{datetime.today().strftime('%Y-%m-%d')}-weekly-summary.md"
with open(filename, "w", encoding="utf-8") as f:
    f.write(f"""---
title: "Twitter週次まとめ ({datetime.today().strftime('%Y/%m/%d')})"
emoji: "📝"
type: "article"
topics: ["Twitter", "自動化", "Python"]
published: false
---

{summary}
""")




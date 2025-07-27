import os
from datetime import date

BASE_DIR = "generated/tweets/season_01"
OUTPUT_DIR = "zenn/articles"
os.makedirs(OUTPUT_DIR, exist_ok=True)

today = date.today().strftime("%Y%m%d")
output_path = os.path.join(OUTPUT_DIR, f"weekly_report_{today}.md")

files = sorted([
    f for f in os.listdir(BASE_DIR)
    if f.endswith(".txt") and not f.startswith("counter")
])[:7]

with open(output_path, "w", encoding="utf-8") as out:
    out.write(f"# 今週の筋トレ投稿まとめ（{today}）\n\n")
    for filename in files:
        with open(os.path.join(BASE_DIR, filename), encoding="utf-8") as f:
            out.write(f"## {filename.replace('.txt','')}\n")
            out.write(f.read())
            out.write("\n\n---\n\n")

print(f"[✅] Zenn用週報を作成しました → {output_path}")

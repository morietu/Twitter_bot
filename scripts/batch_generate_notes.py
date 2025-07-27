# scripts/batch_generate_notes.py
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

import os
from dotenv import load_dotenv
from openai import OpenAI
from datetime import datetime
from utils.google_sheet_logger import log_to_sheet

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

tweet_dir = Path("generated/tweets/season_01")
note_dir = Path("note_articles")
note_dir.mkdir(parents=True, exist_ok=True)

log_entries = []

def generate_detailed_note_from_text(episode_id: str, tweet_text: str) -> str:
    prompt = f"""
以下は、筋トレ初心者の女性（20代〜40代）に向けた、Twitter投稿の内容をもとにしたnote記事の本文です。
以下のツイートを元に、わかりやすく専門家風に詳しく解説してください。

【ツイート内容】
{tweet_text}

【note記事の条件】
- ターゲットは筋トレ初心者の女性
- 専門用語は避け、丁寧でやさしい語り口
- 各メニューの説明、やり方、効果、注意点を記載
- Markdown形式で800〜1200文字以内
- 文末にはやさしい励ましを入れる
"""
    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        content = res.choices[0].message.content.strip()
    except Exception as e:
        content = f"[ERROR] GPT生成に失敗: {e}"

    filepath = note_dir / f"{episode_id}_detailed.md"
    filepath.write_text(content, encoding="utf-8")
    return str(filepath)

for file in sorted(tweet_dir.glob("S*.txt")):
    episode_id = file.stem
    tweet_text = file.read_text(encoding="utf-8")
    saved_path = generate_detailed_note_from_text(episode_id, tweet_text)

    today = datetime.now().strftime("%Y/%m/%d")
    url = f"https://note.com/famous_walrus484/n/{episode_id.lower()}"
    log_entries.append([today, "一括変換", episode_id, tweet_text.splitlines()[0], url])

# Googleシートに一括送信
for row in log_entries:
    log_to_sheet(*row)

print(f"[✅] {len(log_entries)}件のnote原稿を生成し、ログを送信しました。")

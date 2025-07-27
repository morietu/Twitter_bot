# zenn記事
import os
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_weekly_summary() -> str:
    """GPTでZenn用の週次サマリーテキストを自動生成"""
    prompt = """
以下は、Twitterの筋トレBotアカウントの活動記録を週次でまとめる技術記事の本文です。
以下の条件でGPTが要約してください。

【条件】
- 読者は技術に詳しくない一般ユーザー（Zenn読者）
- Botの動作概要（GPTで自動生成、定時投稿、人気分析など）を紹介
- 一週間の投稿数・反響・ハイライト（例：人気ツイート）などに触れる
- noteへの導線があるなら、それにも触れる
- 文字数は800字以内で自然にまとめる
"""

    try:
        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] GPT要約失敗: {e}")
        return "今週の活動記録をうまく取得できませんでした。"

def generate_zenn_weekly_article(message: str):
    """Zenn記事のマークダウンを出力"""
    today = datetime.today().strftime('%Y-%m-%d')
    filename = f"articles/{today}-weekly-summary.md"
    os.makedirs("articles", exist_ok=True)

    summary = generate_weekly_summary()  # ← GPTで生成

    content = f"""---
    title: "Twitter週次まとめ ({datetime.today().strftime('%Y/%m/%d')})"
    emoji: "📝"
    type: "article"
    topics: ["Twitter", "自動化", "Python"]
    published: false
    ---

    {summary}
    """

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[✅] Zenn記事を保存しました: {filename}")
    return filename

# bot/note_writer.py

import os
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_detailed_note(episode_id: str, tweet_text: str) -> str:
    """
    GPTを使ってnote向けの専門家風記事を生成し、保存する。

    Parameters:
        episode_id (str): ツイートのID（例: S01-002）
        tweet_text (str): 元となる投稿文

    Returns:
        str: 保存されたファイルパス
    """
    prompt = """
以下は、筋トレ初心者の女性（20代〜40代）に向けた、Twitter投稿の内容をもとにしたnote記事の本文です。
以下のツイートを元に、わかりやすく専門家風に詳しく解説してください。

【ツイート内容】
{tweet}

【note記事の条件】
- ターゲットは筋トレ初心者の女性
- 専門用語は避け、丁寧でやさしい語り口
- 各メニューの説明、やり方、効果、注意点を記載
- Markdown形式で800〜1200文字以内
- 文末にはやさしい励ましを入れる
""".format(tweet=tweet_text)

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        article = response.choices[0].message.content.strip()
    except Exception as e:
        article = f"[ERROR] GPT生成に失敗しました: {e}"
        print(article)
        return ""

    save_path = Path(f"note_articles/{episode_id}_detailed.md")
    save_path.parent.mkdir(parents=True, exist_ok=True)
    save_path.write_text(article, encoding="utf-8")

    print(f"[✅] note記事を保存しました: {save_path}")
    return str(save_path)

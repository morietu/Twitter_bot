import os
import logging
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ログ設定（まだなら）
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/success_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)

# 設定
MAX_LENGTH = 260
NOTE_URL = "https://note.com/famous_walrus484"
POST_SUFFIX = f"\n\n▼noteで詳しく読む👇\n{NOTE_URL}"

# シーズンと通番管理
SEASON_NUMBER = 1
BASE_DIR = f"generated/tweets/season_{SEASON_NUMBER:02d}"
COUNTER_FILE = os.path.join(BASE_DIR, "counter.txt")

def get_next_episode_number():
    os.makedirs(BASE_DIR, exist_ok=True)
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f:
            f.write("1")
        return 1
    with open(COUNTER_FILE, "r") as f:
        return int(f.read().strip())

def increment_episode_number(n):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(n + 1))



def generate_tweet_with_number(episode_id: str, time_of_day: str) -> str:
    # 時間帯ごとにターゲット部位を切り替え
    if time_of_day == "朝":
        target = "脚（下半身）"
        examples = "スクワット、ランジ、グルートブリッジなど"
    elif time_of_day == "昼":
        target = "上半身（肩・腕・背中）"
        examples = "膝つき腕立て伏せ、ペットボトルショルダープレス、ベントオーバーなど"
    elif time_of_day == "夜":
        target = "体幹（腹筋・背筋・姿勢）"
        examples = "プランク、バードドッグ、クランチなど"
    else:
        target = "全身"
        examples = "スクワット、腕立て伏せ、プランクなど"

    prompt = f"""
あなたはSNS投稿用のNASM認定パーソナルトレーナーです。
20〜40代の筋トレ初心者女性向けに、自宅でできる「{target}」を鍛えるメニューを3種紹介してください。

【条件】
- {examples} のような器具不要の種目で構成
- 絵文字OK、やさしい表現で初心者向け
- あいさつや時間帯の記述は不要
- 全角260文字以内（noteリンク込み）
- 出力文の先頭に「【{episode_id}】」を入れてください
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )

    body = res.choices[0].message.content.strip()
    total_text = body + POST_SUFFIX

    if len(total_text) > MAX_LENGTH:
        allowed = MAX_LENGTH - len(POST_SUFFIX)
        trimmed = body[:allowed].rstrip("。！!、,.…") + "…"
        final_text = trimmed + POST_SUFFIX
    else:
        final_text = total_text

    # 保存とログ
    filename = os.path.join(BASE_DIR, f"{episode_id}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(final_text)

    logging.info(f"[✅ {time_of_day}の投稿生成成功]\n{final_text}\n")
    print(f"[✅] {time_of_day}メニュー → {filename}")
    print("\n────────────\n" + final_text)
    return final_text




def post_gpt_tweet(time_of_day="任意"):
    episode_number = get_next_episode_number()
    episode_id = f"S{SEASON_NUMBER:02d}-{episode_number:03d}"
    text = generate_tweet_with_number(episode_id, time_of_day)
    increment_episode_number(episode_number)
    print(f"[🚀] 投稿処理（{time_of_day}）\n{text}")
    return text

def post_popular_tweet():
    logging.info("[🔥 人気ツイート再投稿]（仮処理）")
    return "人気ツイート（ダミー）を再投稿"

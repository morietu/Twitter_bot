# main.py

from bot.tweet_generator import generate_tweet_with_number
from bot.zenn_generator import generate_zenn_weekly_article
from bot.scheduler_post import post_by_time
from bot.scheduler_collect import collect_and_analyze
from bot.utils import get_next_episode_number
from bot.note_writer import generate_detailed_note
from utils.google_sheet_logger import log_to_sheet

from datetime import datetime
import os

# --- 設定 ---
ENABLE_TWEET_ANALYSIS = datetime.today().weekday() == 6

# --- ディレクトリ確認 ---
os.makedirs("logs", exist_ok=True)
os.makedirs("articles", exist_ok=True)
os.makedirs("note_articles", exist_ok=True)
os.makedirs("generated/tweets/season_01", exist_ok=True)

def detect_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "朝"
    elif 11 <= hour < 17:
        return "昼"
    else:
        return "夜"


if __name__ == "__main__":
    print("====== 🛠️ Bot起動ランチャー ======")

    # ① GPTツイート生成 & 保存
    print("\n[1] GPTツイート生成")
    season = 1
    episode_number = get_next_episode_number()
    episode_id = f"S{season:02d}-{episode_number:03d}"
    time_of_day = detect_time_of_day()  # 任意に変更可能

    final_text = generate_tweet_with_number(episode_id, time_of_day)

    # ② Googleスプレッドシートにログ送信
    today = datetime.now().strftime("%Y/%m/%d")
    note_url = f"https://note.com/famous_walrus484/n/{episode_id.lower()}"
    log_to_sheet(today, time_of_day, episode_id, final_text, note_url)

    # ③ note原稿生成（週報）
    print("\n[2] note原稿作成（weekly_report）")
    weekly_path = f"note_articles/weekly_report_{datetime.now().strftime('%Y%m%d')}.md"
    with open(weekly_path, "w", encoding="utf-8") as f:
        f.write(f"# 週報（{today}）\n\n{final_text}\n\n---\n自動投稿Botの動作ログ付き")
    print(f"[✅] 保存完了 → {weekly_path}")

    # ④ 人気ツイートの分析（毎週日曜のみ）
    if ENABLE_TWEET_ANALYSIS:
        print("\n[4] ツイート分析（週次）")
        try:
            collect_and_analyze()
        except Exception as e:
            print("[ERROR] ツイート分析に失敗:", e)
    else:
        print("\n[4] ツイート分析：今週はスキップ（日曜のみ実行）")

    # ⑤ 投稿Botの投稿（任意でテスト実行）
    print("\n[5] 投稿Botのテスト投稿（{time_of_day}）")
    post_by_time("朝")

    # ⑥ 詳細note記事を自動生成・保存
    print("\n[6] note用 詳細原稿の保存")
    generate_detailed_note(episode_id, final_text)

    print("\n[7] Zenn週報を生成中...")
    generate_zenn_weekly_article("今週もBotが活躍しました！")

    print("\n====== ✅ すべての処理が完了しました ======")

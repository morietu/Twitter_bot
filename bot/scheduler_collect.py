# データ収集・分類・分析専用

import schedule
import time
from datetime import datetime
import logging
from analysis.collector import collect_tweets
from analysis.classifier import classify_csv
from analysis.analyzer import analyze_labeled_csv

# ログ設定
logging.basicConfig(
    filename="logs/collect_log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)

def collect_and_analyze():
    now = datetime.now().strftime("%Y%m%d-%H%M")
    raw_file = f"data/tweets_{now}.csv"
    labeled_file = raw_file.replace(".csv", "_labeled.csv")

    try:
        print(f"[▶] データ収集開始: {now}")
        collect_tweets(query="#筋トレ", max_results=50, out_dir="data")
        classify_csv(raw_file, labeled_file)
        analyze_labeled_csv(labeled_file)
        logging.info(f"✅ 収集・分析成功: {labeled_file}")
    except Exception as e:
        logging.error(f"❌ 収集・分析エラー: {e}")
        print(f"[ERROR] エラー発生: {e}")

# ⏰ スケジュール設定：8時 / 12時 / 20時
schedule.every().day.at("08:00").do(collect_and_analyze)
schedule.every().day.at("12:00").do(collect_and_analyze)
schedule.every().day.at("20:00").do(collect_and_analyze)

if __name__ == "__main__":
    print("[📅] データ収集スケジューラ稼働中（Ctrl+Cで終了）")
    while True:
        schedule.run_pending()
        time.sleep(10)
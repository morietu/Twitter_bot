import schedule
import time
import random
import os
import logging
from datetime import datetime
from bot.tweet_generator import post_gpt_tweet, post_popular_tweet

def post_popular_tweet():
    log_file = "logs/success_log.txt"
    if not os.path.exists(log_file):
        print("[⚠️] 過去ログが見つかりません")
        return "再投稿できませんでした"

    with open(log_file, "r", encoding="utf-8",errors="ignore") as f:
        lines = f.readlines()

    tweets = []
    current_tweet = []

    for line in lines:
        line = line.strip()
        if "【S" in line:
            if current_tweet:
                tweets.append("\n".join(current_tweet))
                current_tweet = []
        if "https://note.com/" in line:
            current_tweet.append(line)
            tweets.append("\n".join(current_tweet))
            current_tweet = []
        elif line:
            current_tweet.append(line)

    if not tweets:
        print("[⚠️] note付きの投稿履歴がありません")
        return "再投稿候補が見つかりませんでした"

    selected = random.choice(tweets)
    print(f"[♻️] 再投稿ツイート:\n{selected}")
    logging.info(f"[♻️ 再投稿]\n{selected}\n")
    return selected

# ✅ 必須！定義が抜けていた関数
def post_by_time(time_of_day): 
    print(f"[🕒] 投稿処理開始（{time_of_day}）")
    if random.random() < 0.5:
        post_gpt_tweet(time_of_day)
    else:
        post_popular_tweet()

# ⏰ スケジュール：朝6時・昼12時・夜20時
schedule.every().day.at("06:00").do(lambda: post_by_time("朝"))
schedule.every().day.at("12:00").do(lambda: post_by_time("昼"))
schedule.every().day.at("20:00").do(lambda: post_by_time("夜"))

if __name__ == "__main__":
    print("[📢] 投稿Botスケジューラ稼働中（Ctrl+Cで停止）")
    while True:
        schedule.run_pending()
        time.sleep(10)

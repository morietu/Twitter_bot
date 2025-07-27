# scripts/weekly_summary.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bot.scheduler_collect import collect_and_analyze
from bot.zenn_generator import generate_zenn_weekly_article
from datetime import datetime

def run_weekly_summary():
    print("📊【週次レポートBot】開始します...\n")

    print("① ツイート分析を実行中...")
    try:
        collect_and_analyze()
        print("✅ ツイート分析 完了\n")
    except Exception as e:
        print("[ERROR] エラー発生:", e)

    print("② Zenn週報テンプレートを生成中...")
    try:
        generate_zenn_weekly_article("今週もBotが活躍しました！")
        print("✅ Zenn記事テンプレート 生成完了\n")
    except Exception as e:
        print("[ERROR] Zenn記事生成失敗:", e)

    print("📦【完了】週次処理がすべて完了しました！🕒")


if __name__ == "__main__":
    os.makedirs("logs", exist_ok=True)
    os.makedirs("articles", exist_ok=True)
    run_weekly_summary()

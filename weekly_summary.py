from bot.scheduler_collect import collect_and_analyze
from bot.zenn_generator import generate_zenn_weekly_article
import time
import traceback

if __name__ == "__main__":
    print("📊【週次レポートBot】開始します...\n")

    print("① ツイート分析を実行中...")
    try:
        collect_and_analyze()
        print("✅ ツイート分析 完了\n")
    except Exception as e:
        if "429" in str(e):
            print("🔒 API制限によりデータ収集はスキップされました（429 Too Many Requests）\n")
        else:
            print(f"[ERROR] ツイート分析で例外発生: {e}\n")

    print("② Zenn週報テンプレートを生成中...")
    generate_zenn_weekly_article("今週もBotが活躍しました！")
    print("✅ Zenn記事テンプレート 生成完了\n")

    print("📦【完了】週次処理がすべて完了しました！🕒")
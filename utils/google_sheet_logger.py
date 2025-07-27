import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import pytz

import os



def log_to_sheet(date: str, time_of_day: str, episode_id: str, text: str, note_url: str):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    credentials_path = os.path.join(os.getcwd(), "credentials.json")
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        credentials_path, scope
    )
    client = gspread.authorize(credentials)

    try:
        # ✅ スプレッドシートIDを指定するには open_by_key()
        sheet = client.open_by_key("1DMllcMQthsAGzBu52-fBJVbpKQM2RcNFF106YmgDFAc").sheet1
        now = datetime.now(pytz.timezone("Asia/Tokyo")).strftime("%H:%M:%S")

        # ✅ 正しい変数名に修正（6列構成）
        row = [date, now, time_of_day, episode_id, text, note_url]
        sheet.append_row(row)
        print(f"[✅] Googleシートにログを保存しました: {row}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[❌] Googleシートログ保存に失敗: {e}")

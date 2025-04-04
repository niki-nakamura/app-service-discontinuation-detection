# main.py (メインスクリプト) - 全体例

from google_play_scraper import get_google_play_app_info
from app_store_scraper import get_app_store_info
from your_sheet_module import get_worksheet, write_results_to_sheet
from datetime import datetime

# サービス終了キーワードの検知関数
END_KEYWORDS = [
    "サービス終了", "配信終了", "提供終了", "終了のお知らせ",
]

def detect_service_end_status(app_info):
    if app_info['status'] == 'not_found':
        return "配信停止"
    desc = (app_info['description'] or "") + (app_info['name'] or "")
    for kw in END_KEYWORDS:
        if kw in desc:
            return "サービス終了告知あり"
    return "提供中"

def main():
    # 1) 監視対象アプリのリスト (実際には外部ファイルやDBから読み込んでもOK)
    google_play_apps = [
        ("com.example.myapp", "Android"),
        ("com.sample.othergame", "Android"),
    ]
    app_store_apps = [
        ("1234567890", "iOS"),
        ("9876543210", "iOS"),
    ]
    
    # 2) アプリ情報を取得し、ステータス判定
    results = []
    
    # Google Play
    for package_name, platform in google_play_apps:
        info = get_google_play_app_info(package_name)
        status = detect_service_end_status(info)
        results.append({
            'app_name': info['name'] or package_name,
            'platform': platform,
            'status': status,
            'url': info['url']
        })
    
    # App Store
    for app_id, platform in app_store_apps:
        info = get_app_store_info(app_id)
        status = detect_service_end_status(info)
        results.append({
            'app_name': info['name'] or app_id,
            'platform': platform,
            'status': status,
            'url': info['url']
        })
    
    # 3) Google Sheetsに書き込み
    SHEET_KEY = "<あなたのスプレッドシートID>"
    worksheet = get_worksheet(SHEET_KEY, "credentials.json", "シート1")
    write_results_to_sheet(worksheet, results)

if __name__ == '__main__':
    main()

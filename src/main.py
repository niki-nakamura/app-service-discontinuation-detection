# main.py
from bigquery_client import fetch_app_list
from play_store_checker import check_android_app
from app_store_checker import check_ios_app
from notifier import notify_results

# 1. アプリ一覧取得
apps = fetch_app_list()  # [{'app_name':..., 'package':..., 'ios_id':...}, ...]

results = []  # チェック結果を格納
for app in apps:
    # 2. 各ストアでの状況確認
    if app.get('package'):  # Androidアプリがある場合
        android_status = check_android_app(app['package'])
        if android_status['removed'] or android_status['outdated']:
            results.append({"app_name": app['app_name'], "platform": "Android", **android_status})
    if app.get('ios_id') or app.get('ios_bundle'):
        ios_status = check_ios_app(app.get('ios_id') or app['ios_bundle'])
        if ios_status['removed'] or ios_status['outdated']:
            results.append({"app_name": app['app_name'], "platform": "iOS", **ios_status})
# 3. 必要なものだけ results に追加済み

# 4. 通知実施（結果が空なら何もしない等の判定あり）
notify_results(results)

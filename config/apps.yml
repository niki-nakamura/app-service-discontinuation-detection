# app_store_scraper.py
import requests

def get_app_store_info(app_id):
    """
    iTunes Search APIを使ってApp Storeのアプリ情報を取得
    app_id: 数字で構成されるAppleのアプリID (例: 1234567890)
    """
    url = f"https://itunes.apple.com/lookup?id={app_id}&country=jp"
    resp = requests.get(url)
    data = resp.json()
    
    if data.get('resultCount') == 0:
        # 該当アプリが検索にヒットしない → ストア上にないと判断
        return {
            'name': None,
            'description': None,
            'url': f"https://apps.apple.com/jp/app/id{app_id}",
            'status': 'not_found'
        }
    
    result = data['results'][0]
    return {
        'name': result.get('trackName'),
        'description': result.get('description'),
        'url': result.get('trackViewUrl'),
        'status': 'available'
    }

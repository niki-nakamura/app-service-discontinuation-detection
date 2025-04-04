# google_play_scraper.py
from google_play_scraper import app, search
from requests import get
from bs4 import BeautifulSoup

def get_google_play_app_info(package_name):
    """
    指定したパッケージ名のアプリ情報をgoogle-play-scraperで取得
    もし取得に失敗したら配信停止の可能性
    """
    try:
        result = app(package_name, lang='ja', country='jp')
        # 取得成功時のデータ
        return {
            'name': result.get('title'),
            'description': result.get('description'),
            'url': f"https://play.google.com/store/apps/details?id={package_name}",
            'status': 'available'  # 仮に
        }
    except Exception:
        # 取得失敗 → ストアから削除されている可能性が高い
        return {
            'name': None,
            'description': None,
            'url': f"https://play.google.com/store/apps/details?id={package_name}",
            'status': 'not_found'  # 配信停止と推定
        }

def check_app_availability_by_html(package_name):
    """
    HTMLを直接スクレイピングして利用不可メッセージを探す(オプション)
    """
    url = f"https://play.google.com/store/apps/details?id={package_name}"
    response = get(url)
    if response.status_code == 404:
        return 'not_found'
    soup = BeautifulSoup(response.text, 'html.parser')
    # 例: 「このアプリはご利用いただけません」を含むかチェック
    if 'このアプリはご利用いただけません' in soup.text:
        return 'unavailable'
    return 'available'

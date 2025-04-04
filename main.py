# main.py
from google_play_scraper import get_google_play_app_info
from app_store_scraper import get_app_store_info
import re

# サービス終了のキーワード例を列挙
END_KEYWORDS = [
    "サービス終了",
    "配信終了",
    "提供終了",
    "サービス終了のお知らせ",
    "終了のお知らせ",
    "〇月〇日をもってサービス終了"  # 正規表現で日付パターンを拾ってもよい
]

def detect_service_end_status(app_info):
    """
    app_info: { name, description, url, status } の辞書
    からサービス終了を推定し、結果を返す
    """
    # 1) ステータスが not_found の場合: 配信停止とみなす
    if app_info['status'] == 'not_found':
        return "配信停止"

    # 2) 説明文・タイトルにキーワードが含まれるかチェック
    desc = app_info['description'] or ""
    name = app_info['name'] or ""
    combined_text = f"{name}\n{desc}"
    
    # キーワード検知
    for kw in END_KEYWORDS:
        if kw in combined_text:
            return "サービス終了告知あり"
    
    # 特別な記載が無ければ「提供中」
    return "提供中"

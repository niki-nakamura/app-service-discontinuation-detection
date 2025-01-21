import os
import requests
from bs4 import BeautifulSoup
import urllib.parse

def get_latest_ranking_info(url):
    # Google 検索ステータスのページを取得
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # 「Ranking」と書かれた要素を探す(例)
    ranking_span = soup.find("span", string="Ranking")
    if not ranking_span:
        return None

    ranking_table = ranking_span.find_next("table")
    if not ranking_table:
        return None

    first_row = ranking_table.find("tbody").find("tr")
    if not first_row:
        return None

    # Summary
    summary_td = first_row.find("td", class_="ise88CpWulY__summary")
    summary_text = summary_td.get_text(strip=True) if summary_td else None
    link_tag = summary_td.find("a") if summary_td else None
    summary_link = urllib.parse.urljoin(url, link_tag.get("href")) if link_tag else None

    # Date
    date_td = first_row.find("td", class_="ise88CpWulY__date")
    date_text = date_td.get_text(strip=True) if date_td else None

    # Duration
    duration_td = first_row.find("td", class_="ise88CpWulY__duration")
    duration_text = duration_td.get_text(strip=True) if duration_td else None

    return summary_text, summary_link, date_text, duration_text

def post_to_teams(webhook_url, summary, link, date_, duration):
    # Teamsに投稿するためのデータ（MessageCard形式）
    payload = {
        "@type": "MessageCard",
        "@context": "https://schema.org/extensions",
        "summary": "Ranking Info",
        "themeColor": "0078D7",
        "title": "Ranking 最新情報",
        "text": (
            f"**Summary:** {summary}  \n"
            f"**Link:** {link}  \n"
            f"**Date:** {date_}  \n"
            f"**Duration:** {duration}"
        )
    }
    response = requests.post(webhook_url, json=payload)
    response.raise_for_status()

def main():
    # 定義: 取得先のURL
    URL = "https://status.search.google.com/summary"
    info = get_latest_ranking_info(URL)

    if not info:
        print("Ranking 情報が取得できませんでした。")
        return

    summary, link, date_, duration = info

    # GitHub Secrets で登録した環境変数を取得
    teams_webhook_url = os.environ.get("TEAMS_WEBHOOK_URL")

    if not teams_webhook_url:
        print("TEAMS_WEBHOOK_URL が設定されていません。")
        return

    # 投稿
    post_to_teams(teams_webhook_url, summary, link, date_, duration)
    print("Teams に投稿しました。")

if __name__ == "__main__":
    main()

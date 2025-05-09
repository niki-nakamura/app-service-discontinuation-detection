import os, requests, json

def notify_results(results):
    if not results:
        print("検知された提供終了/未更新アプリはありません。")
        return
    # 結果を文字列に整形（Markdown形式）
    lines = ["**提供終了または長期未更新の検知結果**"]
    for res in results:
        status = []
        if res.get("removed"):
            status.append("提供終了")
        if res.get("outdated"):
            status.append("更新停止")
        status_text = "・".join(status)
        lines.append(f"- {res['app_name']} ({res['platform']}): {status_text}（最終更新: {res.get('last_update', '不明')}）")
    report = "\n".join(lines)

    # Slack通知が設定されていればWebhook送信
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if webhook_url:
        payload = {"text": report}
        resp = requests.post(webhook_url, data=json.dumps(payload),
                             headers={'Content-Type': 'application/json'})
        if resp.status_code != 200:
            print(f"Slack通知失敗: {resp.status_code}, {resp.text}")
        else:
            print("Slack通知成功")
    else:
        # Slack未設定なら、とりあえずログ出力（Actionsログ or Issue用に）
        print(report)

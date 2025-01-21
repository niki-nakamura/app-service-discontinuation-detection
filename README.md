以下の手順は、**「Microsoft Teams の Incoming Webhook」×「GitHub Actions」** を使って定期的にPythonスクリプトを実行し、Teamsへ通知するまでの一連の流れを解説したものです。  

---
## 全体の流れ

1. **GitHub上にリポジトリ（Repositories）を作成**  
2. **Teamsの Incoming Webhook URL を GitHub の「シークレット(Secrets)」として設定**  
3. **Python スクリプトをリポジトリに置く**  
4. **GitHub Actions の設定ファイル（ワークフロー）を作成**  
   - 例: 定期実行（Schedule）  
   - Pythonスクリプトを実行して Teams に投稿  
5. **実際にスケジュール動作を確認**  

上記を順番に進めていきます。

---
## 1. GitHub上にリポジトリを作成

1. **GitHub にログイン**  
   - ブラウザで [GitHub](https://github.com/) を開き、アカウントでログインします。

2. **新しいリポジトリを作成**  
   - 画面右上の「+」ボタン→「New repository」をクリック。  
   - リポジトリ名（例: `teams-status-bot`）を入力し、公開範囲を「Public」または「Private」（どちらでもOK）で設定します。  
   - 必要に応じて「READMEを追加」などチェックし、「Create repository」ボタンを押してリポジトリを作成します。

3. **作成したリポジトリに移動**  
   - GitHub上でURLが `https://github.com/<あなたのユーザ名>/teams-status-bot` のようなページが表示されればOKです。

---
## 2. Teams の Webhook URL を GitHub Secrets に登録

Teams で発行された **Incoming Webhook URL** は、**外部からそのチャネルに投稿できるキー** のようなものです。  
GitHub にソースコードとして直接書くのは危険なので、**シークレット（Secrets）** として保管します。

1. **リポジトリの「Settings」を開く**  
   - リポジトリトップ画面右上あたりの「Settings」をクリックします。

2. **「Security」または「Secrets and variables」タブを探す**  
   - GitHubの画面 UI によって名前が少し違いますが、「Secrets and variables」 > 「Actions」 などを選ぶとシークレットの管理画面が出てきます。

3. **「New repository secret」を押す**  
   - シークレットを新規登録できる画面が表示されます。

4. **Webhook URL を貼り付ける**  
   - `Name` に `TEAMS_WEBHOOK_URL` (任意ですがわかりやすい名前に)  
   - `Secret` に **コピーしてきた Webhook URL** （例: `https://cboffice365.webhook.office.com/・・・`） を貼り付けます。
   - 入力後、「Add secret」ボタンをクリックすれば登録完了です。  

:::tip
今後、**Pythonコード側では `os.environ["TEAMS_WEBHOOK_URL"]` で呼び出して** 使う流れになります。
また、Webhook URLについて分からない点があれば担当リーダーか仁紀までお尋ねください。
:::

---
## 3. Python スクリプトをリポジトリに置く

1. **リポジトリのトップページで「Add file」 → 「Create new file」をクリック**  
2. **ファイル名を指定し、Python コードを貼り付ける**  
   - 例: `teams_bot.py`  
3. **サンプルコード（Teams用のIncoming Webhook投稿）**  

以下のサンプルは「Google検索のステータスサイトをスクレイピングして取得し、Teamsに通知する」イメージです。
コーディングスキルのある方は、必要に応じてカスタマイズを行ってください。

```python
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
```

4. **「Commit new file」ボタンを押してコミット**  
   - これで `teams_bot.py` というファイルがリポジトリに保存されます。

---
## 4. GitHub Actions の設定ファイル（ワークフロー）を作成

1. **「Actions」タブを開く**  
   - リポジトリのトップページで、「Actions」をクリックします。

2. **ワークフロー（Workflow）を新規作成**  
   - 「set up a workflow yourself」などのリンクをクリックするか、既存のテンプレートから作成します。

3. **ファイル名を指定してワークフローを記述**  
   - 例: `.github/workflows/scheduled_teams_post.yml`  
   - 以下の例では、**毎日朝9時（UTC）に実行**する設定になっています。日本時間で言うと午後6時になりますので、必要に応じて `cron` の値を変更してください。

```yaml
name: Scheduled Teams Post

on:
  schedule:
    - cron: '0 9 * * *'  # 毎日 09:00 (UTC)に実行
  workflow_dispatch:     # 手動実行もできるようにするオプション

jobs:
  post-to-teams:
    runs-on: ubuntu-latest

    steps:
      # 1. リポジトリのソースコードをチェックアウト
      - name: Check out repository
        uses: actions/checkout@v3

      # 2. Python をセットアップ
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'  # 使いたいバージョン

      # 3. 依存パッケージをインストール (requests, bs4などが必要なら)
      - name: Install dependencies
        run: |
          pip install requests beautifulsoup4

      # 4. TEAMS_WEBHOOK_URL を環境変数に指定して、Pythonを実行
      - name: Run Python script
        env:
          TEAMS_WEBHOOK_URL: ${{ secrets.TEAMS_WEBHOOK_URL }}
        run: |
          python teams_bot.py
```

4. **ファイルの内容を保存(コミット)する**  
   - これで「.github/workflows/scheduled_teams_post.yml」というワークフローがリポジトリに登録されます。

---
## 5. 実際にスケジュール動作を確認

- **ワークフローが正しく設定されていれば**、毎日指定した時刻（cronの時間）に自動で実行されます。  
- また、**手動で実行**することも可能です。`workflow_dispatch:` を設定している場合、Actions画面から手動で「Run workflow」ボタンを押すことで試せます。  

### 実行確認の手順
1. **Actions タブを開く**  
   - 左サイドバーに「Workflows」が表示され、先ほど作成した「Scheduled Teams Post」も見えるはずです。
2. **手動実行(“Run workflow”)** を押す  
   - その場で処理が走り、成功・失敗のログが確認できます。
3. **Teams を見る**  
   - 成功していれば、該当の「Testing_Channel」に指定のメッセージが投稿されているはずです。

---
## まとめ

1. **Teams で Incoming Webhook を作成** → Webhook URL を取得。  
2. **GitHub リポジトリの Secrets に Webhook URL を登録** (安全に保持)。  
3. **Python スクリプト** で `requests.post` を使い、Teams に投稿するコードを書いてリポジトリへ。  
4. **GitHub Actions** で `cron` スケジュールや手動トリガーを設定し、Python を定期実行 → Teams に通知。  

これらのステップで、**「Teams への定期通知ボット」を GitHub Actions 上で運用**することが可能になります。  
  
- 特にポイントとなるのは「Secrets」によるWebhook URLの安全な保管と、「ActionsのYAMLファイル」による定期実行の設定です。  
- 一度セットアップしてしまえば、あとはGitHubが自動的に実行してくれるので便利です。  

ぜひお試しください。

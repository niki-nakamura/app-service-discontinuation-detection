name: Scheduled Teams Post

on:
  schedule:
    - cron: '0 9 * * *'  # 毎日 09:00 (UTC)に実行
  workflow_dispatch     # 「:」を削除！！発火を停止のために／手動実行もできるようにするオプション

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

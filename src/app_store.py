```python
import requests
import sys

def check_ios_app(app_id):
    """
    Query iTunes Search API; return True if app exists, False if removed.
    """
    url = f"https://itunes.apple.com/lookup?id={app_id}"
    try:
        resp = requests.get(url, timeout=10)
        data = resp.json()
        # results が空なら未公開 or 削除
        return bool(data.get('results'))
    except (requests.RequestException, ValueError) as e:
        print(f"iOS check error for {app_id}: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    # 簡易テスト
    import yaml
    cfg = yaml.safe_load(open('config/apps.yml'))
    for app in cfg.get('ios', []):
        exists = check_ios_app(app)
        print(f"iOS {app}: {'OK' if exists else 'Removed'}")
```  

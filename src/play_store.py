```python
from google_play_scraper import app
import sys

def check_android_app(package_name):
    """
    Use google_play_scraper to fetch metadata; return True if exists, False if not.
    """
    try:
        info = app(package_name)
        return True
    except Exception as e:
        print(f"Android check error for {package_name}: {e}", file=sys.stderr)
        return False

if __name__ == '__main__':
    import yaml
    cfg = yaml.safe_load(open('config/apps.yml'))
    for pkg in cfg.get('android', []):
        exists = check_android_app(pkg)
        print(f"Android {pkg}: {'OK' if exists else 'Removed'}")
```  

#!/usr/bin/env python3

import yaml
import requests
import sys

CONFIG_PATH = "config/apps.yml"


def load_config(path=CONFIG_PATH):
    """
    Load the YAML configuration file listing apps and endpoints.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Configuration file not found: {path}", file=sys.stderr)
        sys.exit(1)


def check_endpoint(url):
    """
    Send a HEAD request to the URL and return HTTP status code or None on error.
    """
    try:
        response = requests.head(url, timeout=10)
        return response.status_code
    except requests.RequestException:
        return None


def main():
    config = load_config()

    print("=== Endpoint Status ===")
    for url in config.get('endpoints', []):
        status = check_endpoint(url)
        print(f"{url}: {status}")

    # TODO: implement actual App Store / Play Store checks
    # from app_store import check_ios_app
    # from play_store import check_android_app
    #
    # print("=== iOS App Status ===")
    # for app_id in config.get('ios', []):
    #     status = check_ios_app(app_id)
    #     print(f"iOS {app_id}: {status}")
    #
    # print("=== Android App Status ===")
    # for pkg in config.get('android', []):
    #     status = check_android_app(pkg)
    #     print(f"Android {pkg}: {status}")


if __name__ == '__main__':
    main()

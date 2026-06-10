# -*- coding: utf-8 -*-

import time
from urllib.parse import quote
import cloudscraper

BASE_URL = "https://wiki.52poke.com/wiki/"
DELAY = 1.5  # seconds between requests

session = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
        "mobile": False
    }
)


def fetch_page(title: str) -> str:
    url = BASE_URL + quote(title, safe="")
    time.sleep(DELAY)
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.text

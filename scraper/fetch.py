# -*- coding: utf-8 -*-

import time
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

BASE_URL = "https://wiki.52poke.com/wiki/"
DELAY = 1.5  # seconds between requests

session = requests.Session()
session.headers.update({
    "User-Agent": "pmdb-scraper/1.0 (educational project)"
})
session.mount("https://", HTTPAdapter(max_retries=Retry(
    total=3,
    backoff_factor=2,
    status_forcelist=[500, 502, 503, 504]
)))


def fetch_page(title: str) -> str:
    url = BASE_URL + requests.utils.quote(title, safe="")
    time.sleep(DELAY)
    resp = session.get(url, timeout=10)
    resp.raise_for_status()
    resp.encoding = "utf-8"
    return resp.text

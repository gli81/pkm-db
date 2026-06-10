# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from .fetch import fetch_page

# Master list page title on 52poke
_LIST_PAGE = "宝可梦列表（按全国图鉴编号）"


def build_name_map() -> dict[int, str]:
    """
    Scrape the master Pokémon list and return {dex_num: chinese_name}.
    """
    html = fetch_page(_LIST_PAGE)
    soup = BeautifulSoup(html, "lxml")
    result: dict[int, str] = {}

    for link in soup.select("table.roundy a[href*='/wiki/']"):
        href = link.get("href", "")
        name = href.split("/wiki/")[-1]
        # the cell before or sibling text should have the dex number
        # try to find the number from the parent row
        tr = link.find_parent("tr")
        if tr is None:
            continue
        tds = tr.find_all("td")
        if not tds:
            continue
        try:
            num = int(tds[0].get_text(strip=True).lstrip("#"))
        except ValueError:
            continue
        if 1 <= num <= 386 and name not in result.values():
            result[num] = name

    return result

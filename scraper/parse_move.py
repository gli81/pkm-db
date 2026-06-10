# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from .fetch import fetch_page

# 52poke move list page
_MOVE_LIST_PAGE = "招式列表（按全国图鉴编号）"


def parse_move(chinese_name: str) -> dict:
    """
    Scrape data for a single move page.
    Returns:
        {
            "name_cn": str,
            "type": str,
            "category": str,   # 物理 / 特殊 / 变化
            "power": int|None,
            "accuracy": int|None,
            "pp": int,
            "effect": str
        }
    """
    html = fetch_page(chinese_name)
    soup = BeautifulSoup(html, "lxml")
    move: dict = {"name_cn": chinese_name}

    info_table = soup.find("table", class_=lambda c: c and "roundy" in c)
    if info_table is None:
        return move

    for row in info_table.find_all("tr"):
        tds = row.find_all("td")
        if len(tds) < 2:
            continue
        label = tds[0].get_text(strip=True)
        value = tds[1].get_text(strip=True)

        if "属性" in label or "类型" in label:
            move["type"] = value
        elif "分类" in label:
            move["category"] = value
        elif "威力" in label:
            try:
                move["power"] = int(value)
            except ValueError:
                move["power"] = None
        elif "命中" in label:
            try:
                move["accuracy"] = int(value)
            except ValueError:
                move["accuracy"] = None
        elif "PP" in label:
            try:
                move["pp"] = int(value)
            except ValueError:
                pass

    effect_div = soup.find("div", class_=lambda c: c and "effect" in c)
    if effect_div:
        move["effect"] = effect_div.get_text(" ", strip=True)

    return move

# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from .fetch import fetch_page


def parse_evolution(chinese_name: str) -> list[dict]:
    """
    Scrape evolution conditions for a Pokémon.
    Returns a list of dicts, each describing one evolution step:
        {
            "from": str,   # Chinese name
            "to": str,     # Chinese name
            "condition": str  # raw condition text, e.g. "升到16级"
        }
    """
    html = fetch_page(chinese_name)
    soup = BeautifulSoup(html, "lxml")
    evolutions = []

    # Evolution chain is in a table with class containing "evochain"
    evo_table = soup.find("table", class_=lambda c: c and "evochain" in c)
    if evo_table is None:
        return evolutions

    # Each evolution step: find pairs of Pokémon cells separated by a condition cell
    cells = evo_table.find_all("td")
    i = 0
    while i < len(cells) - 2:
        from_cell = cells[i]
        cond_cell = cells[i + 1]
        to_cell = cells[i + 2]

        from_link = from_cell.find("a")
        to_link = to_cell.find("a")
        if from_link and to_link:
            evolutions.append({
                "from": from_link.get_text(strip=True),
                "to": to_link.get_text(strip=True),
                "condition": cond_cell.get_text(" ", strip=True)
            })
            i += 3
        else:
            i += 1

    return evolutions


def parse_learnset(chinese_name: str, gen: int = 3) -> dict[str, list]:
    """
    Scrape the learnset for a Pokémon in the given generation.
    Returns:
        {
            "level_up": [{"level": int|str, "move": str}, ...],
            "tm_hm":    [{"id": str, "move": str}, ...],
            "egg":      [{"move": str}, ...],
            "tutor":    [{"move": str}, ...]
        }
    """
    html = fetch_page(chinese_name)
    soup = BeautifulSoup(html, "lxml")

    learnset: dict[str, list] = {
        "level_up": [],
        "tm_hm": [],
        "egg": [],
        "tutor": []
    }

    # 52poke learnset tables have a preceding header that names the generation
    # and a class like "wikitable" — find the right generation section first
    gen_header_text = f"第{gen}代"
    target_section = None
    for tag in soup.find_all(["h2", "h3", "h4"]):
        if gen_header_text in tag.get_text():
            target_section = tag
            break

    if target_section is None:
        return learnset

    # Collect all tables until the next same-level header
    tables = []
    for sib in target_section.find_next_siblings():
        if sib.name in ["h2", "h3", "h4"] and gen_header_text not in sib.get_text():
            break
        if sib.name == "table":
            tables.append(sib)

    for table in tables:
        caption = table.find("caption")
        caption_text = caption.get_text(strip=True) if caption else ""

        rows = table.find_all("tr")[1:]  # skip header row
        if "升级" in caption_text or "等级" in caption_text:
            for row in rows:
                tds = row.find_all("td")
                if len(tds) >= 2:
                    learnset["level_up"].append({
                        "level": tds[0].get_text(strip=True),
                        "move": tds[1].get_text(strip=True)
                    })
        elif "TM" in caption_text or "HM" in caption_text or "招式机" in caption_text:
            for row in rows:
                tds = row.find_all("td")
                if len(tds) >= 2:
                    learnset["tm_hm"].append({
                        "id": tds[0].get_text(strip=True),
                        "move": tds[1].get_text(strip=True)
                    })
        elif "蛋" in caption_text or "遗传" in caption_text:
            for row in rows:
                tds = row.find_all("td")
                if tds:
                    learnset["egg"].append({
                        "move": tds[0].get_text(strip=True)
                    })
        elif "教授" in caption_text or "传授" in caption_text:
            for row in rows:
                tds = row.find_all("td")
                if tds:
                    learnset["tutor"].append({
                        "move": tds[0].get_text(strip=True)
                    })

    return learnset

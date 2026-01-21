# -*- coding: utf-8 -*-

from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .models.Type import Type

NUM_TYPES: int = 19
TYPE_LST: List[Type] = [None] * NUM_TYPES
TYPE_NAME_CN: List[str] = [
    "一般", "火", "水", "电", "草", "冰", "格斗", "毒", "地面", "飞行",
    "超能力", "虫", "岩石", "幽灵", "龙", "恶", "钢", "妖精", "???"
]
TYPE_NAME: List[str] = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice", "Fighting",
    "Poison", "Ground", "Flying", "Psychic", "Bug", "Rock", "Ghost",
    "Dragon", "Dark", "Steel", "Fairy", "???"
]
## Note: `TYPE_LST` is declared here but populated at runtime by
## `models.Type.initialize_types()` to avoid circular imports.
## Do not import `Type` at module import time in this file.
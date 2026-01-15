# -*- coding: utf-8 -*-

from json import loads
from json.decoder import JSONDecodeError
from typing import Dict
import traceback
from models.Pokemon import Pokemon
from models.Type import Type


PKM_LIST_DIR: str = "./resources/pkm.json"

NUM_TYPES: int = 19
"""
TYPE_LST
    Contains all Type instances of the 19 types.
    The index of this list will be used in DB to represent the type of Pokemon and Move
    The types are in the following order
        一般 火 水 电 草 冰 格斗 毒 地面 飞行 超能力 虫 岩石 幽灵 龙 恶 钢 妖精 ???
        Normal Fire Water Electric Grass Ice Fighting Poison Ground
        Flying Psychic Bug Rock Ghost Dragon Dark Steel Fairy ???
"""
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
## fill the TYPE_LST
for i in range(NUM_TYPES):
    TYPE_LST[i] = Type(i, TYPE_NAME[i], TYPE_NAME_CN[i])

"""
EFFECTIVE_MAT
    represents the coefficient of damage for attacks between types
    each row represents the coefficient of damage when a type attacking others
    each column represents the coefficient of damage when a type attacked by others
"""
EFFECTIVE_MAT: List[List[float]] = [
    ## Normal Type
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.5, 0, 1, 1, 0.5, 1, 1],
    ## Fire
    [1, 0.5, 0.5, 1, 2, 2, 1, 1, 1, 1, 1, 2, 0.5, 1, 0.5, 1, 2, 1, 1],
    ## Water
    [1, 2, 0.5, 1, 0.5, 1, 1, 1, 2, 1, 1, 1, 2, 1, 0.5, 1, 1, 1, 1],
    ## Electric
    [1, 1, 2, 0.5, 0.5, 1, 1, 1, 0, 2, 1, 1, 1, 1, 0.5, 1, 1, 1, 1],
    ## Grass
    [1, 0.5, 2, 1, 0.5, 1, 1, 0.5, 2, 0.5, 1, 0.5, 2, 1, 0.5, 1, 0.5, 1, 1],
    ## Ice
    [1, 0.5, 0.5, 1, 2, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    ## Fighting
    [2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 2, 0.5, 1],
    ## Poison
    [1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 0, 2, 1],
    ## Ground
    [1, 2, 1, 2, 0.5, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 1, 2, 1, 1],
    ## Flying
    [1, 1, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0.5, 1, 1],
    ## Psychic
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ## Bug
    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0, 0.5, 1, 1],
    ## Rock
    [1, 2, 1, 1, 1, 2, 0.5, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 0.5, 1, 1],
    ## Ghost
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 1, 1],
    ## Dragon
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 0.5, 0, 1],
    ## Dark
    [1, 1, 1, 1, 1, 1, 0.5, 1, 1, 1, 2, 1, 1, 2, 1, 0.5, 1, 0.5, 1],
    ## Steel
    [1, 0.5, 0.5, 0.5, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 0.5, 2, 1],
    ## Fairy
    [1, 0.5, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 1, 1, 1, 2, 2, 0.5, 1, 1],
    ## ??? type only has one status move
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def main():
    assert len(EFFECTIVE_MAT) == NUM_TYPES
    for i in range(NUM_TYPES):
        assert len(EFFECTIVE_MAT[i]) == NUM_TYPES
    ## read file from resource
    with open(PKM_LIST_DIR, 'r', encoding="utf-8") as f:
        try:
            ## json load
            pkm_dict = loads(f.read())
        except JSONDecodeError as e:
            print("Invalid JSON")
            quit()
        except Exception as e:
            print(traceback.format_exc())
    ## format 1-386 pkm
    for pk_name in pkm_dict:
        try:
            if "num" in pkm_dict[pk_name] and 0 < pkm_dict[pk_name]["num"] <=386:
                # print(
                #     Pokemon(
                #         j["num"], j["name"], j["types"],
                #         get_male_ratio_from_json(j),
                #         j["baseStats"],
                #         [j["abilities"][k] for k in j["abilities"] if k != 'H'],
                #         j["heightm"], j["weightkg"],
                #         j["color"], j["eggGroups"]
                #     )
                # )
                print(Pokemon.from_json(pkm_dict[pk_name]))
        except KeyError as ke:
            print(f"{pk_name} no ...")

if __name__ == "__main__":
    main()

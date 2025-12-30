# -*- coding: utf-8 -*-

from json import loads
from json.decoder import JSONDecodeError
from typing import Dict
import traceback


PKM_LIST_DIR = "./resources/pkm.json"

def format_pkm_info(j: Dict[str, Any]) -> str:
    ## format
    """
    num
    name
    types
    male_ratio
    hp
    atk
    def
    spa
    spd
    spe
    abilities
    heightm
    weightkg
    eggGroups
    """
    try:
        stats = j["baseStats"]
        return f"index num: {j["num"]}\t" +\
                f"name: {j["name"]}\t" +\
                f"types: {','.join(j["types"])}\t" +\
                f"male ratio: {get_male_ratio_from_json(j)}\n" +\
                f"HP: {stats["hp"]} ATK: {stats["atk"]}" +\
                f" DEF: {stats["def"]} SpA: {stats["spa"]}" +\
                f" SpD: {stats["spd"]} Spe: {stats["spe"]}\n" +\
                f"abilities: {','.join([j["abilities"][k] for k in j["abilities"] if k != 'H'])}\t" +\
                f"height: {j["heightm"]}m\tweight: {j["weightkg"]}kg\n" +\
                f"color: {j["color"]}\n" +\
                f"egg groups: {','.join(j["eggGroups"])}"
    except Exception as e:
        print(f"{j["num"]} {j["name"]} missing field")
        # print(traceback.format_exc())
        
def get_male_ratio_from_json(j: Dict) -> float:
    if "genderRatio" in j:
        return j["genderRatio"]["M"]
    elif "gender" in j and j["gender"] == 'N':
        return -1.0 ## metang
    elif "gender" not in j and "genderRatio" not in j:
        return -1.0


def main():
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
                print(format_pkm_info(pkm_dict[pk_name]))
        except KeyError as ke:
            print(f"{pk_name} no ...")

if __name__ == "__main__":
    main()

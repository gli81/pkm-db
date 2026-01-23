# -*- coding: utf-8 -*-

from json import loads
from json.decoder import JSONDecodeError
import traceback
from .models.Type import Type
from .models.Pokemon import Pokemon
from .type_effectiveness import constant_checking
import os
from .constants import TYPE_LST, NUM_TYPES, TYPE_NAME, TYPE_NAME_CN

PKM_LIST_DIR: str = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "./resources/pkm.json"
)

def initialize_types() -> None:
    """
    Populate `constants.TYPE_LST` with the 19 `Type` instances.
    Safe to call multiple times; initialization happens only once.
    """
    # already initialized?
    if TYPE_LST[0] is not None:
        return
    for i in range(NUM_TYPES):
        TYPE_LST[i] = Type(i, TYPE_NAME[i], TYPE_NAME_CN[i])


def main():
    constant_checking()
    initialize_types()
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
            quit()
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
                Pokemon.from_json(pkm_dict[pk_name])
        except KeyError as ke:
            print(f"{pk_name} no ...")
    print(TYPE_LST)

if __name__ == "__main__":
    main()

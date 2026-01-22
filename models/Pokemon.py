# -*- coding: utf-8 -*-

from typing import List, Dict

class Pokemon:
    """
    index_num, name, name_cn, types, abilities
    base_stats
    base_points
    height, weight, color
    egg_groups, prevo

    """
    def __init__(
        self, num: int, name: str, types: List[str],
        male_ratio: float, baseStats: Dict[str, int],
        abilities: List[str],
        height: int, weight: int,
        color: str, egg_groups: List[str], prevo: str = None,
        basePoints: List[int] = None
    ):
        self.__index_num: int = num
        self.__name: str = name
        self.__types: List[str] = types
        self.__male_ratio: float = male_ratio
        self.__hp: int = baseStats["hp"]
        self.__atk: int = baseStats["atk"]
        self.__def: int = baseStats["def"]
        self.__spa: int = baseStats["spa"]
        self.__spd: int = baseStats["spd"]
        self.__spe: int = baseStats["spe"]
        self.__abilities = abilities
        self.__basePoints: List[int] = basePoints
        self.__height: int = height
        self.__weight: int = weight
        self.__color: str = color
        self.__egg_groups: List[str] = egg_groups
        self.__prevo: str = prevo

    @classmethod
    def from_json(cls, j: Dict):
        """
        create Pokemon from json
        """
        return cls(
            j["num"], j["name"], j["types"],
            cls.get_male_ratio_from_json(j),
            j["baseStats"],
            [j["abilities"][k] for k in j["abilities"] if k != 'H'],
            j["heightm"], j["weightkg"],
            j["color"], j["eggGroups"],
            None if "prevo" not in j else j["prevo"]
        )


    def __str__(self) -> str:
        return f"{self.__index_num} {self.__name}\n" +\
                f"types: {self.__types}\n" +\
                f"egg groups: {self.__egg_groups}\n" +\
                f"HP: {self.__hp} ATK: {self.__atk}" +\
                f" DEF: {self.__def} SpA: {self.__spa}" +\
                f" SpD: {self.__spd} Spe: {self.__spe}\t" +\
                f"abilities: {self.__abilities}\n" +\
                f"height: {self.__height}m\t" +\
                f"weight: {self.__weight}kg\t" +\
                f"color: {self.__color}\t" + f"male ratio: {self.__male_ratio}\n" +\
                f"prevo: {self.__prevo}"

    @staticmethod
    def get_male_ratio_from_json(j: Dict) -> float:
        if "genderRatio" in j:
            return j["genderRatio"]["M"]
        elif "gender" in j and j["gender"] == 'N':
            return -1.0 ## e.g. metang
        elif "gender" not in j and "genderRatio" not in j:
            return -1.0

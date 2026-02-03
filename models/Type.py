# -*- coding: utf-8 -*-

from typing import List
from ..type_effectiveness import EFFECTIVE_MAT
from ..constants import NUM_TYPES, TYPE_NAME, TYPE_NAME_CN, TYPE_LST

"""
TYPE_LST
    Contains all Type instances of the 19 types.
    The index of this list will be used in DB to represent the type of Pokemon and Move
    The types are in the following order
        一般 火 水 电 草 冰 格斗 毒 地面 飞行 超能力 虫 岩石 幽灵 龙 恶 钢 妖精 ???
        Normal Fire Water Electric Grass Ice Fighting Poison Ground
        Flying Psychic Bug Rock Ghost Dragon Dark Steel Fairy ???
"""


TYPE_NAME_IND = {}
TYPE_NAME_CN_IND = {}
for i in range(NUM_TYPES):
    TYPE_NAME_IND[TYPE_NAME[i]] = i
    TYPE_NAME_CN_IND[TYPE_NAME_CN[i]] = i

class Type:
    """
    num, name, name_cn
    """
    def __init__(
        self, num: int = None, name: str = None, name_cn: str = None
    ):
        assert num is not None or name is not None or name_cn is not None,\
            "Not valid type"
        if num is not None:
            assert name is None or name == TYPE_NAME[num],\
                "Type num and English name don't match"
            name = TYPE_NAME[num]
            assert name_cn is None or name_cn == TYPE_NAME_CN[num],\
                "Type num and Chinese name don't match"
            name_cn = TYPE_NAME_CN[num]
        else:
            ## num is None
            if name is not None:
                num = TYPE_NAME_IND[name]
                ## check name_cn and name have same num
                assert name_cn is None or name_cn == TYPE_NAME_CN[num],\
                    "Type Chinese name and English name don't match"
            else:
                ## name is None, name_cn can't be None
                num = TYPE_NAME_CN_IND[name_cn]
                name = TYPE_NAME[num]
        self.__num = num
        self.__name = name
        self.__name_cn = name_cn
        self.__super_effective = []
        self.__not_very_effective = []
        self.__no_effect = []
        self.__weak_to = []
        self.__resists = []
        self.__immune = []
        for i in range(NUM_TYPES):
            if EFFECTIVE_MAT[self.__num][i] == 2:
                self.__super_effective.append(i)
            elif EFFECTIVE_MAT[self.__num][i] == 0.5:
                self.__not_very_effective.append(i)
            elif EFFECTIVE_MAT[self.__num][i] == 0:
                self.__no_effect.append(i)
            if EFFECTIVE_MAT[i][self.__num] == 2:
                self.__weak_to.append(i)
            elif EFFECTIVE_MAT[i][self.__num] == 0.5:
                self.__resists.append(i)
            elif EFFECTIVE_MAT[i][self.__num] == 0:
                self.__immune.append(i)
        # print(self)


    def __str__(self) -> str:
        return f"{self.__name} type\n\tWeak to: "+\
            f"{", ".join(map(lambda x:TYPE_NAME[x], self.__weak_to))}" +\
            f"\n\tResists: {", ".join([TYPE_NAME[x] for x in self.__resists])}" +\
            f"\n\tImmune: {", ".join([TYPE_NAME[x] for x in self.__immune])}" +\
            f"\n\tSuper effective: {", ".join([TYPE_NAME[x] for x in self.__super_effective])}" +\
            f"\n\tNot very effective: {", ".join([TYPE_NAME[x] for x in self.__not_very_effective])}" +\
            f"\n\tNo effect: {", ".join([TYPE_NAME[x] for x in self.__no_effect])}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def getName(self) -> str:
        return self.__name


def initialize_types() -> None:
    """
    Populate `constants.TYPE_LST` with the 19 `Type` instances.
    Safe to call multiple times; initialization happens only once.
    """
    # from ..constants import TYPE_LST
    # already initialized?
    if TYPE_LST[0] is not None:
        return
    for i in range(NUM_TYPES):
        TYPE_LST[i] = Type(i, TYPE_NAME[i], TYPE_NAME_CN[i])




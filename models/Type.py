# -*- coding: utf-8 -*-


class Type:
    """
    num, name, name_cn
    """
    def __init__(
        self, num: int, name: str, name_cn: str
    ):
        self.__num = num
        self.__name = name
        self.__name_cn = name_cn

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
    [1, 0.5, 0.5, 1, 2, 0.5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, 0.5, 1, 1],
    ## Fighting
    [2, 1, 1, 1, 1, 2, 1, 0.5, 1, 0.5, 0.5, 0.5, 2, 0, 1, 2, 2, 0.5, 1],
    ## Poison
    [1, 1, 1, 1, 2, 1, 1, 0.5, 0.5, 1, 1, 1, 0.5, 0.5, 1, 1, 0, 2, 1],
    ## Ground
    [1, 2, 1, 2, 0.5, 1, 1, 2, 1, 0, 1, 0.5, 2, 1, 1, 1, 2, 1, 1],
    ## Flying
    [1, 1, 1, 0.5, 2, 1, 2, 1, 1, 1, 1, 2, 0.5, 1, 1, 1, 0.5, 1, 1],
    ## Psychic
    [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 0.5, 1, 1, 1, 1, 0, 0.5, 1, 1],
    ## Bug
    [1, 0.5, 1, 1, 2, 1, 0.5, 0.5, 1, 0.5, 2, 1, 1, 0.5, 1, 2, 0.5, 0.5, 1],
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
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def constant_checking() -> None:
    assert len(EFFECTIVE_MAT) == NUM_TYPES, "Wrong num of types"
    COUNTS = [
        # """
        # [
        #     super_effective, not_very_effective, no effect,
        #     weak_to, resists, immune
        # ]
        # """
        ## Normal, Fire, Water
        [0, 2, 1, 1, 0, 1], [4, 4, 0, 3, 6, 0], [3, 3, 0, 2, 4, 0],
        ## Electric, Grass, Ice
        [2, 3, 1, 1, 3, 0], [3, 7, 0, 5, 4, 0], [4, 4, 0, 4, 1, 0],
        ## Fighting, Poison, Ground
        [5, 5, 1, 3, 3, 0], [2, 4, 1, 2, 5, 0], [5, 2, 1, 3, 2, 1],
        ## Flying, Psychic, Bug
        [3, 3, 0, 3, 3, 1], [2, 2, 1, 3, 2, 0], [3, 7, 0, 3, 3, 0],
        ## Rock, Ghost, Dragon
        [4, 3, 0, 5, 4, 0], [2, 1, 1, 2, 2, 2], [1, 1, 1, 3, 4, 0],
        ## Dark, Steel, Fairy
        [2, 3, 0, 3, 2, 1], [3, 4, 0, 3, 10, 1], [3, 3, 0, 2, 3, 1],
        ## ???
        [0, 0, 0, 0, 0, 0]
    ]
    for i in range(NUM_TYPES):
        assert len(EFFECTIVE_MAT[i]) == NUM_TYPES,\
            f"Type {TYPE_NAME[i]} has wrong length"
        check_row(i, COUNTS[i][:3])
    for i in range(NUM_TYPES):
        check_col(i, COUNTS[i][3:])

def check_row(i: int, target: List[int]) -> None:
    ## get counts of 2, 0.5, 0 in EFFECTIVE_MAT[i, :]
    super_effective = 0
    not_very_effective = 0
    no_effect = 0
    for j in range(NUM_TYPES):
        if EFFECTIVE_MAT[i][j] == 2:
            super_effective += 1
        elif EFFECTIVE_MAT[i][j] == 0.5:
            not_very_effective += 1
        elif EFFECTIVE_MAT[i][j] == 0:
            no_effect += 1
    assert [super_effective, not_very_effective, no_effect] == target,\
        f"Type {TYPE_NAME[i]} offensive not lining up"

def check_col(i: int, target: List[int]) -> None:
    ## get counts of 2, 0.5, 0 in EFFECTIVE_MAT[:, i]
    weak_to = 0
    resists = 0
    immune = 0
    for j in range(NUM_TYPES):
        if EFFECTIVE_MAT[j][i] == 2:
            weak_to += 1
        elif EFFECTIVE_MAT[j][i] == 0.5:
            resists += 1
        elif EFFECTIVE_MAT[j][i] == 0:
            immune += 1
    assert [weak_to, resists, immune] == target,\
        f"Type {TYPE_NAME[i]} defensive not lining up: " +\
        f"{[weak_to, resists, immune]} - {target}"
# -*- coding: utf-8 -*-

# from typing import List

class Move:
    """
    move_num, name, name_cn, type, ph/sp/mo,
    damage, priority, pp

    """
    def __init__(
        self, move_num: int, name: str, name_cn:str,
        type: str, cate: int, damage: int, 
        priority: int, pp: int
    ):
        self.__index = move_num
        self.__name = name
        self.__name_cn = name_cn
        self.__type = type
        self.__category = cate
        self.__damage = damage
        self.__pp = pp
        self.__priority = priority
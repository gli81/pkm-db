# -*- coding: utf-8 -*-

class EggGroup:
    """
    egg_group_num, name, name_cn

    """
    def __init__(
        self, egg_group_num: int, name: str, name_cn: str = None
    ):
        self.__index = egg_group_num
        self.__name = name
        self.__name_cn = name_cn

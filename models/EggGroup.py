# -*- coding: utf-8 -*-

from typing import Optional

class EggGroup:
    """
    egg_group_num, name, name_cn

    """
    def __init__(
        self, egg_group_num: int, name: str, name_cn: Optional[str] = None
    ):
        self.__index = egg_group_num
        self.__name = name
        self.__name_cn = name_cn

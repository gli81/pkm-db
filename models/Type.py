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
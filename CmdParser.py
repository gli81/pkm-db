# -*- coding: utf-8 -*-

from pmdb.constants import TYPE_NAME
from pmdb.models.Type import TYPE_LST
from typing import Union

class CmdParser:
    def __init__(self):
        self.__help_txt = "Commands:\n" +\
            "\tq type <TypeName>\tshow type matchups\n" +\
            "\tquit\t\t\texit"

    def parse(self, command: str) -> Union[str, dict[str, str]]:
        c = command.strip()
        c_lower = c.lower()
        if c_lower == "quit":
            exit(0)
        elif c_lower == "help" or c_lower == 'h':
            return self.__help_txt
        elif c_lower.startswith("q"):
            c_lst = c.split(' ')
            if len(c_lst) == 3:
                if c_lst[1].lower() == "type" and c_lst[2].capitalize() in TYPE_NAME:
                    for t in TYPE_LST:
                        if t and t.getName() == c_lst[2].capitalize():
                            return t.__repr__()
        return "Invalid command"
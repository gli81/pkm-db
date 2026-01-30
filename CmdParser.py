# -*- coding: utf-8 -*-

from .constants import TYPE_NAME
from typing import Dict

class CmdParser:
    def __init__(self):
        pass

    def parse(self, command: str) -> str | Dict[str, str]:
        c = command.strip()
        if c.lower() == "quit":
            exit(0)
        elif c.lower().startswith("q"):
            c_lst = c.split(' ')
            if len(c_lst) == 3:
                if c_lst[1].lower() == "type" and c_lst[2].capitalize() in TYPE_NAME:
                    return c
        
        return "Invalid command"
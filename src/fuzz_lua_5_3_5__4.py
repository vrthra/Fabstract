import Abstract as A
import Fuzz as F
import json
import os
import os.path
import tempfile
import random

import lua_5_3_5__4 as Main

import sys
if __name__ == '__main__':
    F.main('./lang/lua/grammar/lua.fbjson', './lang/lua/bugs/4.lua', Main.my_predicate)
